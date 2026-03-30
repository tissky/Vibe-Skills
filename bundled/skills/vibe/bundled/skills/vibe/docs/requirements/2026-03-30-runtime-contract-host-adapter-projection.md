# Runtime Contract Host Adapter Projection 实施需求

**日期**: 2026-03-30
**目标**: 在不退化当前 runtime / router / specialist execution 行为的前提下，实施技术债修复路线中的 Wave 2 起步批次：把 host adapter 相关契约从散落的手工拼装收口为共享 projection/helper。

## Intent Contract

- Goal: 先收口 runtime contract 中最重复、最容易漂移的 `host_adapter` 字段投影，而不是一次性重写整个 runtime packet / execution manifest schema。
- Deliverable:
  - `scripts/runtime/VibeRuntime.Common.ps1` 提供共享 host adapter identity / projection helper。
  - `Freeze-RuntimeInputPacket.ps1`、`Invoke-PlanExecute.ps1`、`VibeExecution.Common.ps1` 复用同一组 helper。
  - 新增 characterization tests，冻结 requested/effective host adapter 的兼容契约。
- Constraints:
  - 不修改 router route selection 语义。
  - 不修改 release / outputs / mirror topology。
  - 不做 breaking rename；现有字段名必须继续保留。
  - 不要求本轮抽取 runtime packet 的所有字段，只收口 host adapter projection 这一小段。
- Acceptance Criteria:
  - runtime input packet 里的 `host_adapter.requested_host_id/effective_host_id` 由共享 helper 构造。
  - execution manifest 里的 `route_runtime_alignment.requested_host_adapter_id/effective_host_adapter_id` 由共享 helper 投影。
  - specialist execution accounting / result 继续保留现有 requested/effective host adapter 语义。
  - 新增测试能直接验证 helper 语义，并验证 runtime packet 与 execution manifest 的字段对齐。
- Product Acceptance Criteria:
  - 后续继续做 runtime schema extraction 时，不需要再在三个脚本里分别手工改 host adapter 逻辑。
  - 当前 `test_multi_host_specialist_execution.py` 等现有 runtime-neutral 测试不退化。
- Manual Spot Checks:
  - 使用非 `codex` host 运行 runtime，检查 runtime packet、execution manifest、specialist accounting 的 requested/effective host adapter 值一致。
  - 检查 helper 对 fallback host id、closure path、target root 的投影是否稳定。
- Completion Language Policy:
  - 只有 helper 落地、测试通过、阶段清理完成后，才允许宣称本波次完成。
- Delivery Truth Contract:
  - 本轮完成声明只覆盖 Wave 2 的 host adapter projection extraction，不外推到整个 runtime schema extraction 全部完成。
- Non-goals:
  - 不做 runtime packet 全字段 schema 化。
  - 不拆 `Invoke-PlanExecute.ps1` 大文件。
  - 不改变 specialist dispatch 的审批/执行策略。
- Autonomy Mode: `interactive_governed`
- Inferred Assumptions:
  - 当前最安全的 Wave 2 切入点是 host adapter projection，因为它已有现成测试面且重复度高。
