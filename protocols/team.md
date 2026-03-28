# vibe-team Protocol

Protocol for XL-grade multi-agent tasks requiring coordination.

## Governed Runtime Position

This protocol is the XL execution topology used inside runtime stage 5 `plan_execute`.
It is not a separate user entrypoint.

The fixed user-facing runtime path remains:

1. `skeleton_check`
2. `deep_interview`
3. `requirement_doc`
4. `xl_plan`
5. `plan_execute`
6. `phase_cleanup`

This protocol only activates after the requirement and plan are already frozen.

## Scope
Activated for XL grade tasks that require:
- Multiple agents working in parallel
- Workflow-based execution with phases
- Swarm or hive-mind coordination
- Long-running iterative tasks

## Hybrid Architecture: Codex Native Team + ruflo Collaboration

Codex native agent APIs manage lifecycle + task assignment (primary path).
ruflo remains optional for workflow/memory enhancements.

All spawned subagent prompts must end with `$vibe` so the governed runtime remains the active contract inside delegated work.

## Root/Child Authority Model

XL delegation uses two governance scopes:

- `root_governed`: one lane per user task; owns canonical requirement/plan truth and final completion claims
- `child_governed`: delegated lane; inherits frozen context and emits local execution evidence

Child-governed lanes keep `vibe` discipline but are not new top-level governors.

Child-governed lanes must not:

- create a second canonical requirement surface
- create a second canonical execution-plan surface
- emit final completion claims for the full root task
- self-approve new global specialist dispatch

### Role Division

| Concern | Provider | Tool |
|---------|----------|------|
| Agent spawning | Codex native | `spawn_agent` |
| Task assignment & follow-up | Codex native | `send_input` |
| Agent synchronization | Codex native | `wait` |
| Agent shutdown | Codex native | `close_agent` |
| Workflow definition (optional) | ruflo | `workflow_create`, `workflow_execute` |
| Vector memory (optional) | ruflo | `memory_store`, `memory_search` |
| Session persistence (optional) | ruflo | `session_save`, `session_restore` |
| Consensus algorithms (optional) | ruflo | `hive-mind_consensus` |

## Anti-Drift Handoff Contract

Every XL subtask handoff should preserve:

- the primary objective,
- the declared scope,
- the current completion-state target,
- any report-only anti-drift warnings already known,
- whether the work is a bounded specialization or a generalized capability claim.

Lead-agent rules:
- subagents may surface report-only warnings, but must not invent a new hard gate,
- if an existing approved policy or failed gate truly blocks progress, cite that exact surface,
- aggregation must not flatten bounded-specialization outputs into generalized completion claims.
- when a specialist skill is dispatched, keep its native workflow intact instead of rewriting it into generic lead-agent prose.
- only root-governed aggregation may publish final completion claims for the full task.

## Native Specialist Dispatch

Within XL execution, a specialist skill is a bounded helper, not a replacement runtime.

Rules:

- `vibe` keeps final control of stage order, plan authority, and completion claims
- specialist dispatch should be declared in the frozen plan before execution
- each specialist receives a bounded subtask contract plus the frozen requirement context
- specialist outputs must stay in the native format or workflow expected by that specialist skill
- lead aggregation may summarize specialist output, but must not erase specialist-specific verification notes
- a specialist recommendation is advisory until the governed plan chooses to dispatch it

Hierarchy-specific dispatch semantics:

- `approved_dispatch`: specialist usage approved by root and frozen in plan; child lanes may execute directly
- `local_suggestion`: child-lane specialist suggestion; advisory until explicit root escalation approval

Escalation rule:

- child lanes needing non-approved specialists must emit explicit escalation evidence to root
- no silent specialist activation is allowed in child lanes

## Orchestration Options

### Option A: Codex Native Team + ruflo Collaboration (Preferred)
1. Define decomposition plan (owners + interfaces + deliverables)
2. Spawn agents via `spawn_agent` with role-specific prompts
3. Assign work and clarifications via `send_input`
4. Store intermediate state via ruflo `memory_store` (milestone summaries, handoff artifacts)
5. Use ruflo `workflow_create` / `workflow_execute` when explicit step orchestration is needed
6. Synchronize via `wait` at each milestone
7. Use ruflo `hive-mind_consensus` when formal consensus is required
8. Aggregate and reconcile outputs in lead agent/context
9. Close agents via `close_agent`

