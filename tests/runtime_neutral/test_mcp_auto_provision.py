from __future__ import annotations

import importlib
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = REPO_ROOT / "config" / "mcp-auto-provision.registry.json"
CLI_SRC = REPO_ROOT / "apps" / "vgo-cli" / "src"

if str(CLI_SRC) not in sys.path:
    sys.path.insert(0, str(CLI_SRC))


def load_provision_module():
    return importlib.import_module("vgo_cli.mcp_provision")


class McpAutoProvisionContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.target_root = Path(self.tempdir.name) / "target-root"
        self.target_root.mkdir(parents=True, exist_ok=True)
        self.module = None

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_registry_declares_required_surfaces_for_all_public_hosts(self) -> None:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8-sig"))
        self.assertEqual(
            ["github", "context7", "serena", "scrapling", "claude-flow"],
            registry["required_servers"],
        )
        self.assertEqual(
            ["claude-code", "codex", "cursor", "openclaw", "opencode", "windsurf"],
            sorted(registry["hosts"].keys()),
        )

    def test_registry_declares_status_vocabulary_approved_in_spec(self) -> None:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8-sig"))
        self.assertEqual(
            [
                "ready",
                "attempt_failed",
                "host_native_unavailable",
                "missing_credentials",
                "verification_failed",
                "not_attempted_due_to_host_contract",
            ],
            registry["allowed_statuses"],
        )

    def test_attempt_failures_are_captured_without_blocking_install(self) -> None:
        self.module = load_provision_module()
        report = self.module.provision_required_mcp(
            repo_root=REPO_ROOT,
            target_root=self.target_root,
            host_id="cursor",
            profile="full",
            allow_scripted_install=True,
            executor=self.module.FakeExecutor(
                results={
                    ("host_native", "github"): self.module.ProvisionResult(status="host_native_unavailable"),
                    ("host_native", "context7"): self.module.ProvisionResult(status="ready"),
                    ("host_native", "serena"): self.module.ProvisionResult(status="ready"),
                    ("scripted_cli", "scrapling"): self.module.ProvisionResult(
                        status="attempt_failed",
                        failure_reason="pip missing",
                    ),
                    ("scripted_cli", "claude-flow"): self.module.ProvisionResult(status="ready"),
                }
            ),
        )
        self.assertTrue(report["mcp_auto_provision_attempted"])
        self.assertEqual("installed_locally", report["install_state"])
        self.assertEqual("host_native_unavailable", self.module.lookup_server(report, "github")["status"])
        self.assertEqual("attempt_failed", self.module.lookup_server(report, "scrapling")["status"])
        self.assertEqual("final_report_only", self.module.lookup_server(report, "scrapling")["disclosure_mode"])

    def test_scripted_cli_probe_marks_existing_tool_ready(self) -> None:
        self.module = load_provision_module()
        executor = self.module.ProvisionExecutor()
        original_which = self.module.shutil.which
        self.addCleanup(setattr, self.module.shutil, "which", original_which)
        self.module.shutil.which = lambda name: f"/mock/bin/{name}" if name == "scrapling" else None

        result = executor.attempt(
            strategy="scripted_cli",
            server_name="scrapling",
            contract={"verify_path": "command_present"},
            repo_root=REPO_ROOT,
            target_root=self.target_root,
            host_id="cursor",
            allow_scripted_install=True,
        )

        self.assertEqual("ready", result.status)

    def test_not_attempted_status_marks_attempted_false(self) -> None:
        self.module = load_provision_module()
        original_which = self.module.shutil.which
        self.addCleanup(setattr, self.module.shutil, "which", original_which)
        self.module.shutil.which = lambda _name: None
        report = self.module.provision_required_mcp(
            repo_root=REPO_ROOT,
            target_root=self.target_root,
            host_id="cursor",
            profile="full",
            allow_scripted_install=False,
        )

        self.assertFalse(self.module.lookup_server(report, "scrapling")["attempted"])
        self.assertEqual(
            "not_attempted_due_to_host_contract",
            self.module.lookup_server(report, "scrapling")["status"],
        )

    def test_incomplete_registry_contract_degrades_to_warning_receipt(self) -> None:
        self.module = load_provision_module()
        original_load_registry = self.module.load_registry
        self.addCleanup(setattr, self.module, "load_registry", original_load_registry)
        self.module.load_registry = lambda _repo_root: {
            "required_servers": ["github"],
            "hosts": {
                "cursor": {
                    "attempt_order": ["github"],
                    "servers": {},
                }
            },
        }

        report = self.module.provision_required_mcp(
            repo_root=REPO_ROOT,
            target_root=self.target_root,
            host_id="cursor",
            profile="full",
            allow_scripted_install=True,
        )

        github = self.module.lookup_server(report, "github")
        self.assertEqual("attempt_failed", github["status"])
        self.assertIn("registry", str(github["failure_reason"]))

    def test_receipt_write_failure_does_not_abort_report_generation(self) -> None:
        self.module = load_provision_module()
        original_write_receipt = self.module.write_receipt
        self.addCleanup(setattr, self.module, "write_receipt", original_write_receipt)

        def fail_write_receipt(target_root: Path, receipt: dict[str, object]) -> Path:
            raise OSError("disk full")

        self.module.write_receipt = fail_write_receipt

        report = self.module.provision_required_mcp(
            repo_root=REPO_ROOT,
            target_root=self.target_root,
            host_id="cursor",
            profile="full",
            allow_scripted_install=True,
            executor=self.module.FakeExecutor(
                results={
                    ("host_native", "github"): self.module.ProvisionResult(status="ready"),
                    ("host_native", "context7"): self.module.ProvisionResult(status="ready"),
                    ("host_native", "serena"): self.module.ProvisionResult(status="ready"),
                    ("scripted_cli", "scrapling"): self.module.ProvisionResult(status="ready"),
                    ("scripted_cli", "claude-flow"): self.module.ProvisionResult(status="ready"),
                }
            ),
        )

        self.assertTrue(report["mcp_auto_provision_attempted"])
        self.assertEqual("ready", self.module.lookup_server(report, "scrapling")["status"])

    def test_install_completion_report_summarizes_mcp_follow_up_once(self) -> None:
        output_module = importlib.import_module("vgo_cli.output")
        report = {
            "install_state": "installed_locally",
            "mcp_auto_provision_attempted": True,
            "mcp_results": [
                {
                    "name": "github",
                    "status": "host_native_unavailable",
                    "provision_path": "host_native",
                    "next_step": "Register in host UI.",
                },
                {
                    "name": "scrapling",
                    "status": "attempt_failed",
                    "provision_path": "scripted_cli",
                    "next_step": "Install scrapling CLI.",
                },
            ],
        }
        with io.StringIO() as buffer, redirect_stdout(buffer):
            output_module.print_install_completion_report(
                frontend="shell",
                host_id="cursor",
                profile="full",
                target_root=self.target_root,
                install_receipt={"profile": "full"},
                mcp_receipt=report,
            )
            rendered = buffer.getvalue()

        self.assertIn("MCP auto-provision summary", rendered)
        self.assertIn("manual_follow_up", rendered)
        self.assertNotIn("[WARN] github", rendered)


if __name__ == "__main__":
    unittest.main()
