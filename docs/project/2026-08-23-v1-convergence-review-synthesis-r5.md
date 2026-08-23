---
summary: "Controlling R5 synthesis for Decision 128: revision 5 is ready for ADR after exact Git/AK attachment."
read_when:
  - "Checking the controlling review closure for Decision 128."
  - "Preparing the v1 convergence ADR without implying implementation or release."
type: "review_synthesis"
task_id: 4907
decision_id: 128
artifact_kind: "review_synthesis"
review_outcome: "ready_for_adr"
reviewed_artifact: "docs/rfc/2026-08-23-v1-convergence-contract-r5.md"
reviewed_sha256: "d8a17d69b12d9235de75e123acb28362876f0062d504ac45d991cec15736b5e4"
---

# Review Synthesis — engineering-core v1.0 convergence revision 5

## Controlling outcome

```text
review_closure_mode = multi_lane_requires_synthesis
reviewed_artifact = docs/rfc/2026-08-23-v1-convergence-contract-r5.md
reviewed_SHA256 = d8a17d69b12d9235de75e123acb28362876f0062d504ac45d991cec15736b5e4
review_outcome = ready_for_adr
legal_next_move = open_adr_pack_after_AK_attachment
implementation_legal = false
release_legal = false
```

Inputs:

- `docs/project/2026-08-23-v1-convergence-review-set-plan-r5.md`
- `docs/project/2026-08-23-v1-convergence-review-memo-r5.md`
- R2–R4 plans, memos, and controlling `revise_rfc` syntheses
- five R5 lane continuations under dispatch IDs `dispatch-1787524357077`, `...7079`,
  `...7081`, `...7083`, and `...7085`

## Synthesis judgment

All five required R5 lanes independently returned `ready_for_adr`. No medium- or high-confidence RFC
blocker remains.

Revision 5 preserves Model A while resolving the multi-review process's controlling disputes:

1. v1.0 is a clean break from v0 package behavior, but v1.x and retained protocol meanings are stable;
2. the public constitution is separate from owner adapters and internal qualification machinery;
3. final stable/rendered manifests follow live pilot dispositions and bind executable assertions;
4. participants are qualification facts selected under constitutional independence properties;
5. public operator journeys, installed artifacts, hostile inputs, adapters, and empirical claims have
   executable fail-closed oracles rather than static confidence;
6. live governance outcomes are not quota-driven or coerced; and
7. the source-to-candidate transition is admitted prospectively from exact reviewed bytes and verified
   independently before any qualification evidence.

The strongest alternative—a smaller deterministic-core v1 with calibration/governance outside the
release claim—is viable but rejected for a stated product reason and with its lower cost acknowledged.
The architecture therefore reflects an explicit preference, not fake synthesis.

## Non-blocking downstream decisions

The accepted G0-A2 protocols may still specify, without reopening this architecture when they preserve
its invariants:

- admission-record schema/canonicalization and verifier identity;
- exact egress serialization and `unsupported` versus `incomplete` mappings;
- resource budgets above public parser guarantees;
- empirical SESOI, error/power, calibration, harm, and confidential-oracle commitments;
- rollback behavior under post-apply drift and platform-matrix rendering coverage.

Any change to a public v1 promise, pillar, authority boundary, population-independence property, or
constitutional invariant reopens the architecture instead.

## Lifecycle legality

The substantive review is complete, but ADR recording is not legal until canonical state catches up:

1. commit the exact R2–R5 lineage and supporting artifacts;
2. revise Decision 128 through each immutable RFC attempt, attaching each plan/memo/synthesis in order;
3. attach the problem brief and evidence note;
4. make this R5 synthesis the controlling `ready_for_adr` closure with exact commit/content binding;
5. confirm the passport and direction checks; and
6. move to decision-owner acceptance/ADR preparation through separately scoped task `4870`.

The known `ak decision review-lineage --check` failure over four missing historical source files is a
pre-existing projection/tooling warning, not evidence against this RFC. It must be recorded truthfully
and must not be misreported as a passing check.

## Final recommendation

```text
review_outcome = ready_for_adr
recommendation = approve_R5_as_ADR_basis
next_legal_move = attach_exact_lineage_then_open_ADR_pack
```

This synthesis does not accept Decision 128, create the ADR, authorize implementation, clear
post-ADR tasks, create a candidate, or permit publication.
