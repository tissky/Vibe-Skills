from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "packages" / "runtime-core" / "src"))

from vgo_runtime.router_contract_runtime import route_prompt  # noqa: E402


def route(prompt: str, task_type: str = "coding", grade: str = "M") -> dict[str, object]:
    return route_prompt(prompt=prompt, grade=grade, task_type=task_type, repo_root=REPO_ROOT)


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
                str(row.get("candidate_selection_reason") or row.get("legacy_role") or ""),
            )
        )
    return rows


def load_pack(pack_id: str) -> dict[str, object]:
    manifest = json.loads((REPO_ROOT / "config" / "pack-manifest.json").read_text(encoding="utf-8-sig"))
    return next(pack for pack in manifest["packs"] if pack["id"] == pack_id)


class ZeroRouteAuthoritySecondPassTests(unittest.TestCase):
    def assert_selected(
        self,
        prompt: str,
        expected_pack: str,
        expected_skill: str,
        *,
        task_type: str = "coding",
        grade: str = "M",
    ) -> None:
        result = route(prompt, task_type=task_type, grade=grade)
        self.assertEqual((expected_pack, expected_skill), selected(result), ranked_summary(result))

    def test_cloud_modalcom_has_direct_owner(self) -> None:
        pack = load_pack("cloud-modalcom")
        self.assertEqual(["modal-labs"], pack["skill_candidates"])
        self.assertEqual(["modal-labs"], pack["route_authority_candidates"])
        self.assertEqual([], pack["stage_assistant_candidates"])

    def test_cloud_modalcom_routes_chinese_modal_deployment(self) -> None:
        self.assert_selected("用 Modal 部署 Python GPU 函数和云端作业", "cloud-modalcom", "modal-labs")
        self.assert_selected("把 FastAPI 部署到 Modal 而不是 Vercel", "cloud-modalcom", "modal-labs")
        self.assert_selected("用 modal.com 部署 Python GPU function", "cloud-modalcom", "modal-labs")
        self.assert_selected("使用 Modal Labs 运行 serverless GPU batch job", "cloud-modalcom", "modal-labs")

    def test_cloud_modalcom_does_not_capture_frontend_modal_dialogs(self) -> None:
        result = route("修复 React modal dialog 弹窗和 overlay 样式", task_type="coding")
        self.assertNotEqual(("cloud-modalcom", "modal-labs"), selected(result), ranked_summary(result))

    def test_ml_torch_geometric_has_one_canonical_owner(self) -> None:
        pack = load_pack("ml-torch-geometric")
        self.assertEqual(["torch-geometric"], pack["skill_candidates"])
        self.assertEqual(["torch-geometric"], pack["route_authority_candidates"])
        self.assertEqual([], pack["stage_assistant_candidates"])
        self.assertEqual("torch-geometric", pack["defaults_by_task"]["planning"])
        self.assertEqual("torch-geometric", pack["defaults_by_task"]["coding"])
        self.assertEqual("torch-geometric", pack["defaults_by_task"]["research"])

    def test_ml_torch_geometric_routes_alias_keywords_to_canonical_skill(self) -> None:
        self.assert_selected("用 PyTorch Geometric 构建 GCN 图神经网络", "ml-torch-geometric", "torch-geometric")
        self.assert_selected("用 torch_geometric 写 GAT 节点分类模型", "ml-torch-geometric", "torch-geometric")
        self.assert_selected("训练 PyG graph classification pipeline", "ml-torch-geometric", "torch-geometric")

    def test_ml_torch_geometric_does_not_capture_generic_pytorch(self) -> None:
        result = route("用 PyTorch 训练 CNN 图像分类模型，不涉及 graph neural network 或 PyG", task_type="coding")
        self.assertNotEqual(("ml-torch-geometric", "torch-geometric"), selected(result), ranked_summary(result))

    def test_science_quantum_has_direct_owners(self) -> None:
        pack = load_pack("science-quantum")
        expected = ["qiskit", "cirq", "pennylane", "qutip"]
        self.assertEqual(expected, pack["skill_candidates"])
        self.assertEqual(expected, pack["route_authority_candidates"])
        self.assertEqual([], pack["stage_assistant_candidates"])
        self.assertEqual("qiskit", pack["defaults_by_task"]["planning"])
        self.assertEqual("qiskit", pack["defaults_by_task"]["coding"])
        self.assertEqual("qiskit", pack["defaults_by_task"]["research"])

    def test_science_quantum_routes_to_ecosystem_owners(self) -> None:
        self.assert_selected("用 Qiskit 构建量子电路并在 simulator 上运行", "science-quantum", "qiskit")
        self.assert_selected("用 Cirq 写 quantum gate circuit 和 moments", "science-quantum", "cirq")
        self.assert_selected("用 PennyLane 做 quantum machine learning 变分量子线路", "science-quantum", "pennylane")
        self.assert_selected("用 QuTiP 模拟开放量子系统 master equation", "science-quantum", "qutip")

    def test_selected_packs_do_not_reintroduce_stage_assistants(self) -> None:
        for pack_id in ("cloud-modalcom", "ml-torch-geometric", "science-quantum"):
            with self.subTest(pack_id=pack_id):
                self.assertEqual([], load_pack(pack_id)["stage_assistant_candidates"])


if __name__ == "__main__":
    unittest.main()
