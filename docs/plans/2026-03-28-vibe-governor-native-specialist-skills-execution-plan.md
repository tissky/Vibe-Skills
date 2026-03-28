# Vibe Governor + Native Specialist Skills

## Execution Summary
Implement the smallest coherent extension that lets explicit `vibe` runs freeze, plan, and execute native specialist assistance without surrendering runtime authority. Reuse existing router outputs, keep `runtime_selected_skill=vibe`, and add bounded specialist dispatch surfaces to requirement, plan, execution, verification, and documentation.

## Frozen Inputs
- Requirement doc: /home/lqf/table/table5/workspace/issue-57-ai-governance/docs/requirements/2026-03-28-vibe-governor-native-specialist-skills.md
- Source task: `vibe` governor + native specialist skills
- Runtime authority invariant: explicit `vibe` remains the only runtime owner

## Internal Grade Decision
- Grade: XL
- User-facing runtime remains fixed; the grade is internal only.
- Parallel work is warranted because code, tests, and governance docs can advance on disjoint write scopes.

## Wave Plan
- Wave 1: freeze contracts, inspect runtime surfaces, and define specialist recommendation schema
- Wave 2: implement runtime packet, requirement, and plan surfacing
- Wave 3: implement bounded specialist execution accounting and manifest recovery
- Wave 4: update protocol/docs surfaces and operator guidance
- Wave 5: add tests, run verification, and close with cleanup receipts

## Ownership Boundaries
- Runtime packet and artifact contract: `config/runtime-input-packet-policy.json`, `scripts/runtime/Freeze-RuntimeInputPacket.ps1`
- Requirement/plan surfacing: `scripts/runtime/Write-RequirementDoc.ps1`, `scripts/runtime/Write-XlPlan.ps1`
- Execution accounting: `scripts/runtime/Invoke-PlanExecute.ps1`
- Protocol/docs authority model: `SKILL.md`, `protocols/runtime.md`, `protocols/team.md`, supporting docs
- Verification: runtime tests and targeted gates
- Subagent prompts must end with `$vibe`.

## Specialist Skill Dispatch Plan
- Dispatch only bounded specialist units; keep `vibe` as the sole runtime owner.
- Preserve native specialist usage by carrying native workflow expectations, required inputs, expected outputs, and verification mode into the dispatch contract.
- Do not auto-promote specialist recommendations into runtime ownership changes.
- Record all specialist units in execution evidence and recover their outputs into the `vibe` manifest.

## Verification Commands
- `git diff --check`
- `python3 -m py_compile scripts/runtime/*.ps1` is not applicable; instead validate PowerShell syntax via targeted gates and JSON schema checks
- `python3 -m pytest tests/runtime_neutral -k "runtime_input_packet or plan_execute or specialist or requirement or plan"`
- targeted `rg` checks for authority invariants such as `explicit_runtime_skill`, `shadow_only`, `specialist_recommendations`
- repo cleanliness checks and node audit after each wave

## Rollback Plan
- Revert only the governor-specialist change set if authority invariants or regression tests fail.
- Do not revert unrelated user changes or existing untracked docs.
- If specialist execution accounting proves too invasive, fall back to metadata-only surfacing while keeping the new contracts explicit and non-authoritative.

## Phase Cleanup Contract
- Remove temporary logs or scratch files created during each wave.
- Run node audit and clean stale managed node residue when present.
- Leave the repository with only intended source, docs, tests, and proof artifacts.
- Emit a cleanup receipt after verification closure.
