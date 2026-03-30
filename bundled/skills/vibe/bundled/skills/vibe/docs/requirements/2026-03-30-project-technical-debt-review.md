# 项目问题与技术债审查需求

**日期**: 2026-03-30
**目标**: 基于 GitHub 当前最新 `main`（`v2.3.53` / `1a049f1`）对仓库进行一次受治理的结构性审查，识别当前存在的问题、脆弱点与主要技术债，并输出按严重度排序的审查结论。

## Intent Contract

- Goal: 对最新主线代码做一次面向维护性、发布治理、运行时契约与历史产物质量的系统审查。
- Deliverable: 一份带文件/行号证据的技术债审查报告，以及对应的冻结 requirement / execution plan 文档。
- Constraints:
  - 必须基于最新 `main` 的实际仓库内容，不基于历史记忆或过时分支。
  - 结论必须区分“当前缺陷”和“过渡态技术债”，不能把已知迁移中的临时安排误写成未被治理的随机问题。
  - 只做审查，不直接改动产品逻辑或发布新的版本。
- Acceptance Criteria:
  - 产出按严重度排序的 findings，且每条都带明确证据路径。
  - 至少覆盖发布治理、镜像/打包拓扑、runtime 契约传播、历史产物边界、脚本可维护性几个维度。
  - 报告明确哪些是立即风险，哪些是长期技术债。
- Product Acceptance Criteria:
  - 审查结论能够帮助后续规划治理收敛，而不是只给出泛泛评价。
  - 对 release / router / runtime / outputs 这几个高影响平面给出可执行的债务归因。
- Manual Spot Checks:
  - 对照 `git status --short --branch` 与 `git log --oneline --decorate -n 5` 确认审查基线。
  - 对照 `config/version-governance.json`、`scripts/governance/*.ps1`、`scripts/runtime/*.ps1`、`scripts/router/*.ps1`、`docs/releases/*.md`、`config/outputs-boundary-policy.json` 检查关键证据。
  - 对照 `tests/runtime_neutral/*` 判断哪些平面有测试，哪些仍主要依赖人工治理。
- Completion Language Policy:
  - 只有当 findings 已写入报告并附带证据时，才允许使用“已完成审查”表述。
- Delivery Truth Contract:
  - 本次结论以仓库现状与直接可读证据为准。
  - 未执行的 gate 或未跑的全量测试不能被表述为“已验证通过”。
- Non-goals:
  - 不在本轮直接修复技术债。
  - 不重写历史 release notes 内容。
  - 不替用户决定后续治理优先级之外的具体实现方案。
- Autonomy Mode: `interactive_governed`
- Inferred Assumptions:
  - 用户需要的是深入审查与债务归纳，而不是立即实施修复。
  - 本轮最有价值的输出是结构化问题清单，而非表面式仓库概览。
