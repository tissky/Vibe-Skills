from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


class DiscoverableWrapperHostVisibilityTests(unittest.TestCase):
    def test_shell_check_reports_host_visible_discoverable_entries(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            target_root = Path(tempdir) / "codex-root"
            subprocess.run(
                [
                    "bash",
                    str(REPO_ROOT / "install.sh"),
                    "--host",
                    "codex",
                    "--profile",
                    "full",
                    "--target-root",
                    str(target_root),
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            result = subprocess.run(
                [
                    "bash",
                    str(REPO_ROOT / "check.sh"),
                    "--host",
                    "codex",
                    "--profile",
                    "full",
                    "--target-root",
                    str(target_root),
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            self.assertIn("[OK] host-visible discoverable entries", result.stdout)

    def test_shell_check_fails_when_a_wrapper_entry_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            target_root = Path(tempdir) / "codex-root"
            subprocess.run(
                [
                    "bash",
                    str(REPO_ROOT / "install.sh"),
                    "--host",
                    "codex",
                    "--profile",
                    "full",
                    "--target-root",
                    str(target_root),
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            (target_root / "commands" / "vibe-how.md").unlink()

            result = subprocess.run(
                [
                    "bash",
                    str(REPO_ROOT / "check.sh"),
                    "--host",
                    "codex",
                    "--profile",
                    "full",
                    "--target-root",
                    str(target_root),
                ],
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertIn("[FAIL] host-visible discoverable entries", result.stdout)

    def test_powershell_check_reports_host_visible_discoverable_entries(self) -> None:
        if shutil.which("pwsh") is None:
            self.skipTest("pwsh not available")

        with tempfile.TemporaryDirectory() as tempdir:
            target_root = Path(tempdir) / "codex-root"
            subprocess.run(
                [
                    "pwsh",
                    "-NoProfile",
                    "-File",
                    str(REPO_ROOT / "install.ps1"),
                    "-HostId",
                    "codex",
                    "-Profile",
                    "full",
                    "-TargetRoot",
                    str(target_root),
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            result = subprocess.run(
                [
                    "pwsh",
                    "-NoProfile",
                    "-File",
                    str(REPO_ROOT / "check.ps1"),
                    "-HostId",
                    "codex",
                    "-Profile",
                    "full",
                    "-TargetRoot",
                    str(target_root),
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            self.assertIn("[OK] host-visible discoverable entries", result.stdout)


if __name__ == "__main__":
    unittest.main()
