# Runtime Summary Projection 实施需求

**日期**: 2026-03-30
**目标**: 在不改变 runtime summary 公开字段名、相对路径策略与 artifact 语义的前提下，把 `invoke-vibe-runtime.ps1` 中的 runtime summary 手工拼装收口为共享 helper，降低公共汇总契约漂移风险。

## Intent Contract

- Goal: 把 `runtime-summary.json` 的 summary object 从脚本内手工拼装收口为共享 projection helper。
- Deliverable:
  - `scripts/runtime/VibeRuntime.Common.ps1` 新增 runtime summary projection helpers。
  - `scripts/runtime/invoke-vibe-runtime.ps1` 改为复用同一 helper 构造 summary。
  - 新增 characterization tests，冻结 summary 兼容契约。
- Constraints:
  - 不改变现有 summary 字段名。
  - 不改变 `artifacts` / `artifacts_relative` 的路径策略。
  - 不改变 memory activation / delivery acceptance 的摘要字段语义。
  - 不混入 outputs boundary、mirror topology 或 router 行为改造。
- Acceptance Criteria:
  - runtime summary 的 `hierarchy` 由共享 helper 构造。
  - runtime summary 的 `artifacts` 与 `artifacts_relative` 由共享 helper 构造。
  - runtime summary 的 `memory_activation` 与 `delivery_acceptance` 摘要由共享 helper 构造。
  - 现有 bridge / memory activation / canonical surface gates 不退化。
- Product Acceptance Criteria:
  - 后续继续做 Wave 2 schema extraction 时，不需要再在 `invoke-vibe-runtime.ps1` 内直接维护整块 summary 结构。
  - runtime summary 仍保持现有 tests/gates 预期的公共契约。
- Manual Spot Checks:
  - 比较 `runtime-summary.json` 与 payload `summary` 的字段一致性。
  - 检查 `artifacts_relative` 是否仍是相对路径。
  - 检查 `delivery_acceptance` 缺省和有报告时的结构是否不变。
- Completion Language Policy:
  - 只能宣称“runtime summary projection 子波次完成”，不能把它外推为整个 Runtime Contract Wave 2 完成。
- Delivery Truth Contract:
  - 必须有 fresh test evidence。
- Non-goals:
  - 不修改 `runtime-summary.json` 的文件名或落盘位置。
  - 不改变 payload 返回结构。
  - 不进入 Wave 3 outputs migration。
- Autonomy Mode: `interactive_governed`
- Inferred Assumptions:
  - runtime summary 是 authority 之后下一条最适合收口的公共汇总契约面，因为它影响 bridge/gates，但变更半径仍可控制在单 consumer + shared helper。
