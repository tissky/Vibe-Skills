from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


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


def install_minimal_codex_runtime(target_root: Path) -> None:
    result = subprocess.run(
        [
            "bash",
            str(REPO_ROOT / "install.sh"),
            "--host",
            "codex",
            "--profile",
            "minimal",
            "--skip-runtime-freshness-gate",
            "--target-root",
            str(target_root),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise AssertionError(f"install failed\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")


class CheckInstalledRuntimeRootTests(unittest.TestCase):
    def test_check_sh_accepts_installed_runtime_root(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            target_root = Path(tempdir) / ".codex"
            install_minimal_codex_runtime(target_root)
            installed_root = target_root / "skills" / "vibe"

            result = subprocess.run(
                [
                    "bash",
                    str(REPO_ROOT / "check.sh"),
                    "--host",
                    "codex",
                    "--profile",
                    "minimal",
                    "--skip-runtime-freshness-gate",
                    "--target-root",
                    str(installed_root),
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )

        self.assertEqual(0, result.returncode, msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
        self.assertNotIn("skills/vibe/skills/vibe", result.stdout)

    def test_check_ps1_accepts_installed_runtime_root(self) -> None:
        powershell = resolve_powershell()
        if powershell is None:
            self.skipTest("PowerShell executable not available in PATH")

        with tempfile.TemporaryDirectory() as tempdir:
            target_root = Path(tempdir) / ".codex"
            install_minimal_codex_runtime(target_root)
            installed_root = target_root / "skills" / "vibe"

            result = subprocess.run(
                [
                    powershell,
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(REPO_ROOT / "check.ps1"),
                    "-HostId",
                    "codex",
                    "-Profile",
                    "minimal",
                    "-SkipRuntimeFreshnessGate",
                    "-TargetRoot",
                    str(installed_root),
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )

        self.assertEqual(0, result.returncode, msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
        self.assertNotIn("skills\\vibe\\skills\\vibe", result.stdout)


if __name__ == "__main__":
    unittest.main()
