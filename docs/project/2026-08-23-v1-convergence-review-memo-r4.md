---
summary: "Current-track R4 review memo for Decision 128: four lanes approve, one requires an immutable G0-A3 admission record."
read_when:
  - "Inspecting the historical R4 review attempt."
  - "Checking the final R4-to-R5 correction."
type: "review_memo"
task_id: 4907
decision_id: 128
artifact_kind: "review_memo"
reviewed_artifact_ref: "docs/rfc/2026-08-23-v1-convergence-contract-r4.md"
reviewed_sha256: "dfaf60c826ca1eec475a848b7b8ff7a81344f6c13251b7c81179e6f53096b5d1"
track_id: "current_track"
review_outcome: "revise_rfc"
---

# Review Memo — engineering-core v1.0 convergence revision 4

## Status

```text
reviewed_artifact = docs/rfc/2026-08-23-v1-convergence-contract-r4.md
reviewed_SHA256 = dfaf60c826ca1eec475a848b7b8ff7a81344f6c13251b7c81179e6f53096b5d1
review_outcome = revise_rfc
next_legal_move = bounded_R5_then_fresh_review
ADR_legal_from_R4 = false
```

All lanes confirmed the digest and made no mutation.

## Lane outcomes

| Lane | Continuation evidence | Outcome |
|---|---|---|
| Semver/authority | `dispatch-1787524357077` | `ready_for_adr`; G0 authority deadlock closed. |
| Protocol/federation | `dispatch-1787524357079` | `revise_rfc`; G0-A3 lacks immutable source-transition admission. |
| Operator/rendering | `dispatch-1787524357081` | `ready_for_adr`; all R3 operator findings closed. |
| Empirical validity | `dispatch-1787524357083` | `ready_for_adr`; no regression. |
| Governance/legality | `dispatch-1787524357085` | `ready_for_adr`; ADR legal now: no pending artifacts. |

## Findings closed

R4 lawfully introduced exact G0-A2 convergence-implementation tasks and a G0-A3 candidate task,
kept release authority separate, required exact installed-wheel/extracted-sdist rendering, restored
malformed-input fail-before-effect rules, covered every durable mutation boundary, required non-empty
structured/text mixed-ownership maps, and scoped v1 resolution per adoption/package scope.

## Controlling blocker

G0-A3 verifies task fan-in and clean source state but does not emit an immutable admission record
binding the exact base tree, reviewed implementation outputs, accepted G4 bytes/negative lineage,
frozen G0-A2 protocol/template/fixture/impact/toolchain inputs, candidate-task identity, and permitted
content diff. An effect allowlist alone cannot prove source provenance. A clean but stale or unrelated
committed tree could become a self-consistent candidate and be detected only post hoc.

R5 must:

1. include G0-A3 in universal stage binding;
2. require a named immutable admission record with every authorized input/digest/task/allowlist;
3. require candidate preparation to produce only the declared transition and restart A3 on drift;
4. make G0-B verify the candidate tree/diff against that record; and
5. keep candidate checks synthetic/study-disjoint and prohibit premature G1–G4 corpus execution.

## Outcome

```text
review_outcome = revise_rfc
next_legal_move = create docs/rfc/2026-08-23-v1-convergence-contract-r5.md
```

Model A remains viable. R4 is immutable review history and authorizes no ADR or implementation.
