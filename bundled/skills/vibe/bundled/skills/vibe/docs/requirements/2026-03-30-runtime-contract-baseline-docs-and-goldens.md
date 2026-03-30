# Runtime Contract Baseline Docs And Goldens 实施需求

**日期**: 2026-03-30
**目标**: 在不改变现有 runtime artifact 公开字段名的前提下，补齐 Runtime Contract Wave 2 剩余的 contract field 文档与 packet/manifest curated golden snapshots，为进入 Wave 3 之前建立稳定 baseline。

## Intent Contract

- Goal: 把 runtime packet / execution manifest / runtime summary 的关键字段约束显式文档化，并为 packet/manifest 补一组 curated golden snapshots。
- Deliverable:
  - 新增长期 contract 文档，写清 required fields、optional compatibility fields、allowed deprecations。
  - 新增 packet/manifest curated golden fixture。
  - 新增 golden-based runtime neutral test。
- Constraints:
  - 不改变现有公开字段名。
  - golden 只冻结高价值稳定字段，不做全 JSON parity。
  - 动态值必须显式归一化，不能把 run id、时间戳、绝对路径直接写入 golden。
  - 不进入 Wave 3 outputs migration。
- Acceptance Criteria:
  - repo 内有可引用的 runtime contract schema 文档。
  - packet/manifest 有可执行的 curated golden baseline。
  - golden 测试与现有 schema/bridge/topology 测试同时通过。
- Product Acceptance Criteria:
  - 后续 Wave 3/4 改造时，可以先看 contract 文档，再用 goldens 识别是否发生非预期语义漂移。
  - runtime contract 的关键公共面不再只靠 scattered tests 隐式表达。
- Manual Spot Checks:
  - 文档应覆盖 runtime input packet、execution manifest、runtime summary。
  - golden 应只锁定稳定字段，并明确归一化策略。
  - goldens 不能和 host-specific absolute path 强耦合。
- Completion Language Policy:
  - 只能宣称“Wave 2 baseline docs/goldens 子波次完成”，不能把它外推为整个技术债修复完成。
- Delivery Truth Contract:
  - 必须有 fresh test evidence。
- Non-goals:
  - 不做 outputs fixture family 迁移。
  - 不做 nested mirror policy 变更。
  - 不重构 router/runtime 主流程。
- Autonomy Mode: `interactive_governed`
- Inferred Assumptions:
  - Wave 2 在进入 Wave 3 前，最缺的是“显式字段文档 + curated baseline”，而不是继续抽更多 helper。
