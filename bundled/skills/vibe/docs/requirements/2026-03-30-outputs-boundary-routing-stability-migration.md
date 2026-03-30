# Outputs Boundary Routing Stability Migration 实施需求

**日期**: 2026-03-30
**目标**: 作为 Wave 3 第一批迁移，把 `outputs/verify/vibe-routing-stability-gate.{json,md}` 从 tracked legacy outputs 退役，只保留 `references/fixtures/verify/routing-stability/` 作为 canonical fixture root。

## Intent Contract

- Goal: 迁移最小、消费面最窄的 outputs family，验证 outputs boundary migration 路径可行。
- Deliverable:
  - `outputs-boundary-policy.json` 不再把 routing-stability 视为 tracked allowlisted output。
  - 旧 `outputs/verify/vibe-routing-stability-gate.{json,md}` 从 tracked surface 移除。
  - 新增 migration characterization test，冻结该 family 的迁移契约。
- Constraints:
  - 不改变 `references/fixtures/verify/routing-stability/` 现有 fixture 内容。
  - 不改变 `migration-map.json` 的已存在镜像映射记录。
  - 不同时迁移 external-corpus 或 retro-compare family。
- Acceptance Criteria:
  - tracked outputs 计数从 `21` 下降到 `19`。
  - policy 不再包含 routing-stability allowlisted set。
  - 仓库内不再跟踪 `outputs/verify/vibe-routing-stability-gate.{json,md}`。
  - fixture root 中对应文件仍存在。
- Product Acceptance Criteria:
  - outputs boundary 继续保持“生成物不进入 tracked outputs”方向收敛。
  - 首批迁移不影响现有 verify/runtime 行为。
- Manual Spot Checks:
  - 检查仓库中不再有 tracked `outputs/verify/vibe-routing-stability-gate.*`。
  - 检查 `references/fixtures/verify/routing-stability/` 两个 fixture 文件仍存在。
- Completion Language Policy:
  - 只能宣称“routing-stability outputs family 迁移完成”，不能外推为整个 Wave 3 完成。
- Delivery Truth Contract:
  - 必须有 fresh gate/test evidence。
- Non-goals:
  - 不迁移 `external-corpus` family。
  - 不迁移 `retro-compare` families。
  - 不切换 `strict_requires_zero_tracked_outputs`。
- Autonomy Mode: `interactive_governed`
- Inferred Assumptions:
  - routing-stability family 是最安全的首批对象，因为 fixture 已存在且仓库内没有读取旧 tracked outputs 路径的消费方。
