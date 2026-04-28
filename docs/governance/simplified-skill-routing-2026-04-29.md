# Simplified Skill Routing Governance Note

Date: 2026-04-29

## Decision

Expert skill routing now has one execution authority:

```text
skill_routing.selected
```

Final usage claims now have one proof authority:

```text
skill_usage.used / skill_usage.unused
```

The public Vibe runtime still has the same six stages. This cleanup changes how selected expert skills enter those stages and how their use is proven.

## Runtime Rule

Selected skills are not suggestions. Every skill in `skill_routing.selected` must be attempted in the governed workflow:

```text
selected -> load full SKILL.md -> bind to task_slice -> record used or unused
```

A skill can be reported as `used` only when it has:

- full `SKILL.md` load evidence, including a content hash;
- artifact impact evidence in a six-stage runtime artifact;
- a matching entry in `skill_usage.used`.

If the skill is selected but not loaded or does not shape artifacts, it remains explicit in `skill_usage.unused`.

## Deprecated Authority

The following fields are legacy-only and cannot drive new execution decisions or final used claims:

- `specialist_recommendations`
- `stage_assistant_hints`
- `specialist_dispatch.approved_dispatch`
- `specialist_dispatch.local_specialist_suggestions`
- `consultation_bucket`
- `promotion_state`
- `primary`
- `stage_assistant`
- `route_authority_candidates`
- `stage_assistant_candidates`

During migration, old runtime data is isolated under `legacy_skill_routing`. It may explain older artifacts, but it is not execution authority.

## Pack Manifest Rule

Pack routing now prefers one candidate surface:

```text
pack.skill_candidates
```

If `skill_candidates` is absent in an old pack, the router may fall back to:

```text
route_authority_candidates + stage_assistant_candidates
```

That fallback is compatibility only. Old pack role lists no longer decide whether a candidate may be selected. When the router keeps old classification for audit, it records it as:

```text
legacy_role
```

Candidate selection is therefore:

```text
skill_candidates -> ranked candidates -> selected skill
```

Positive keyword guards and task boundaries may still block a candidate, but legacy route/stage labels do not.

## JSON Shape

Root runtime packets expose concise current authority:

```text
skill_routing
skill_usage
legacy_skill_routing
```

Root-level `specialist_recommendations`, `stage_assistant_hints`, and `specialist_dispatch` are no longer authoritative runtime surfaces. They remain only under `legacy_skill_routing` while migration tests still need them.

Execution manifests point back to authoritative artifacts through:

```text
skill_routing_path
skill_routing_summary
selected_skill_ids
```

They do not need to copy the full old specialist routing state.

## Verification Evidence

Focused routing and usage tests:

```powershell
python -m pytest tests/runtime_neutral/test_simplified_skill_routing_contract.py tests/runtime_neutral/test_binary_skill_usage_contract.py tests/runtime_neutral/test_binary_skill_usage_runtime_flow.py tests/runtime_neutral/test_runtime_delivery_acceptance.py -q
```

Broader runtime tests:

```powershell
python -m pytest tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_skill_promotion_freeze_contract.py tests/runtime_neutral/test_bundled_stage_assistant_freeze.py -q
```

Pack candidate compatibility tests:

```powershell
python -m pytest tests/runtime_neutral/test_global_pack_consolidation_audit.py tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py -q
python -m pytest tests/runtime_neutral/test_router_bridge.py tests/runtime_neutral/test_python_validation_contract.py -q
python -m pytest tests/unit/test_router_contract_selection_guards.py tests/integration/test_router_core_cutover.py -q
```

Verification gates:

```powershell
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-governed-runtime-contract-gate.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-runtime-execution-proof-gate.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-routing-smoke.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-offline-skills-gate.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
git diff --check
```

## Boundaries

This work does not delete skill directories. Physical deletion remains a separate cleanup step.

This work does not change canonical `$vibe` or `/vibe` entry behavior. Canonical launch evidence is still checked through the canonical session root artifacts.

This work does not claim older runtime artifacts have the new shape. Old artifacts should be interpreted through the compatibility helpers.