### Option B: Codex Native Team Only (When ruflo Unavailable)
1. Run native lifecycle only: `spawn_agent` → `send_input` → `wait` → `close_agent`
2. Use runtime-neutral state_store + conversation context for milestone state
3. Keep the same staged confirmations and validation gates

### Option C: Ralph-loop (Iterative Tasks)
When task requires repeated iteration on same prompt:
1. User explicitly invokes /ralph-loop
2. Choose engine:
   - `compat` (default): local state loop, manual `--next`, stable and low-dependency
   - `open`: delegates to external open-ralph-wiggum CLI for auto-iteration
3. Define completion promise (exit condition)
4. Set max iterations (safety limit)
5. For `open` engine, prefer no-commit mode during active loop and run VCO quality gates before any manual commit

IMPORTANT: Ralph-loop is MUTUALLY EXCLUSIVE with active team orchestration.

## Agent Type Selection

| Role | Native Agent Type | Notes |
|------|-------------------|-------|
| Researcher | `explorer` | Read/search-heavy investigation |
| Planner | `default` | Planning + decomposition |
| Implementer | `worker` | Implementation ownership with isolated scope |
| Reviewer | `worker` or `default` | Review prompt enforces bug/risk-first output |
| Security | `worker` or `default` | Security-focused prompt and checklist |

## Team Templates
See references/team-templates.md for predefined compositions:
- feature-team, debug-team, research-team, review-team, full-stack-team
- supervisor-scatter-gather (Agent-Squad-style Supervisor + Specialists)
- dialectic-design

If `local-vco-roles` is installed, you may also use:
- local-vco-dialectic-review (Template 7)
- Role prompts sourced from the installed skills root resolved from `CODEX_HOME` when set, otherwise the host default Codex home (commonly `~/.codex`)

## Supervisor-Style Dispatch Pattern (Agent-as-Tools)

Agent Squad's `SupervisorAgent` uses an "agent-as-tools" model: a lead agent fans out tasks in parallel, then fuses results with a bounded shared memory (`<agents_memory>`).

In VCO XL, the equivalent primitive is:

```
spawn_agent × N → send_input (fan-out) → wait (fan-in) → close_agent
```

### Scatter-Gather Fan-out/Fan-in (Agent Squad `send_messages`)

Agent Squad provides a single built-in tool (`send_messages`) that takes an array of `{recipient, content}` and executes the fan-out in parallel, then returns gathered responses.

In VCO XL, keep the same *contract shape*, but implement it with native team primitives:
- **Fan-out**: `send_input` to each agent (one subtask per role/agent)
- **Fan-in**: one `wait` barrier per milestone
- **Gather**: Lead updates `<agents_memory>` once per milestone (not continuously)

Rule of thumb: **one milestone == one scatter-gather round**.

### Dispatch Envelope (Recommended)

When using `send_input`, wrap each subtask in a small envelope so that reliability + memory become mechanical (instead of ad-hoc).

```yaml
run_id: "{yyyy-mm-dd}#{short}"
phase: "plan|investigate|implement|verify"
owner: "{role_name}"
deadline_minutes: 15
retry_budget: 1
deliverable:
  format: "markdown"
  sections: ["summary", "evidence", "risks", "next_steps"]
memory:
  private_key: "team/{run_id}/agent/{owner}/notes"
  shared_key: "team/{run_id}/shared/agents_memory"
```

Notes:
- Keep `deliverable.sections` stable so Lead can aggregate quickly.
- `private_key` is per-agent; `shared_key` is the only cross-agent memory.

### Task Contract (Subtask Interface / DoD)

The dispatch envelope is *transport*. The task contract is *correctness*.

Before fan-out, each subtask SHOULD include a compact contract so specialists do not drift or guess:

```yaml
task_id: "T-1"
goal: "One-sentence, testable outcome"
scope:
  in: ["Allowed modules/files/APIs"]
  out: ["Explicit non-goals"]
inputs:
  - "Facts, constraints, and required context"
outputs:
  - "Artifacts (file paths) or result shape"
definition_of_done:
  - "Acceptance criteria (verifiable)"
verification:
  - "Commands/tests/checks to run"
handoff_questions:
  - "Missing info that must be confirmed by user/lead"
status: "todo|doing|blocked|done"
```

