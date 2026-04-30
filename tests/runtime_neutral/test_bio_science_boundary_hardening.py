from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "packages" / "runtime-core" / "src"))

from vgo_runtime.router_contract_runtime import route_prompt  # noqa: E402


def route(prompt: str, task_type: str = "research", grade: str = "M") -> dict[str, object]:
    return route_prompt(
        prompt=prompt,
        grade=grade,
        task_type=task_type,
        repo_root=REPO_ROOT,
    )


def selected(result: dict[str, object]) -> tuple[str, str]:
    selected_row = result.get("selected")
    assert isinstance(selected_row, dict), result
    return str(selected_row.get("pack_id") or ""), str(selected_row.get("skill") or "")


def ranked_summary(result: dict[str, object]) -> list[tuple[str, str, float, str]]:
    ranked = result.get("ranked")
    assert isinstance(ranked, list), result
    rows: list[tuple[str, str, float, str]] = []
    for row in ranked[:8]:
        assert isinstance(row, dict), row
        rows.append(
            (
                str(row.get("pack_id") or ""),
                str(row.get("selected_candidate") or ""),
                float(row.get("score") or 0.0),
                str(row.get("candidate_selection_reason") or ""),
            )
        )
    return rows


class BioScienceBoundaryHardeningTests(unittest.TestCase):
    def assert_selected(
        self,
        prompt: str,
        expected_pack: str,
        expected_skill: str,
        *,
        task_type: str = "research",
        grade: str = "M",
    ) -> None:
        result = route(prompt, task_type=task_type, grade=grade)
        self.assertEqual((expected_pack, expected_skill), selected(result), ranked_summary(result))

    def assert_not_selected(
        self,
        prompt: str,
        blocked_pack: str,
        blocked_skill: str,
        *,
        task_type: str = "research",
        grade: str = "M",
    ) -> None:
        result = route(prompt, task_type=task_type, grade=grade)
        self.assertNotEqual((blocked_pack, blocked_skill), selected(result), ranked_summary(result))

    def test_geniml_owns_bed_genomic_interval_embeddings(self) -> None:
        self.assert_selected(
            "对 BED genomic intervals 做 embeddings 和 similarity search。",
            "bio-science",
            "geniml",
        )

    def test_negated_genomic_ml_does_not_route_to_geniml(self) -> None:
        self.assert_not_selected(
            "用 random forest 对普通临床表格做 machine learning，不是 genomic ML。",
            "bio-science",
            "geniml",
        )

    def test_chinese_bu_shi_negation_keeps_flowio_from_stealing_scanpy(self) -> None:
        self.assert_selected(
            "做 single-cell RNA-seq clustering 和 UMAP，不是 flow cytometry，也不是 FCS 文件解析。",
            "bio-science",
            "scanpy",
        )


if __name__ == "__main__":
    unittest.main()
