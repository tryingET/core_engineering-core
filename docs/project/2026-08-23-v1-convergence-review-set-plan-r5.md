---
summary: "Final-candidate R5 review-set plan for Decision 128 after R4 left one G0-A3 source-provenance blocker."
read_when:
  - "Reviewing revision 5 of the v1 convergence RFC."
  - "Checking final ADR-readiness review coverage."
type: "review_set_plan"
task_id: 4907
decision_id: 128
artifact_kind: "review_set_plan"
rfc_ref: "docs/rfc/2026-08-23-v1-convergence-contract-r5.md"
rfc_sha256: "d8a17d69b12d9235de75e123acb28362876f0062d504ac45d991cec15736b5e4"
---

# Review Set Plan — engineering-core v1.0 convergence revision 5

## Status

```text
review_kind = re-review after revise_rfc
reviewed_artifact = docs/rfc/2026-08-23-v1-convergence-contract-r5.md
reviewed_SHA256 = d8a17d69b12d9235de75e123acb28362876f0062d504ac45d991cec15736b5e4
outer_host = pi_sdk
AK_active_track = current_track
review_closure_mode = multi_lane_requires_synthesis
intended_effect = closure_candidate
```

R5 is a narrow correction after R4. It authorizes no implementation, acceptance, ADR, candidate, or
release. Any RFC-byte change invalidates this review input.

## Inputs

- exact R5 artifact above;
- problem/evidence notes, vision, product posture, and support policy;
- immutable R2–R4 plans/memos/syntheses;
- AK task `4907`, decision `128`, direction `AK.V5.SF01`;
- governance-kernel decision lifecycle and review-synthesis v6 contract.

## R4 blocker R5 must close

G0-A3 must prove the candidate is the authorized transition, not merely a clean self-consistent tree:

- bind exact base commit/tree;
- bind every reviewed implementation output/task/review digest;
- bind accepted G4 bytes and negative lineage;
- bind frozen population/protocol/template/fixture/oracle/impact/toolchain inputs;
- bind exact candidate task plus content/diff/effect allowlists and target proof channel;
- reject stale, missing, extra, or changed input and rerun the owning stage;
- map every candidate output byte to admitted input or declared deterministic materialization;
- prevent candidate checks from exposing G1–G4 corpora/outcomes; and
- require G0-B to verify tree/base/diff/task/input/output against the admission record.

## Review lanes

1. **Semver/authority:** verify stage binding, A3 admission provenance, exact task/effect boundaries,
   candidate/release separation, manifest timing, v1 baseline, population, and alternatives.
2. **Protocol/federation:** verify the admission record closes stale/unauthorized source routes without
   weakening negotiation, adapters, parser guarantees, downgrade, threats, or oracle timing.
3. **Operator/rendering:** regression-check exact installed artifacts, public runbooks, malformed-input
   boundaries, every-boundary recovery, mixed ownership, scoped resolution, removal, and owner exit.
4. **Empirical validity:** ensure candidate checks remain study-disjoint and cannot leak/capture G3;
   recheck treatment, weighting, models, multiplicity, forecast, harm missingness, safety, and freeze.
5. **Governance/legality:** verify no A3 authority promotion, immutable revision lineage, G4 freedom,
   population ownership, task dependencies, direction, and exact remaining AK steps.

## Outcome rule

The designated synthesis emits `ready_for_adr`, `revise_rfc`, or `reject_current_direction`.
A supported authority/security/testability contradiction controls; no vote or average applies. Missing
future implementation is not a byte-level blocker when an explicit task/gate fails closed.

## Canonical outputs

- `docs/project/2026-08-23-v1-convergence-review-memo-r5.md`
- `docs/project/2026-08-23-v1-convergence-review-synthesis-r5.md`

This plan is attached before synthesis. The fresh synthesis alone may control ADR legality.

## Completion conditions

- all lanes confirm the exact digest and R4 blocker disposition;
- no constitutional regression remains;
- memo and synthesis state quality separately from current AK legality;
- commit/digest binding reaches AK attachment evidence; and
- the passport exposes one controlling closure without session inference.
