#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REQUIRED_HEADINGS = ["## Highlights", "## Validation Notes", "## Migration Notes"]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def resolve_repo_root(start_path: Path) -> Path:
    current = start_path.resolve()
    if current.is_file():
        current = current.parent
    candidates: list[Path] = []
    while True:
        if (current / "config" / "version-governance.json").exists():
            candidates.append(current)
        if current.parent == current:
            break
        current = current.parent
    if not candidates:
        raise RuntimeError(f"Unable to resolve VCO repo root from: {start_path}")
    git_candidates = [candidate for candidate in candidates if (candidate / ".git").exists()]
    if git_candidates:
        return git_candidates[-1]
    return candidates[-1]


def load_governance(repo_root: Path) -> dict[str, Any]:
    return json.loads((repo_root / "config" / "version-governance.json").read_text(encoding="utf-8-sig"))


def default_release_note_path(repo_root: Path) -> Path:
    governance = load_governance(repo_root)
    version = str((governance.get("release") or {}).get("version") or "").strip()
    if not version:
        raise RuntimeError("release.version is missing from config/version-governance.json")
    return repo_root / "docs" / "releases" / f"v{version}.md"


def evaluate_note(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    normalized = [line.strip() for line in lines]
    todo_lines = [index + 1 for index, line in enumerate(lines) if "TODO" in line.upper()]
    headings = [line.strip() for line in lines if line.startswith("## ")]
    heading_counts = Counter(headings)
    duplicate_headings = sorted([heading for heading, count in heading_counts.items() if count > 1])
    missing_headings = [heading for heading in REQUIRED_HEADINGS if heading not in heading_counts]
    return {
        "path": str(path),
        "todo_lines": todo_lines,
        "duplicate_headings": duplicate_headings,
        "missing_headings": missing_headings,
        "headings": headings,
        "headline": normalized[0] if normalized else "",
        "passes": not todo_lines and not duplicate_headings and not missing_headings,
    }


def evaluate(repo_root: Path, note_paths: list[Path]) -> dict[str, Any]:
    checks = [evaluate_note(path) for path in note_paths]
    failing = [item for item in checks if not item["passes"]]
    return {
        "evaluated_at": utc_now(),
        "repo_root": str(repo_root),
        "required_headings": list(REQUIRED_HEADINGS),
        "summary": {
            "gate_result": "PASS" if not failing else "FAIL",
            "note_count": len(checks),
            "failing_note_count": len(failing),
            "completion_language_allowed": len(failing) == 0,
        },
        "notes": checks,
    }


def write_artifacts(repo_root: Path, artifact: dict[str, Any], output_directory: str | None) -> None:
    output_root = Path(output_directory) if output_directory else repo_root / "outputs" / "verify"
    json_path = output_root / "vibe-release-notes-quality-gate.json"
    md_path = output_root / "vibe-release-notes-quality-gate.md"
    write_text(json_path, json.dumps(artifact, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Vibe Release Notes Quality Gate",
        "",
        f"- Gate Result: **{artifact['summary']['gate_result']}**",
        f"- Notes Checked: `{artifact['summary']['note_count']}`",
        f"- Failing Notes: `{artifact['summary']['failing_note_count']}`",
        "",
        "## Notes",
        "",
    ]
    for item in artifact["notes"]:
        lines.append(f"- `{item['path']}` passes=`{item['passes']}`")
        if item["todo_lines"]:
            lines.append(f"  todo_lines={item['todo_lines']}")
        if item["duplicate_headings"]:
            lines.append(f"  duplicate_headings={item['duplicate_headings']}")
        if item["missing_headings"]:
            lines.append(f"  missing_headings={item['missing_headings']}")
    write_text(md_path, "\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate release note structure and quality invariants.")
    parser.add_argument("--repo-root", help="Optional explicit repository root.")
    parser.add_argument("--path", action="append", dest="paths", help="Optional explicit release note path. Defaults to the current governed release note.")
    parser.add_argument("--write-artifacts", action="store_true", help="Write JSON/Markdown artifacts.")
    parser.add_argument("--output-directory", help="Optional output directory for artifacts.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve() if args.repo_root else resolve_repo_root(Path(__file__))
    note_paths = [Path(item).resolve() for item in args.paths] if args.paths else [default_release_note_path(repo_root)]
    artifact = evaluate(repo_root, note_paths)
    if args.write_artifacts:
        write_artifacts(repo_root, artifact, args.output_directory)
    print(json.dumps(artifact, ensure_ascii=False, indent=2))
    return 0 if artifact["summary"]["gate_result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