Contract rules:
- Prefer `verification` that is command-shaped (copy/paste runnable).
- If required info is missing, return `status=blocked` with `handoff_questions` (do not guess).
- The same contract maps cleanly to the GSD wave contract (`entry_criteria`/`exit_criteria`/`verify_commands`).
- If the subtask is owned by a specialist skill, keep the contract narrow enough that native specialist workflow still applies without improvising a new method.

## Shared Memory Contract (3-Tier)

To keep XL coordination coherent while avoiding context bloat, treat memory as three tiers:

1. **User ↔ Lead memory**: the main conversation (source of truth for user intent + decisions).
2. **Lead ↔ Agent private memory**: per-agent working notes (NOT broadcast by default).
3. **Shared agents memory**: a bounded, continuously refreshed "what we know so far" block owned by Lead.

Mapping to Agent Squad terminology:
- **User ↔ Lead memory** ≈ User-Supervisor Memory
- **Lead ↔ Agent private memory** ≈ Supervisor-Team Memory
- **Shared agents memory** ≈ Combined Memory (`<agents_memory>`)

Bounded history rule (pair-safe):
- Cap per-agent private history (e.g., last 10–20 message pairs).
- When trimming, preserve complete user/assistant pairs (avoid orphan half-turns).

### Shared Memory Format (Supervisor-style)

Lead maintains a rolling block (in conversation context, or via ruflo `memory_store` when available):

```text
<agents_memory>
[run_id] phase=investigate
- (Investigator-1) key finding: ...
- (Implementer-2) patch plan: ...
- Open questions: ...
- Next milestone: ...
</agents_memory>
```

Rules:
- Update only at milestone boundaries (after `wait`), not on every message.
- Prefer facts + artifacts over prose. Link to file paths or commands when applicable.
- Hard cap: if it grows beyond what can fit comfortably in-context, summarize and overwrite (do not append forever).

## Reliability & Failure Handling (Timeout + Retry Budget)

Borrowing from Agent Squad's orchestration patterns (bounded history, explicit error messages), XL teams should treat failures as first-class:

1. **Timeout**
   - If an agent misses its `deadline_minutes`, send one reminder via `send_input`.
   - If still no response: proceed with partial results and record the missing deliverable in `<agents_memory>`.

2. **Retry**
   - Respect `retry_budget`. A retry must change *something* (prompt constraint, narrower scope, more context, or a different role).
   - If retry budget is exhausted: either degrade scope or respawn a replacement agent with a simplified task, but only with an explicit hazard alert and a non-authoritative status.

3. **Contradiction**
   - When two agents disagree, Lead runs V2/V6: demand concrete evidence (file path, log line, command output) before choosing.

4. **Degraded Mode**
   - If multiple agents fail or outputs are low-quality, do not silently fall back to Option B (native only). Any degraded path must emit a standalone hazard alert, reduce parallelism deliberately, and mark the result non-authoritative until the primary path is restored.

## Staged Confirmation
Always confirm with user at these points:
1. After workflow definition (before spawning agents)
2. After each major phase completion
3. Before final integration of results
4. Before committing changes

Mode-aware interpretation:
- `interactive_governed`: the four confirmation points above remain user-visible by default
- `benchmark_autonomous`: replace interactive pauses with explicit receipts unless a blocking ambiguity, scope breach, or safety boundary is hit

## GSD-Lite Wave Contract Hook (Optional)

Policy source: `config/gsd-overlay.json`

When `enabled=true`, `mode != off`, and `wave_contract.enabled=true`, apply this hook as orchestration metadata only.

Activation:
- XL planning: enabled by default
- XL coding: enabled when the lead expects dependency-sensitive multi-wave execution
- If `wave_contract.xl_only=true`, never run for M/L

Contract output:
- Generate `waves.json` (or configured artifact) with:
  - `wave_id`
  - `units` (task ids / owners)
  - `depends_on`
  - `entry_criteria`
  - `exit_criteria`
  - `verify_commands`

Execution semantics:
1. Independent units run in parallel within a wave.
2. Waves run sequentially by dependency.
3. Verification gates must pass before advancing to next wave.
4. This contract does not alter grade/task assignment.

