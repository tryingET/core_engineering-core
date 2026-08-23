---
summary: "Current-track review memo for Decision 128 revision 2; five lanes require one further RFC revision."
read_when:
  - "Inspecting the historical R2 review attempt for Decision 128."
  - "Checking why R3 was required before ADR readiness."
type: "review_memo"
task_id: 4907
decision_id: 128
artifact_kind: "review_memo"
reviewed_artifact_ref: "docs/rfc/2026-08-23-v1-convergence-contract-r2.md"
reviewed_sha256: "93f6060d6fab2af7b0b39b4dd0d998592ce0c9a7610f7b42b701f396986c24a5"
track_id: "current_track"
review_outcome: "revise_rfc"
---

# Review Memo — engineering-core v1.0 convergence revision 2

## Review chain status

```text
review_kind = re-review after revise_rfc
reviewed_artifact = docs/rfc/2026-08-23-v1-convergence-contract-r2.md
reviewed_SHA256 = 93f6060d6fab2af7b0b39b4dd0d998592ce0c9a7610f7b42b701f396986c24a5
review_outcome = revise_rfc
legal_next_move = produce_r3_and_fresh_review_set
ADR_legal_from_this_attempt = false
implementation_authorized = false
```

All lanes confirmed the exact digest and made no mutation.

## Lane evidence

| Lane | Execution evidence | Controlling conclusion |
|---|---|---|
| Semver/public constitution | `dispatch-1787524357077` | Manifest/G4 ordering, exhaustive stable-surface test binding, qualification-population layering, and strongest-alternative analysis need revision. |
| Protocol/adversarial federation | `dispatch-1787524357079` | Downgrade transcript/floor, adapter-loss status, stable parser limits, and minimum-v1 compatibility need tightening. |
| Operator/rendered product | `dispatch-1787524357081` | Candidate-runbook identity, removal/owner-exit postconditions, mixed-file drift, and every-boundary recovery remain under-specified. |
| Prospective empirical validity | `dispatch-1787524357083` | Arms must differ only by treatment; owner/model weighting and harm-missingness rules need correction. |
| Federated governance/legality | `dispatch-1787524357085` | G4 is non-coercive, but two transfer rules cite the wrong universal-rule ordinal; ADR lifecycle artifacts are still absent. |

Dispatch/session evidence is not canonical closure. This memo embodies the reviewed findings; AK controls legal state.

## Strengths retained

- Model A is explicit and all four pillars remain non-compensating.
- The v0-to-v1 clean break is coherent and does not weaken recovery, removal, owner exit, privacy, custody, or hostile-input expectations.
- Package semver and protocol identity are correctly separated.
- Public surfaces default stable; proof tooling and owner adapters are not automatically public.
- G3 exact values are delegated to a prospectively accepted empirical protocol rather than invented in the RFC.
- G4 now separates live legitimacy from deterministic transition coverage and no longer requires an outcome quota.
- Candidate, release, publication, and verification identities remain distinct.

## Must-fix findings

1. Freeze final compatibility/rendered manifests after G4-A or constrain G4-A so it cannot mutate an already frozen public surface.
2. Require every compatibility-manifest entry to cite a normative source and executable assertion, plus a frozen v1 baseline for later v1.x comparison.
3. Move named participants and ordinary population replacement out of the constitution into an accepted qualification protocol while retaining constitutional independence requirements.
4. Compare Model A fairly with the strongest narrower-core/independent-qualification alternative.
5. Require authenticated complete-offer negotiation, freshness/channel binding, deterministic version order, and a local minimum semantic/security floor.
6. Classify adapter loss and require canonical output/config digests and append-only conversion lineage; critical semantic loss cannot yield `complete`.
7. Separate stable parser acceptance guarantees from platform qualification budgets; existing valid v1 use cannot be replaced by a downgrade result.
8. Bind every G1 runbook to a candidate path/digest and require removal/exit postconditions, mixed-file/post-apply drift cases, clean-transition invariants, and failure recovery at every durable mutation boundary or verified atomicity.
9. Make evidence the sole arm difference, normalize weights first by owner, and apply pessimistic missingness to harm boundaries.
10. Correct G2/G3 transfer references to the named default-deny transfer/custody rule.

## Required questions

- **Preferred direction:** explicit and viable.
- **Stable core versus adapters:** directionally clear, but test binding and adapter-loss semantics need revision.
- **Transitional compatibility:** clean pre-v1 break is clear; safe transition remains required.
- **Migration/rollback:** public-surface direction is sound but removal/recovery oracles are incomplete.
- **Rendered behavior:** broad manifest exists, but runbook identity must be digest-bound.
- **Executable validation:** strong overall; stable-surface baseline comparison is missing.
- **Options:** strongest narrower-core alternative is not yet fairly represented.

## Outcome

```text
review_outcome = revise_rfc
next_legal_move = create docs/rfc/2026-08-23-v1-convergence-contract-r3.md
```

Revision 2 remains immutable review history. It is not an ADR basis.
