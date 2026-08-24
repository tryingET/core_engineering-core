---
summary: "Accepted v1 proof-population manifest revision 2: four positive baselines across three owner groups plus the untouched HealthCo negative control, bound to participant owner tasks 4931-4935."
read_when:
  - "Executing or reviewing v1 Gate G0-A2 admission, G1 journeys, or any population-dependent proof."
  - "Changing, replacing, or re-digesting the qualification population."
type: "adr"
---

# ADR — Freeze the v1 qualification population (manifest revision 2)

## Status

Accepted under decision `131` (local tier). Supersedes the unbound revision-1 draft.

## Decision

Freeze `docs/project/v1-proof-population.json` **revision 2** as the immutable
population input for one protocol/candidate revision of engineering-core v1.0
qualification:

- Canonical (RFC 8785 JCS) SHA-256:
  `50eb98aaf4b927f642530e3dc5f9cb15c0409a9f2f57426e1bb86c382d32d5c3`
- Raw transport SHA-256:
  `af7b605bf708cc8be0dd1788df962436eea0cea19dd8173501911532644d79e0`
- Byte length: 7479

Population: HoldingCo `fcos-control-board` (pos-1, existing-adopter transition),
TeachingCo `mathe` (pos-2, small transition/portability), TeachingCo `wib` at RFC pin
`316c457…` (pos-3, historical clean-slate), SoftwareCo `pi-extensions` (pos-4,
heterogeneous federation/package boundary), plus HealthCo `agents` as the untouched
read-only negative control. Constitutional shape: ≥3 independent positive owner groups,
≥4 baselines, all required cases present; engineering-core is not a positive adopter;
TeachingCo's two baselines count as one group.

Participant enrollment is bound to exact scoped owner tasks created in each owning
repository: 4931 (HoldingCo), 4932/4933 (TeachingCo), 4934 (SoftwareCo),
4935 (HealthCo notice-only acknowledgement), authorized by the operator on 2026-08-24.
Enrollment is administrative; **proof independence is earned at execution time** — each
owner still runs its own journeys, validations, dispositions, and rollbacks under its
own task, and no result, receipt, or adoption may be inferred from this enrollment.

## Consequences

- Every G1–G5 artifact must record this manifest's canonical digest; every run
  re-resolves live AK and owner state, and missing/stale/conflicting state blocks rather
  than repairs from the manifest.
- Participant decline or unsuitability requires a fresh accepted population decision
  preserving constitutional properties, restarts affected evidence, and yields a new
  digest. Silent or post-result substitution invalidates G1–G5.
- Changing a constitutional property reopens the governing RFC (decision 128).

## Rollback

This decision supersedes only the unbound revision-1 draft; no participant repository
was mutated by enrollment, so withdrawal restores nothing beyond task state. The
revision-1 digests remain recorded in the handoff document as history.
