---
summary: "Problem brief for the Decision 128 revision chain: make Model A decision-grade without pre-v1 compatibility or accidental proof-tool coupling."
read_when:
  - "Reviewing Decision 128 or preparing its ADR."
  - "Checking why the first convergence RFC required revision."
type: "brief"
decision_id: 128
task_id: 4907
---

# Problem Brief — engineering-core v1.0 convergence revision chain

## Status and authority

This is the Tier 1 problem brief for AK decision `128`, produced under task `4907`.
It frames a revised proposal; it does not accept Model A, record an ADR, authorize implementation,
mutate a participant repository, create a candidate, or release v1.0.

Current runtime truth at authoring:

```text
decision:128 = review_pending
ADR = absent
legal_review_closure = absent
current execution task = 4907
latest stable release = v0.10.0
```

## Trigger

The first reviewed RFC made the four maturity pillars cumulative, repaired its gate order, and
preserved owner authority. Subsequent multi-domain review exposed a deeper ambiguity: the document
claimed to freeze a public v1 contract while deferring the classification of its public interfaces,
and it mixed a semver constitution with one proof campaign.

The operator then clarified the key product constraint:

> v1.0 does not need backward compatibility with pre-v1 package releases.

That removes an accidental burden, but the RFC bytes still required pre-v1 upgrades, old released
inputs, and an older compatible consumer. A verbal clarification cannot override normative `MUST`
or PASS language.

## Problem statement

Decision 128 cannot lawfully or safely reach ADR while the proposal leaves these questions unresolved:

1. **What becomes stable?** The public v1 core, owner adapters, pilot surfaces, and internal proof
   tooling were not classified before the decision.
2. **What does the clean break mean?** Pre-v1 package behavior may break, while existing versioned
   protocol identifiers have independent meaning and cannot silently reset at package `1.0.0`.
3. **What must an operator actually do?** A participant-selected harness could stand in for public
   transition, recovery, rollback, removal, and rendered documentation.
4. **What is evidence versus constitutional law?** G3 embedded unsupported numeric thresholds and
   G2 embedded ungrounded resource constants rather than requiring prospectively accepted protocols.
5. **Can owner decisions remain free?** G4 disclaimed coercion while requiring a predetermined mix
   of promotion, rejection, revision, and rollback outcomes.
6. **What makes ADR progression legal?** AK lacks the required problem/evidence/review attempt and
   controlling synthesis chain for the revised artifact.

## Decision-grade target

A successful revision must preserve Model A while establishing a two-layer contract:

- a stable public v1 constitution with a clean pre-v1 break and compatible v1.x semantics; and
- prospectively governed qualification protocols whose fixtures, thresholds, adapters, and release
  machinery do not become public APIs merely by existing in the repository.

It must also require candidate-shipped operator journeys, canonical v1 federation boundaries,
justified empirical protocols, and non-coercive lifecycle evidence.

## Non-goals

- Implementing the future compatibility manifest, adapters, validators, transition commands, study,
  lifecycle suite, or release workflow.
- Promising compatibility with any v0 package release.
- Weakening privacy, hostile-input, custody, rollback, removal, owner-exit, or release-lineage controls.
- Accepting the decision or drafting the ADR under task `4907`.

## Decision questions

1. Should Model A remain the v1 release constitution once pre-v1 compatibility is removed?
2. Does the revised stable/public/internal/adapter classification sufficiently constrain G0-A2?
3. May exact empirical and resource thresholds live in separately accepted prospective protocols?
4. Can deterministic transition conformance replace quotas over substantive live-owner outcomes?
5. Is the revised contract precise enough for a fresh `ready_for_adr` review closure?

## Linked evidence

- `docs/project/2026-08-23-v1-convergence-evidence-note.md`
- `docs/rfc/2026-08-23-v1-convergence-contract.md` (historical revision)
- `docs/rfc/2026-08-23-v1-convergence-contract-r2.md` and its `revise_rfc` review artifacts
- `docs/rfc/2026-08-23-v1-convergence-contract-r3.md` and its `revise_rfc` review artifacts
- `docs/rfc/2026-08-23-v1-convergence-contract-r4.md` and its `revise_rfc` review artifacts
- `docs/rfc/2026-08-23-v1-convergence-contract-r5.md` (current proposal)
- `docs/project/2026-08-23-v1-convergence-review-set-plan-r5.md`
