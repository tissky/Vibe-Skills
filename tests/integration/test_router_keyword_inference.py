from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
ROUTE_SCRIPT = REPO_ROOT / "scripts" / "router" / "resolve-pack-route.ps1"


def _resolve_powershell() -> str | None:
    return shutil.which("pwsh") or shutil.which("powershell")


def _invoke_route(prompt: str) -> dict[str, object]:
    powershell = _resolve_powershell()
    if not powershell:
        pytest.skip("PowerShell executable not available in PATH")

    completed = subprocess.run(
        [
            powershell,
            "-NoLogo",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(ROUTE_SCRIPT),
            "-Prompt",
            prompt,
        ],
        capture_output=True,
        check=True,
    )
    return json.loads(completed.stdout.decode("utf-8-sig"))


def test_router_infers_grade_and_task_type_from_keyword_style_prompt() -> None:
    route = _invoke_route(
        "debug router confidence-low fallback misroute task-classification grade-selection candidate-scoring"
    )

    assert route["task_type"] == "debug"
    assert route["grade"] == "L"


def test_router_keyword_style_prompt_does_not_fall_into_ml_or_clinical_pack() -> None:
    route = _invoke_route(
        "debug router confidence-low fallback misroute task-classification grade-selection candidate-scoring evidence"
    )

    selected = route.get("selected") or {}
    assert selected.get("pack_id") not in {"data-ml", "science-clinical-regulatory"}
