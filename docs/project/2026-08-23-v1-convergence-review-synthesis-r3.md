---
summary: "Controlling R3 synthesis for Decision 128: broad closure achieved, but two lanes require a bounded R4."
read_when:
  - "Checking the controlling outcome of the R3 convergence review set."
  - "Tracing the R3-to-R4 revision boundary."
type: "review_synthesis"
task_id: 4907
decision_id: 128
artifact_kind: "review_synthesis"
review_outcome: "revise_rfc"
reviewed_artifact: "docs/rfc/2026-08-23-v1-convergence-contract-r3.md"
reviewed_sha256: "eb7279ca3d844baefa1f1377a63f124b36379c57c975412a6fca1cf455635ed7"
---

# Review Synthesis — engineering-core v1.0 convergence revision 3

## Controlling state

```text
review_closure_mode = multi_lane_requires_synthesis
reviewed_artifact = docs/rfc/2026-08-23-v1-convergence-contract-r3.md
reviewed_SHA256 = eb7279ca3d844baefa1f1377a63f124b36379c57c975412a6fca1cf455635ed7
review_outcome = revise_rfc
legal_next_move = bounded_r4_then_fresh_review
ADR_legal_from_R3 = false
```

Inputs:

- `docs/project/2026-08-23-v1-convergence-review-set-plan-r3.md`
- `docs/project/2026-08-23-v1-convergence-review-memo-r3.md`
- five resumed lane sessions under dispatch IDs `dispatch-1787524357077`, `...7079`, `...7081`, `...7083`, and `...7085`

## Synthesis

R3 closed every R2 semver, population, protocol, adapter, parser, downgrade, empirical, governance,
and transfer-reference blocker. Three lanes found the RFC ready on their domains. Two concrete defects
still control under the predeclared no-vote rule:

1. the gate graph contains no checkpoint that lawfully releases convergence implementation and
   candidate-preparation tasks between G0-A2/G4-A and G0-B; and
2. G1 can still pass archive-only rendering, weakened malformed-input boundaries, or vacuous
   mixed-ownership coverage.

These are localized and do not undermine Model A. They are nevertheless architectural testability
and authority defects in the reviewed bytes. Missing Git/AK closure is separately a lifecycle step,
not the reason for this substantive outcome.

## Required R4 delta

- Add a post-G0-A2/G4-A implementation and candidate-preparation admission checkpoint with exact
  engineering-core tasks, dependencies, allowed effects, and no publication authority.
- Require exact built-wheel installation and extracted-sdist workflow execution for all rendered
  assertions.
- Restore fail-before-effect rules for malformed/unavailable pins and malformed policy.
- Require non-vacuous structured/text mixed-ownership coverage or reviewed non-applicability.
- Scope the no-mixed-runtime invariant per declared adoption/resolution scope.

```text
final_recommendation = bounded_revision_then_rereview
review_outcome = revise_rfc
```

R3 remains immutable history and authorizes no ADR or implementation.
