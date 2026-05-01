# Binary Skill Usage Routing Governance Note

> Historical / Retired Note: This document records a previous routing design or
> migration state. Current routing authority is defined by
> `docs/governance/current-routing-contract.md` and
> `docs/governance/current-runtime-field-contract.md`.

Date: 2026-04-28

## Decision

Skill usage has only two user-facing states:

- `used`
- `unused`

Only `skill_usage` can support a usage claim.

## Used Standard

A skill is `used` only when:

1. the full `SKILL.md` was loaded,
2. load evidence records `skill_md_path`, `skill_md_sha256`, and `load_status = loaded_full_skill_md`,
3. at least one six-stage artifact impact record exists in `skill_usage.evidence`.

## Non-Authoritative Fields

These fields remain audit data and do not prove usage:

- `specialist_recommendations`
- `stage_assistant_hints`
- `specialist_dispatch.approved_dispatch`
- consultation receipts
- `native_skill_description`

## Runtime Contract

The public six-stage runtime remains unchanged. Binary usage is an internal truth layer written through `skill-usage.json` and surfaced in final delivery acceptance.

## Completion Language

Completion reports may say a skill was used only when `skill_usage.used_skills` contains it and `skill_usage.evidence` supports it.
