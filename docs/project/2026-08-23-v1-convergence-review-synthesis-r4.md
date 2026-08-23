---
summary: "Controlling R4 synthesis for Decision 128: one final candidate-admission provenance gap requires R5."
read_when:
  - "Checking the controlling R4 outcome."
  - "Tracing why R4 did not yet close ADR review."
type: "review_synthesis"
task_id: 4907
decision_id: 128
artifact_kind: "review_synthesis"
review_outcome: "revise_rfc"
reviewed_artifact: "docs/rfc/2026-08-23-v1-convergence-contract-r4.md"
reviewed_sha256: "dfaf60c826ca1eec475a848b7b8ff7a81344f6c13251b7c81179e6f53096b5d1"
---

# Review Synthesis — engineering-core v1.0 convergence revision 4

## Controlling outcome

```text
review_outcome = revise_rfc
reviewed_SHA256 = dfaf60c826ca1eec475a848b7b8ff7a81344f6c13251b7c81179e6f53096b5d1
legal_next_move = bounded_R5_then_fresh_review
ADR_legal_from_R4 = false
```

Inputs are the R4 plan, R4 memo, and five continued lanes under dispatch IDs
`dispatch-1787524357077`, `...7079`, `...7081`, `...7083`, and `...7085`.

Four lanes found R4 ready. The protocol lane's high-confidence source-provenance finding controls:
G0-A3 has effect and task boundaries but no immutable admission record proving that the candidate is
the authorized transition from reviewed implementation/G4 outputs and frozen protocol inputs.
Post-hoc candidate consistency is not equivalent to transition provenance.

The required correction is narrow: bind every admitted source/input/task/allowlist digest before
candidate preparation, constrain the exact tree/diff transition, restart on drift, and require G0-B
to verify that record. Candidate checks must not expose G1–G4 qualification outputs early.

```text
final_recommendation = bounded_revision_then_rereview
review_outcome = revise_rfc
```

R4 authorizes no ADR or implementation.
