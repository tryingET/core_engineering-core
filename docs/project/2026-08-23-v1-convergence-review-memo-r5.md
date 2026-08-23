---
summary: "Current-track R5 review memo for Decision 128: all five lanes find the revised Model A contract ready for ADR."
read_when:
  - "Preparing or reviewing the Decision 128 ADR."
  - "Checking the final current-track review of the v1 convergence contract."
type: "review_memo"
task_id: 4907
decision_id: 128
artifact_kind: "review_memo"
reviewed_artifact_ref: "docs/rfc/2026-08-23-v1-convergence-contract-r5.md"
reviewed_sha256: "d8a17d69b12d9235de75e123acb28362876f0062d504ac45d991cec15736b5e4"
track_id: "current_track"
review_outcome: "ready_for_adr"
---

# Review Memo — engineering-core v1.0 convergence revision 5

## Review chain status

```text
review_kind = re-review after revise_rfc
reviewed_artifact = docs/rfc/2026-08-23-v1-convergence-contract-r5.md
reviewed_SHA256 = d8a17d69b12d9235de75e123acb28362876f0062d504ac45d991cec15736b5e4
review_outcome = ready_for_adr
legal_next_move = attach_controlling_synthesis_then_open_adr_pack
ADR_legal_now_before_AK_attachment = no
implementation_authorized = false
```

All five lanes confirmed the exact digest, made no mutation, and returned `ready_for_adr`.

## Lane evidence

| Lane | Continued dispatch | Outcome | Controlling conclusion |
|---|---|---|---|
| Semver/authority | `dispatch-1787524357077` | `ready_for_adr` | A3 admission closes stale/unauthorized candidate trees; public/v1.x/population/alternative contracts remain coherent. |
| Protocol/federation | `dispatch-1787524357079` | `ready_for_adr` | Every R4 admission requirement and prior protocol/security finding is closed. |
| Operator/rendering | `dispatch-1787524357081` | `ready_for_adr` | Exact artifacts, public runbooks, failure boundaries, mixed ownership, scoped resolution, and owner exit are testable. |
| Empirical validity | `dispatch-1787524357083` | `ready_for_adr` | A3 remains study-disjoint; treatment, weighting, power, forecast, harm, safety, and freeze invariants remain intact. |
| Governance/legality | `dispatch-1787524357085` | `ready_for_adr`; ADR legal now: no | No authority promotion or G4 coercion; Git/AK attachment is the remaining legal step. |

Session/dispatch evidence is supporting execution evidence, not canonical legal closure. This memo and
the attached synthesis become review facts only through AK.

## System4D summary

- **Boundary:** stable portable v1 product constitution plus separately owned qualification protocols,
  participant tasks, empirical work, and release authority.
- **Driver:** earn a trustworthy v1 claim without carrying v0 compatibility or centralizing owner truth.
- **Invariants:** four non-compensating pillars; stable v1.x meaning; exact task/evidence/candidate
  lineage; no self-authorizing proof; owner exit and irreversible-effect honesty.
- **Main risks controlled:** accidental public proof APIs, stale candidate sources, downgrade/adapter
  loss, harness proxies, arbitrary studies, coerced governance outcomes, and publication drift.

## Lens 1 — Product constitution, semver, and protocol boundary

### Strengths

- Clean v0-to-v1 break is explicit while retained protocol identifiers preserve independent meaning.
- Public stable, experimental, internal qualification, and owner-adapter classes are default-deny.
- Final manifests occur after G4-A, bind per-entry sources/assertions, and become the v1.x baseline.
- Population identities are qualification facts; owner-independence properties remain constitutional.
- The strongest narrower-core alternative and Model A's delay/dependency costs are fairly represented.

### Risks and disposition

- Future admission/compatibility schemas still need exact implementation. Their absence is a fail-closed
  G0 prerequisite, not an RFC blocker.
- Optional protocol refinements—egress semantics and exact `unsupported`/`incomplete` mapping—remain
  owned by the accepted protocol without changing constitutional rules.

### Evidence quality

Strong for architecture text and current source-surface observations; future runtime behavior remains
`insufficient evidence` until its gates run.

## Lens 2 — Operator, federation, and empirical testability

### Strengths

- G1 uses candidate-digest public behavior, reviewed-plan binding, every-boundary failure recovery,
  non-vacuous mixed ownership, exact installed wheel/sdist rendering, rollback, removal, and owner exit.
- G2 uses authenticated complete offers, a local security floor, append-only adapter lineage,
  non-shrinkable parser guarantees, and entrypoint × threat coverage.
- G3 isolates the evidence treatment, normalizes first by owner, uses a common model set, and delegates
  justified values prospectively while preserving multiplicity, forecast, harm, missingness, and safety.

### Risks and disposition

Implementation, participant, power, fixture, and candidate evidence do not exist. The RFC never labels
them current and blocks every downstream claim until executable checks pass.

### Evidence quality

Contract testability is strong; empirical and operator success remain `insufficient evidence` by design.

## Lens 3 — Federated governance, candidate provenance, and release authority

### Strengths

- G4 live owner decisions have no required outcome distribution; fixtures prove mechanics only.
- G0-A3 prospectively binds the exact base tree, reviewed outputs, frozen inputs, task/allowlists, and
  output-byte derivation before candidate work; G0-B independently verifies that transition.
- Candidate, readiness, release, tag, publication, and post-release verification remain separate.
- Participant, empirical, content-owner, AK, candidate, and release authority never collapse.

### Risks and disposition

AK still points to the historical RFC and lacks attachments. That is a lifecycle blocker to ADR
recording, not a substantive R5 defect.

### Evidence quality

Strong for normative boundaries and current AK readback; future effects remain unexecuted.

## Required checklist disposition

- problem framing: evidence-backed;
- options: fairly represented;
- preferred direction: explicit two-layer Model A;
- stable core/adapter boundary: clear;
- interfaces/contracts: assertion- and fixture-bindable;
- transition/rollback: realistic and public-surface bound;
- docs/templates: exact installed-artifact execution required;
- validation: executable and fail-closed;
- open questions: downstream protocol choices, not hidden architecture choices;
- recommendation: actionable.

## Outcome

```text
review_outcome = ready_for_adr
next_legal_move = attach_R5_memo_and_controlling_synthesis_then_prepare_ADR
```

This outcome accepts R5 as an ADR basis only. It does not accept Decision 128, record the ADR, release
post-ADR tasks, or claim any G0–G5 implementation or PASS.