Failure semantics:
- If wave contract generation fails or is incomplete, do not silently fall back to standard Option A/B orchestration. If a degraded path is used, emit a standalone hazard alert and record that the resulting execution is non-authoritative.
- Do not block the entire XL flow unless strict policy explicitly requires a regenerated contract.

## Quality Injection: Enhanced Tier (XL Default)

In addition to Core Tier (P5, V2, V7 + task-type-specific from vibe-do):

### Additional Enhanced Patterns
- **P2**: Effort Allocation. 验证阶段的投入应与执行阶段相当，不可跳过。顺序：理解 → 规划 → 执行 → 验证，每阶段都应有明确产出。
- **P6**: PDCA Cycle. Plan -> Do -> Check -> Act. Never retry without understanding WHY it failed.
- **V4**: Red Flags Self-Check. REJECT: "Quick fix for now", "Just try changing X", "Might work".
- **V5**: Rationalization Blocker. "Should work now" -> demand verification. "I am confident" -> confidence != evidence.
- **V6**: Agent Trust-But-Verify. After agent returns: check VCS diff independently, run verification, compare claim vs evidence.

### XL Injection Matrix

| Task Type | Pre-Injection | Post-Validation |
|-----------|--------------|-----------------|
| Planning | P3, P5, P6 | V2, V5, V6, V7 |
| Coding | P5, P6 | V2, V3, V5, V6, V7 |
| Review | P3, P5 | V2, V5, V6, V7 |
| Debug | P1, P4, P5, P6 | V2, V4, V5, V6, V7 |
| Research | P2, P3, P5, P6 | V1, V2, V5, V6, V7 |

## Dialectic Mode

Structured multi-perspective design analysis. Activated only when user explicitly requests dialectic think-tank mode (`dialectic_team_requested = true`).

### When to Use

- Multiple viable architectural approaches with unclear trade-offs
- High-stakes design decisions where blind spots are costly
- User explicitly requests "使用辩证智囊团", "启用辩证智囊团", "`$vibe dialectic`", or "dialectic-design"

### Not For

- Implementation tasks (use standard coding flow)
- Single correct answer questions (use sc:research)
- Trivial design choices (use think.md B2 Self-Check instead)
- Debugging (use debug-team template)

### XL Execution (Codex Native Team)

Uses dialectic-design template from team-templates.md.

**Step 1 — Prepare context**
Lead reads relevant code/docs, formulates the design question, selects perspective pair from team-templates.md Perspective Assignment table.

**Step 2 — Create team**
```
spawn_agent × 4: one per thinker agent
```

**Step 3 — Send role prompt template**
Each agent receives this prompt (Lead fills `{placeholders}`):

```
你是 {role} ({group} 组)。

设计问题：{question}

你的分析视角：{perspective}
上下文材料：{context_slice}

执行 6 阶段工作流：
1. Propose: 基于你的视角，独立提出一个完整方案（含架构、关键决策、风险）
2. Reflect: 列出你方案的 3 个最可能的生产环境失败模式
3. Synthesize: 基于自我批判改进方案 → 通过 send_input 发给组内伙伴
4. Compare: 收到伙伴方案后，分析两个方案的核心分歧点
5. Reflect on comparison: 伙伴看到了什么你遗漏的？为什么会产生分歧？
6. Final synthesis: 整合伙伴洞察，产出最终方案 → 通过 send_input 发给 Lead

输出格式（Phase 6）：
- 方案摘要（≤200字）
- 关键决策 + 理由（列表）
- 已知风险 + 缓解策略
- 从伙伴方案吸收的要素
```

**Step 4 — Context isolation**
Group A receives context slice emphasizing perspective A's concerns.
Group B receives context slice emphasizing perspective B's concerns.
Groups do NOT share context or communicate cross-group.

**Memory note (keep isolation real)**
- Do NOT maintain a single shared `<agents_memory>` while groups are executing.
- If you need rollups, keep **two separate blocks** (Group A only / Group B only) owned by Lead, and merge only after Step 6.

**Step 5 — Execute**
4 agents run 6-phase workflow. Intra-group communication via `send_input` (A1↔A2, B1↔B2). Max 1 round.

**Step 6 — Collect**
Lead waits for 4 Phase-6 outputs.

