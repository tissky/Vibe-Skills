# Release Operator Closure 实施需求

**日期**: 2026-03-30
**目标**: 在不退化当前 routing / release / install / runtime / verify 行为的前提下，实施技术债修复路线中的 Wave 1：把 `scripts/governance/release-cut.ps1` 收口为更完整的 release operator，并补齐对应验证。

## Intent Contract

- Goal: 实施 release operator closure，而不是继续停留在规划层。
- Deliverable:
  - `release-cut.ps1` 能自动收口 `docs/releases/README.md` 和 `dist/*/manifest.json` 的 release 面。
  - 新增 release note 质量校验。
  - 新增对 release-cut 行为的 runtime-neutral 测试。
- Constraints:
  - 不在本轮修改 runtime contract schema、outputs migration、mirror topology policy。
  - 不允许引入会破坏现有 `release-cut` preview/apply 语义的行为。
  - 不能让 release-cut 在现有 `v2.3.53` 仓库状态下失败。
- Acceptance Criteria:
  - `release-cut.ps1 -Preview` 能显示新增 release surface 改动。
  - `release-cut.ps1` apply 路径会更新 `docs/releases/README.md` 当前 surface 和 recent releases 列表。
  - `release-cut.ps1` apply 路径会更新 `dist/*/manifest.json` 中的 `source_release.version/updated`。
  - 自动生成的新 release note 不再写入 `TODO` 占位。
  - 新增质量 gate / tests 可以发现 `TODO` 和重复主标题问题。
- Product Acceptance Criteria:
  - 发布面从“operator + 手工补面”收口为“operator 主路径 + 手工编辑内容补充”。
  - 当前现有发布/验证脚本仍可运行。
- Manual Spot Checks:
  - 用临时版本号执行 preview / apply，检查 release README 和 dist manifests 是否跟随更新。
  - 检查新增 release note 模板是否没有 `TODO`。
  - 检查新 gate 是否能拦截故意构造的坏 note。
- Completion Language Policy:
  - 只有代码改动、测试和阶段清理都完成后，才允许说“Wave 1 已落地”。
- Delivery Truth Contract:
  - 本轮完成声明只覆盖 release operator closure，不外推到其他技术债波次。
- Non-goals:
  - 不实施 runtime schema extraction。
  - 不实施 outputs family migration。
  - 不实施 nested mirror 缩减。
- Autonomy Mode: `interactive_governed`
- Inferred Assumptions:
  - 用户已明确允许 XL 并发子代理执行。
  - 当前最优先、最安全的实施对象是 Wave 1。
