# Runtime Contract Hierarchy Projection 实施需求

**日期**: 2026-03-30
**目标**: 在不改变 runtime packet 和 execution manifest 公开 hierarchy 字段名的前提下，抽取 hierarchy 共享投影逻辑，降低 root/child 治理链路上的字段漂移风险。

## Intent Contract

- Goal: 把 `hierarchy` 从 `Freeze-RuntimeInputPacket.ps1` 和 `Invoke-PlanExecute.ps1` 的重复手工拼装收口为共享 helper。
- Deliverable:
  - `scripts/runtime/VibeRuntime.Common.ps1` 新增 hierarchy projection helper。
  - `Freeze-RuntimeInputPacket.ps1` 与 `Invoke-PlanExecute.ps1` 复用同一 helper。
  - 新增 characterization tests，冻结 hierarchy 兼容契约。
- Constraints:
  - 不改变现有 hierarchy 字段名。
  - 不改变 root/child authority 语义。
  - 不混入更大的 runtime summary / route / outputs / mirror 结构改造。
- Acceptance Criteria:
  - runtime packet 的 `hierarchy` 由共享 helper 构造。
  - execution manifest 的 `hierarchy` 由共享 helper 构造。
  - root scope 下 packet 与 execution manifest 的 hierarchy 字段保持一致。
  - child scope 的 null/继承字段语义被 helper-level test 覆盖。
- Product Acceptance Criteria:
  - 后续继续做 runtime schema extraction 时，不需要再在多个脚本里分别修改 hierarchy 投影逻辑。
  - 现有 governed runtime / topology tests 不退化。
- Manual Spot Checks:
  - root scope 运行时，比较 runtime packet 和 execution manifest 的 hierarchy。
  - helper-level 测试覆盖 child scope 下 `parent_run_id` / `parent_unit_id` / inherited paths 的行为。
- Completion Language Policy:
  - 只能宣称“hierarchy projection 子波次完成”，不能把它外推为整个 Runtime Contract Wave 2 完成。
- Delivery Truth Contract:
  - 必须有 fresh test evidence。
- Non-goals:
  - 不处理 `invoke-vibe-runtime.ps1` summary 的 hierarchy 收口。
  - 不处理 authority projection。
  - 不处理 route snapshot 或 custom admission projection。
- Autonomy Mode: `interactive_governed`
- Inferred Assumptions:
  - hierarchy 是下一条最适合收口的 runtime contract 重复链，因为它已有主流程测试面且变更半径小。
