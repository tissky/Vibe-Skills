# Vibe Governor + Native Specialist Skills

## Summary
Keep `vibe` as the sole governed runtime authority while enabling it to call specialist skills as bounded native assistants. Router output must remain a single canonical routing truth, but explicit `vibe` runs should freeze specialist recommendations that can be consumed by planning and execution without handing control to a second runtime.

## Goal
Implement a minimal-change governed model where:

- `vibe` remains the only runtime owner for requirement freeze, execution planning, execution receipts, verification, and cleanup.
- specialist skills can be recommended, planned, dispatched, and verified as bounded native helpers.
- specialist usage preserves each skill's native workflow expectations rather than flattening the skill into a label.

## Deliverable
A repository change set that adds:

- a frozen runtime packet contract for `specialist_recommendations`
- requirement and plan surfacing for native specialist dispatch
- execution-manifest support for specialist units and their recovery into `vibe`
- protocol and operator documentation for the governor-plus-specialists model
- regression tests and proof artifacts demonstrating authority preservation, stability, usability, and intelligent specialist selection

## Constraints
- Do not change `runtime_selected_skill` away from `vibe` during explicit `vibe` runtime entry.
- Do not create a second router, second requirement surface, second execution-plan surface, or second runtime authority.
- Reuse existing router outputs and runtime artifacts as much as possible; prefer additive contract extensions over structural rewrites.
- Preserve current host adapter boundaries; this task is not a host-entry auto-bridge project.
- Specialist execution must remain bounded and must feed back into `vibe` verification and cleanup surfaces.
- Specialist skills must retain native usage expectations, input contracts, workflow semantics, and validation style when dispatched.

## Acceptance Criteria
- Runtime input packet includes machine-readable `specialist_recommendations` for explicit `vibe` runs without changing `authority_flags.explicit_runtime_skill`.
- Requirement documents surface specialist recommendations and native-usage expectations as frozen inputs.
- Execution plans include an explicit `Specialist Skill Dispatch Plan` section describing bounded specialist use.
- Execution manifests record specialist unit counts, outcomes, and recovery status while keeping `vibe` as runtime owner.
- Protocol docs define the `vibe governor + native specialist skills` model and forbid specialist takeover of runtime truth.
- Tests prove:
  - `vibe` authority is preserved
  - specialist recommendations are frozen and surfaced
  - plan/execute artifacts include specialist dispatch data
  - degraded specialist paths remain explicit and non-authoritative when appropriate

> Fill the anti-drift fields once here. Downstream governed plan and completion surfaces should reuse them rather than restate them.

## Primary Objective
Enable `vibe` to orchestrate specialist skills natively without losing governed runtime authority.

## Proxy Signal
The system freezes specialist recommendations, plans them explicitly, executes them as bounded units, and records them in execution evidence.

## Scope
In scope:
- runtime packet extension
- requirement/plan surfacing
- execution manifest specialist accounting
- protocol and proof documentation
- regression tests and cleanup receipts

Out of scope:
- host auto-interception of every incoming message
- automatic replacement of `vibe` with router-selected specialist skills
- global redesign of the router scoring system
- skill-by-skill metadata rewrites across the entire repository

## Completion
The work is complete when explicit `vibe` runs can preserve runtime authority while still planning and executing native specialist assistance with traceable evidence and passing regression coverage.

## Evidence
- code changes in runtime/config/protocol/test surfaces
- new or updated governed requirement/plan docs
- passing targeted tests
- cleanup receipts and node audit output

## Non-Goals
- Do not make router-selected specialist skills authoritative runtime owners.
- Do not silently downgrade specialist usage into generic text-only hints.
- Do not let any specialist skill create or own a separate execution plan.

## Autonomy Mode
interactive_governed

## Assumptions
- Existing router ranking already provides enough signal to derive specialist candidates without redesigning pack scoring.
- The current runtime packet shadow model can be extended rather than replaced.
- Specialist dispatch can first land as governed execution metadata and bounded units before any future deeper automation.

## Evidence Inputs
- Source task: implement `vibe` governor + native specialist skills with minimal framework change
