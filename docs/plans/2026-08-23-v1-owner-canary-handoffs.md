---
summary: "Bounded owner-canary handoffs and the v1 proof-population manifest draft for G0-A2 admission; every participant action remains owner-authorized."
read_when:
  - "Preparing or accepting the qualification-population decision for v1 convergence."
  - "Acting as a participant owner deciding whether to accept a v1 proof role."
type: "implementation-plan"
---

# v1 owner-canary handoffs and proof population

Controlling contract: `docs/rfc/2026-08-23-v1-convergence-contract-r5.md`
(Qualification population), accepted as
`docs/adr/2026-08-23-v1-convergence-contract.md`.
Manifest: `docs/project/v1-proof-population.json`.

## Manifest digests (draft revision 1)

- Canonical (RFC 8785 JCS) SHA-256:
  `2f1bc660fcf9a73999b46584208b9eae23a9ebf4969e5f418f87738a8e0b6e09`
- Raw transport SHA-256:
  `7090ad2f329c61c03058587ff2ebab9937cad8d92f4feed52ce993ca88181ce8`
- Byte length: 6973

The manifest contains only strings, integers, booleans, and null, so JCS equals
sorted-key compact UTF-8 JSON. Every G1–G5 artifact must record the canonical digest of
the accepted revision. A changed population requires an accepted decision revision and a
new manifest digest.

## Population shape

Four positive baselines across three independently governed owner groups (TeachingCo's
two baselines count as one group), covering the constitutional cases: existing-adopter
transition (HoldingCo), historical clean-slate adoption at the RFC-pinned revision
(TeachingCo/wib `316c457…`), small transition/portability/rollback/removal
(TeachingCo/mathe), and heterogeneous package-boundary federation (SoftwareCo). One
truthful untouched negative control (HealthCo) completes the shape.

## Owner handoff packets

Each participant owner is asked to accept — inside its own repository and its own AK
task, never through engineering-core — exactly one bounded role:

| Owner | Ask | Must record before G0-A2 admission |
|---|---|---|
| HoldingCo | `pos-1` existing-adopter transition and governed-lifecycle canary | exact owner task id, pinned revision refresh, declared validation commands, baseline state, evidence custody, transfer policy, isolation and rollback boundaries, final proof-workspace posture |
| TeachingCo | `pos-2` small-transition/portability canary and `pos-3` historical clean-slate canary at the pinned revision | same record per baseline; separate tasks recommended |
| SoftwareCo | `pos-4` heterogeneous transition/federation canary | same record |
| HealthCo | negative-control **notice only**: repo stays untouched, read-only observation, no adoption mutation | acknowledgement reference; no execution task |

The ask is bounded: disposable-replica journey work under the G1 protocol
(`docs/plans/2026-08-23-v1-dependable-adoption-proof.md`), opt-in G4-A pilot candidacy,
or read-only observation. No owner is asked to adopt v1 as a production dependency, and
no owner acceptance is inferred from silence, inactivity, or this document.

## Stop conditions

Stop and route to the population decision on: any owner refusal; inability to bind a
full immutable revision; active conflicting task claims; or a baseline becoming
unsuitable. Missing, stale, conflicting, or unknown state blocks execution rather than
being repaired from this manifest.

## Non-authorizations

- No shadow execution tasks exist in engineering-core for participant work.
- No participant repository has been mutated; revisions above are read-only observations.
- No adoption, rollout, or capability claim follows from manifest membership; entries
  are bounded routing references, not participant capability proof.
- The accepted qualification-population decision — replacing this draft — remains open
  owner work under decision 128's G0-A2 preconditions.

## Rollback

Withdrawal of any participant before population-dependent evidence creates a fresh
accepted population decision preserving every constitutional property, records the
reason and exact owner task, and restarts affected evidence. This draft can be
superseded without touching any owner record.
