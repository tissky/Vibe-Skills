# 非退化技术债修复规划需求

**日期**: 2026-03-30
**目标**: 基于 `v2.3.53` 当前主线技术债审查结果，规划一条“功能不出问题、行为不退化、发布/安装/验证链路不弱化”的修复路线，明确修复顺序、分批策略、兼容期、验证要求与 stop rules。

## Intent Contract

- Goal: 设计一套可执行的技术债修复路线，而不是直接做高风险的大爆炸式重构。
- Deliverable: 一份受治理的修复规划文档，明确优先级、分 wave 的实施顺序、每波需要的 proof、回滚边界与完成标准。
- Constraints:
  - 不能以“仓库更整洁”为理由牺牲 routing、release、install、runtime、verify 的现有行为。
  - 必须优先选择 dual-read / dual-write、compatibility window、characterization tests 等低风险迁移路径。
  - 不允许把多个高风险结构改造捆绑到同一批次。
  - 规划必须区分“先补护栏”和“再做收敛”，不能先删后证。
- Acceptance Criteria:
  - 规划覆盖前一轮审查识别出的主要技术债：镜像拓扑、release automation、runtime contract drift、outputs 边界、release truth surface、超大脚本可维护性。
  - 每个债务项都给出推荐修复方式、依赖顺序、验证方式和禁止操作。
  - 明确指出第一批最适合落地的修复动作。
- Product Acceptance Criteria:
  - 规划执行后，仓库应朝着“单一真源、更少人工同步、更少手工字段映射、更清晰生成物边界”收敛。
  - 但在每个阶段，用户可见能力和 release/install/runtime 结果语义必须保持稳定。
- Manual Spot Checks:
  - 对照前一轮技术债报告，确认每个 finding 都有对应的修复策略。
  - 对照现有 gates / tests，确认哪些可以直接复用，哪些必须先新增。
  - 对照 `release-cut.ps1`、`sync-bundled-vibe.ps1`、runtime packet / manifest 生成逻辑，确认规划顺序没有反过来制造更大的迁移风险。
- Completion Language Policy:
  - 只有 requirement 和 plan 都冻结完成后，才允许说“修复路线已规划完成”。
  - 在未实际实施前，只能说“建议修复方案/执行计划”，不能说“问题已修复”。
- Delivery Truth Contract:
  - 规划必须以当前仓库结构、现有 gate 和现有测试边界为依据。
  - 对未来将新增的 gate / tests / helper，只能写成“应新增”，不能假装已经存在。
- Non-goals:
  - 本轮不直接执行代码改动。
  - 本轮不承诺一次性清空全部技术债。
  - 本轮不把大重构包装成“轻量 cleanup”。
- Autonomy Mode: `interactive_governed`
- Inferred Assumptions:
  - 用户要的是可靠的修复路线，而不是立刻进入高风险重构。
  - 最合理的策略是先强化 proof surfaces，再推进结构收敛。