**Step 7 — Timeout handling**
If any agent does not respond within reasonable time:
- Send reminder via `send_input`
- If still no response: proceed with available outputs (minimum 2 from different groups)
- If <2 outputs: abort dialectic, fall back to think.md B2 Self-Check

**Step 8 — Output processing**
Lead analyzes 4 final syntheses:

```
1. Extract consensus: 所有方案一致同意的决策点
2. Extract divergence: 方案间的核心分歧 + 每方的论据
3. Identify blind spots: 某组发现而另一组完全未提及的风险/机会
4. Synthesize: 产出综合方案（consensus 为基础 + divergence 中选择最优 + blind spots 纳入风险清单）
5. Present to user:
   - 综合方案
   - 关键分歧点 + 各方论据（供用户决策）
   - 风险清单（含 blind spot 来源标注）
```

**Step 9 — User decision**
Present synthesis to user. User may:
- Accept synthesis as-is → proceed to implementation
- Choose one group's approach → proceed with that direction
- Request deeper analysis on specific divergence point

**Step 10 — Shutdown**
Close all 4 agents via `close_agent`.

### L-Grade Adaptation

L grade does not run XL team orchestration. Use 2 native agents sequentially:

```
1. Agent-A: spawn_agent(agent_type="default" or "worker", prompt="{question} 从 {perspective_A} 视角分析")
2. Agent-B: spawn_agent(agent_type="default" or "worker", prompt="{question} 从 {perspective_B} 视角分析")
3. Lead synthesizes both outputs using the same output processing algorithm (Step 8)
```

Limitations vs XL: no intra-group dialogue (only 1 agent per perspective), no Phase 3-5 refinement. Suitable for moderate-complexity design decisions.

### Integration with think.md

- If `dialectic_team_requested = true` AND grade = L/XL → skip think.md B2 Self-Check, use Dialectic Mode instead
- If `dialectic_team_requested = true` AND grade = M → use think.md B2 Self-Check (team dialectic is overkill for M)
- Dialectic Mode output feeds into writing-plans as the design foundation

## Conflict Avoidance
- Do NOT use Everything-CC agents as the primary XL executor (use Codex native team)
- Do NOT use Superpowers subagent-driven-dev for XL tasks
- Ralph-loop and active team orchestration are mutually exclusive
- Only one team active per project at a time
- Prefer native agent communication via `send_input`
- Do NOT bypass runtime stage 6; XL execution must still hand off into `phase_cleanup`

## BrowserOps / DesktopOps Governance Hooks

在 Wave24–30 之后，XL 团队执行涉及真实浏览器或 open-world GUI 任务时，必须额外遵守以下边界：

- BrowserOps 只通过 provider policy 建议 `API / Playwright / Chrome / TuriX-CUA / browser-use`，不得绕开 VCO 主路由。
- DesktopOps 只允许以 `shadow/advisory/contract` 形式吸收 `Agent-S` 思路，不得把任何外部桌面代理提升为默认执行 owner。
- 若 BrowserOps / DesktopOps 建议与主计划冲突，优先服从 `references/conflict-rules.md` 与 cross-plane conflict policy。
- 进入 soft/strict 之前，必须能提供对应 gate 与 rollback command。

相关资产：
- `docs/browserops-provider-integration.md`
- `docs/agent-s-shadow-integration.md`
- `docs/cross-plane-conflict-governance.md`
- `docs/promotion-board-governance.md`

## Wave19-30 Specialist Roles

在 XL 多智能体执行中，Wave19-30 新增以下“治理型角色”，它们提供建议与验证，不接管 VCO 总编排：

- **Memory Contract Steward**：检查 Memory Runtime v2、`mem0`、`Letta` 是否越权。
- **Prompt Intelligence Steward**：检查 prompt cards / risk checklist 是否只停留在 advisory 层。
- **BrowserOps Provider Steward**：负责 provider candidate 建议与 browser contract 校验。
- **DesktopOps Shadow Steward**：负责 ACI/open-world 合同化，不允许默认 takeover。
- **Promotion Board Steward**：负责 rollout evidence、blocking findings、rollback plan 汇总。

团队规则：
1. 治理型角色不能直接替代 implementer / reviewer / router。
2. 任何角色给出的 promote 建议都必须经过 promotion board gate。
3. 子代理的文件写入范围必须提前切分，避免互相覆盖。
