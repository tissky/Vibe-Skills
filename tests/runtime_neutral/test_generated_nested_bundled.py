from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
HELPERS = REPO_ROOT / "scripts" / "common" / "vibe-governance-helpers.ps1"
PS_RESOLVER = REPO_ROOT / "scripts" / "common" / "Resolve-VgoAdapter.ps1"
PY_RESOLVER = REPO_ROOT / "scripts" / "common" / "resolve_vgo_adapter.py"
PS_INSTALLER = REPO_ROOT / "scripts" / "install" / "Install-VgoAdapter.ps1"
PY_INSTALLER = REPO_ROOT / "scripts" / "install" / "install_vgo_adapter.py"
SYNC_SCRIPT = REPO_ROOT / "scripts" / "governance" / "sync-bundled-vibe.ps1"
INSTALL_REQUIRED_SKILLS = (
    "dialectic",
    "local-vco-roles",
    "spec-kit-vibe-compat",
    "superclaude-framework-compat",
    "ralph-loop",
    "cancel-ralph",
    "tdd-guide",
    "think-harder",
    "brainstorming",
    "writing-plans",
    "subagent-driven-development",
    "systematic-debugging",
)


def resolve_powershell() -> str | None:
    candidates = [
        shutil.which("pwsh"),
        shutil.which("pwsh.exe"),
        r"C:\Program Files\PowerShell\7\pwsh.exe",
        r"C:\Program Files\PowerShell\7-preview\pwsh.exe",
        shutil.which("powershell"),
        shutil.which("powershell.exe"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(Path(candidate))
    return None


class GeneratedNestedBundledTests(unittest.TestCase):
    def setUp(self) -> None:
        self.powershell = resolve_powershell()
        if self.powershell is None:
            self.skipTest("PowerShell is required for generated nested bundled tests.")
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self._write_fixture()
        subprocess.run(["git", "init"], cwd=self.root, capture_output=True, text=True, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.root, capture_output=True, text=True, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=self.root, capture_output=True, text=True, check=True)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def _write(self, relative_path: str, content: str) -> None:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")

    def _write_fixture(self) -> None:
        self._write("scripts/common/vibe-governance-helpers.ps1", HELPERS.read_text(encoding="utf-8"))
        self._write("scripts/governance/sync-bundled-vibe.ps1", SYNC_SCRIPT.read_text(encoding="utf-8"))
        self._write("config/operator-preview-contract.json", json.dumps({"contract_version": 1, "preview_output_root": "outputs/governance/preview"}, indent=2) + "\n")
        self._write(
            "config/version-governance.json",
            json.dumps(
                {
                    "release": {"version": "9.9.9", "updated": "2026-03-30", "channel": "stable", "notes": "fixture"},
                    "source_of_truth": {
                        "canonical_root": ".",
                        "bundled_root": "bundled/skills/vibe",
                        "nested_bundled_root": "bundled/skills/vibe/bundled/skills/vibe",
                    },
                    "mirror_topology": {
                        "canonical_target_id": "canonical",
                        "sync_source_target_id": "canonical",
                        "targets": [
                            {"id": "canonical", "path": ".", "role": "canonical", "required": True, "presence_policy": "required", "sync_enabled": False, "parity_policy": "authoritative"},
                            {"id": "bundled", "path": "bundled/skills/vibe", "role": "mirror", "required": True, "presence_policy": "required", "sync_enabled": True, "parity_policy": "full"},
                            {"id": "nested_bundled", "path": "bundled/skills/vibe/bundled/skills/vibe", "role": "mirror", "required": False, "presence_policy": "if_present_must_match", "sync_enabled": False, "parity_policy": "full", "materialization_mode": "release_install_only"},
                        ],
                    },
                    "execution_context_policy": {
                        "require_outer_git_root": True,
                        "fail_if_script_path_is_under_mirror_root": True,
                    },
                    "packaging": {
                        "mirror": {
                            "files": ["SKILL.md"],
                            "directories": ["config", "scripts"],
                        },
                        "allow_bundled_only": [],
                        "normalized_json_ignore_keys": ["updated", "generated_at"],
                    },
                },
                indent=2,
            )
            + "\n",
        )
        self._write("SKILL.md", "---\nname: vibe\ndescription: fixture\n---\n")
        self._write("config/sample.json", json.dumps({"version": 1}, indent=2) + "\n")
        self._write("scripts/sample.ps1", "Write-Host 'sample'\n")

    def _run_sync(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                self.powershell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(self.root / "scripts" / "governance" / "sync-bundled-vibe.ps1"),
                *extra,
            ],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=True,
        )

    def test_default_sync_skips_creating_missing_generated_nested_target(self) -> None:
        self._run_sync("-PruneBundledExtras")

        bundled_root = self.root / "bundled" / "skills" / "vibe"
        nested_root = bundled_root / "bundled" / "skills" / "vibe"
        self.assertTrue((bundled_root / "SKILL.md").exists())
        self.assertFalse((nested_root / "SKILL.md").exists())

    def test_opt_in_sync_materializes_generated_nested_target(self) -> None:
        self._run_sync("-PruneBundledExtras", "-IncludeGeneratedCompatibilityTargets")

        bundled_root = self.root / "bundled" / "skills" / "vibe"
        nested_root = bundled_root / "bundled" / "skills" / "vibe"
        self.assertTrue((bundled_root / "SKILL.md").exists())
        self.assertTrue((nested_root / "SKILL.md").exists())
        self.assertEqual(
            (self.root / "config" / "sample.json").read_text(encoding="utf-8"),
            (nested_root / "config" / "sample.json").read_text(encoding="utf-8"),
        )


class InstallTimeGeneratedNestedBundledTests(unittest.TestCase):
    def setUp(self) -> None:
        self.powershell = resolve_powershell()
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.repo_root = self.root / "repo"
        self.target_root = self.root / "target"
        self.repo_root.mkdir(parents=True, exist_ok=True)
        self.target_root.mkdir(parents=True, exist_ok=True)
        self._write_install_fixture()

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def _write(self, relative_path: str, content: str) -> None:
        path = self.repo_root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")

    def _write_install_fixture(self) -> None:
        self._write("scripts/common/vibe-governance-helpers.ps1", HELPERS.read_text(encoding="utf-8"))
        self._write("scripts/common/Resolve-VgoAdapter.ps1", PS_RESOLVER.read_text(encoding="utf-8"))
        self._write("scripts/common/resolve_vgo_adapter.py", PY_RESOLVER.read_text(encoding="utf-8"))
        self._write("scripts/install/Install-VgoAdapter.ps1", PS_INSTALLER.read_text(encoding="utf-8"))
        self._write("scripts/install/install_vgo_adapter.py", PY_INSTALLER.read_text(encoding="utf-8"))
        self._write("config/upstream-lock.json", json.dumps({"lock_version": 1}, indent=2) + "\n")
        self._write(
            "config/runtime-core-packaging.json",
            json.dumps(
                {
                    "schema_version": 1,
                    "package_id": "runtime-core",
                    "directories": ["skills", "config"],
                    "copy_directories": [{"source": "bundled/skills", "target": "skills"}],
                    "copy_files": [{"source": "config/upstream-lock.json", "target": "config/upstream-lock.json", "optional": False}],
                    "canonical_vibe_mirror": {"enabled": True, "target_relpath": "skills/vibe"},
                },
                indent=2,
            )
            + "\n",
        )
        self._write(
            "config/version-governance.json",
            json.dumps(
                {
                    "release": {"version": "9.9.9", "updated": "2026-03-30", "channel": "stable", "notes": "fixture"},
                    "source_of_truth": {
                        "canonical_root": ".",
                        "bundled_root": "bundled/skills/vibe",
                        "nested_bundled_root": "bundled/skills/vibe/bundled/skills/vibe",
                    },
                    "mirror_topology": {
                        "canonical_target_id": "canonical",
                        "sync_source_target_id": "canonical",
                        "targets": [
                            {"id": "canonical", "path": ".", "role": "canonical", "required": True, "presence_policy": "required", "sync_enabled": False, "parity_policy": "authoritative"},
                            {"id": "bundled", "path": "bundled/skills/vibe", "role": "mirror", "required": True, "presence_policy": "required", "sync_enabled": True, "parity_policy": "full"},
                            {"id": "nested_bundled", "path": "bundled/skills/vibe/bundled/skills/vibe", "role": "mirror", "required": False, "presence_policy": "if_present_must_match", "sync_enabled": False, "parity_policy": "full", "materialization_mode": "release_install_only"},
                        ],
                    },
                    "packaging": {
                        "mirror": {
                            "files": ["SKILL.md", "check.ps1", "check.sh", "install.ps1", "install.sh"],
                            "directories": ["config", "protocols", "references", "docs", "templates", "scripts", "mcp"],
                        },
                        "allow_bundled_only": [],
                        "normalized_json_ignore_keys": ["updated", "generated_at"],
                    },
                    "runtime": {
                        "installed_runtime": {
                            "target_relpath": "skills/vibe",
                            "receipt_relpath": "skills/vibe/outputs/runtime-freshness-receipt.json",
                            "require_nested_bundled_root": False,
                        }
                    },
                },
                indent=2,
            )
            + "\n",
        )

        self._write("SKILL.md", "---\nname: vibe\ndescription: fixture\n---\n")
        self._write("check.ps1", "Write-Host 'check'\n")
        self._write("check.sh", "#!/usr/bin/env bash\necho check\n")
        self._write("install.ps1", "Write-Host 'install'\n")
        self._write("install.sh", "#!/usr/bin/env bash\necho install\n")
        self._write("config/sample.json", json.dumps({"version": 1}, indent=2) + "\n")
        self._write("protocols/runtime.md", "# runtime\n")
        self._write("references/index.md", "# refs\n")
        self._write("docs/readme.md", "# docs\n")
        self._write("templates/template.txt", "template\n")
        self._write("scripts/runtime/sample.ps1", "Write-Host 'sample'\n")
        self._write("mcp/servers.template.json", json.dumps({"servers": []}, indent=2) + "\n")

        vibe_root = self.repo_root / "bundled" / "skills" / "vibe"
        vibe_root.mkdir(parents=True, exist_ok=True)
        for rel in ("SKILL.md", "check.ps1", "check.sh", "install.ps1", "install.sh"):
            source = self.repo_root / rel
            target = vibe_root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
        for rel in ("config", "protocols", "references", "docs", "templates", "scripts", "mcp"):
            source = self.repo_root / rel
            target = vibe_root / rel
            if source.is_dir():
                shutil.copytree(source, target)

        self.assertFalse((vibe_root / "bundled" / "skills" / "vibe" / "SKILL.md").exists())

        for name in INSTALL_REQUIRED_SKILLS:
            skill_dir = self.repo_root / "bundled" / "skills" / name
            skill_dir.mkdir(parents=True, exist_ok=True)
            (skill_dir / "SKILL.md").write_text(f"---\nname: {name}\ndescription: fixture\n---\n", encoding="utf-8", newline="\n")

    def assert_generated_nested_installed(self) -> None:
        installed_root = self.target_root / "skills" / "vibe"
        nested_root = installed_root / "bundled" / "skills" / "vibe"
        self.assertTrue((installed_root / "SKILL.md").exists())
        self.assertTrue((nested_root / "SKILL.md").exists())
        self.assertEqual(
            (installed_root / "config" / "sample.json").read_text(encoding="utf-8"),
            (nested_root / "config" / "sample.json").read_text(encoding="utf-8"),
        )
        self.assertEqual(
            (installed_root / "scripts" / "runtime" / "sample.ps1").read_text(encoding="utf-8"),
            (nested_root / "scripts" / "runtime" / "sample.ps1").read_text(encoding="utf-8"),
        )

    def test_python_installer_materializes_generated_nested_compatibility_root(self) -> None:
        subprocess.run(
            [
                "python3",
                str(self.repo_root / "scripts" / "install" / "install_vgo_adapter.py"),
                "--repo-root",
                str(self.repo_root),
                "--target-root",
                str(self.target_root),
                "--host",
                "openclaw",
                "--profile",
                "minimal",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assert_generated_nested_installed()

    def test_powershell_fallback_installer_materializes_generated_nested_compatibility_root(self) -> None:
        if self.powershell is None:
            self.skipTest("PowerShell is required for fallback installer test.")

        env = os.environ.copy()
        empty_path = self.root / "no-python-path"
        empty_path.mkdir(parents=True, exist_ok=True)
        env["PATH"] = str(empty_path)
        subprocess.run(
            [
                self.powershell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(self.repo_root / "scripts" / "install" / "Install-VgoAdapter.ps1"),
                "-RepoRoot",
                str(self.repo_root),
                "-TargetRoot",
                str(self.target_root),
                "-HostId",
                "openclaw",
                "-Profile",
                "minimal",
            ],
            capture_output=True,
            text=True,
            check=True,
            env=env,
        )
        self.assert_generated_nested_installed()
