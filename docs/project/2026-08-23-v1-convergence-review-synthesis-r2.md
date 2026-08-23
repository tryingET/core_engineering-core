---
summary: "Controlling synthesis for Decision 128 revision 2: Model A remains viable but the RFC requires revision 3."
read_when:
  - "Checking the controlling outcome of the R2 convergence review set."
  - "Tracing why Decision 128 advanced from R2 to R3 rather than ADR."
type: "review_synthesis"
task_id: 4907
decision_id: 128
artifact_kind: "review_synthesis"
review_outcome: "revise_rfc"
reviewed_artifact: "docs/rfc/2026-08-23-v1-convergence-contract-r2.md"
reviewed_sha256: "93f6060d6fab2af7b0b39b4dd0d998592ce0c9a7610f7b42b701f396986c24a5"
---

# Review Synthesis — engineering-core v1.0 convergence revision 2

## Status

```text
review_closure_mode = multi_lane_requires_synthesis
reviewed_artifact = docs/rfc/2026-08-23-v1-convergence-contract-r2.md
reviewed_SHA256 = 93f6060d6fab2af7b0b39b4dd0d998592ce0c9a7610f7b42b701f396986c24a5
review_outcome = revise_rfc
legal_next_move = revise_rfc_with_fresh_review_set
ADR_legal_from_R2 = false
```

Inputs:

- `docs/project/2026-08-23-v1-convergence-review-set-plan-r2.md`
- `docs/project/2026-08-23-v1-convergence-review-memo-r2.md`
- execution evidence `dispatch-1787524357077`, `dispatch-1787524357079`,
  `dispatch-1787524357081`, `dispatch-1787524357083`, and `dispatch-1787524357085`

This synthesis is review closure for R2 only. It authorizes no ADR, implementation, participant
mutation, candidate, release, or publication.

## Controlling judgment

Model A survives review. The clean pre-v1 break, cumulative pillars, authority split, prospective
empirical ownership, and non-coercive G4 direction are coherent. Rejection is not justified.

ADR progression is nevertheless blocked because every lane found at least one concrete contract
defect. The defects cluster around five architectural seams:

1. **Freeze order:** public manifests cannot be finalized before G4-A if G4-A can change public content.
2. **Compatibility enforcement:** enumeration is not enough; every stable item needs a normative
   source, executable assertion, and future-v1.x baseline comparison.
3. **Federation safety:** negotiation needs authenticated complete offers/freshness/floors, while
   adapter loss and parser acceptance limits need constitutional status rules.
4. **Operator truth:** candidate-shipped runbooks must be digest-bound, and removal/recovery must
   prove owner exit, mixed-file preservation, and all durable mutation boundaries.
5. **Empirical validity:** arm equivalence, owner-normalized weighting, and harm-missingness treatment
   must be mandatory, not left as optional protocol choices.

Two incorrect universal-rule references are also normative defects and require new bytes.

## Synthesis rule application

The plan gives a supported high-consequence contradiction precedence over stylistic approval. The
findings above are testability, security, and decision-scope defects in the RFC itself, not merely
missing future implementation. Therefore `ready_for_adr` is unlawful for this digest.

## Required next move

1. preserve R2, this memo, and this synthesis as immutable history;
2. author revision 3 resolving every controlling finding;
3. declare a fresh exact R3 digest and review-set plan;
4. execute fresh review lanes; and
5. attach only the new controlling synthesis as ADR-ready if it returns `ready_for_adr`.

```text
final_recommendation = request_another_rfc_revision_round
review_outcome = revise_rfc
```
