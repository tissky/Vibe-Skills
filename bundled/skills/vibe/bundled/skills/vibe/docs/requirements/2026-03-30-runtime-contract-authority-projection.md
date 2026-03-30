# Runtime Contract Authority Projection 实施需求

**日期**: 2026-03-30
**目标**: 在不改变 runtime packet、execution manifest 与 execute receipt 公开 authority 字段名的前提下，抽取 authority 共享投影逻辑，降低 root/child 治理链路上的字段漂移风险。

## Intent Contract

- Goal: 把 `authority_flags`、execution manifest `authority` 与 execute receipt `completion_claim_allowed` 的同源 authority 布尔位收口为共享 helper。
- Deliverable:
  - `scripts/runtime/VibeRuntime.Common.ps1` 新增 authority projection helpers。
  - `Freeze-RuntimeInputPacket.ps1` 与 `Invoke-PlanExecute.ps1` 复用同一 authority 能力投影。
  - 新增 characterization tests，冻结 authority 兼容契约。
- Constraints:
  - 不改变现有 authority JSON 字段名。
  - 不改变 root/child authority 语义。
  - 不修改 `Get-VibeHierarchyState` 作为 authority 源状态。
  - 不混入更大的 route/runtime summary/outputs/mirror 结构改造。
- Acceptance Criteria:
  - runtime packet 的 `authority_flags` 由共享 helper 构造。
  - execution manifest 的 `authority` 由共享 helper 构造。
  - execute receipt 的 `completion_claim_allowed` 从同一 authority 能力投影读取。
  - root 与 child scope 下 packet / manifest / receipt authority 语义保持一致。
- Product Acceptance Criteria:
  - 后续继续做 runtime schema extraction 时，不需要再在多个脚本里分别修改 authority 投影逻辑。
  - governed runtime / hierarchy / delivery acceptance tests 不退化。
- Manual Spot Checks:
  - root scope 运行时，比较 runtime packet `authority_flags` 与 execution manifest `authority` 的字段映射。
  - child scope 运行时，确认四个 authority 布尔位均为 `false`。
  - compare execute receipt `completion_claim_allowed` with execution manifest `authority.completion_claim_allowed`.
- Completion Language Policy:
  - 只能宣称“authority projection 子波次完成”，不能把它外推为整个 Runtime Contract Wave 2 完成。
- Delivery Truth Contract:
  - 必须有 fresh test evidence。
- Non-goals:
  - 不处理 runtime summary authority 收口。
  - 不处理 route/runtime alignment helper。
  - 不重命名 hierarchy state 的 `allow_*` 字段。
- Autonomy Mode: `interactive_governed`
- Inferred Assumptions:
  - authority 是 hierarchy 之后最小且高收益的重复链，且已有 root/child/runtime delivery acceptance 测试面可以稳定兜底。
