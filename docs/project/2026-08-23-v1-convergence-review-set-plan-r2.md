---
summary: "Fresh multi-domain review-set plan for Decision 128 revision 2 after the explicit clean pre-v1 break."
read_when:
  - "Reviewing revision 2 of the v1 convergence RFC."
  - "Checking the review topology and ADR-closure conditions for Decision 128."
type: "review_set_plan"
task_id: 4907
decision_id: 128
artifact_kind: "review_set_plan"
rfc_ref: "docs/rfc/2026-08-23-v1-convergence-contract-r2.md"
rfc_sha256: "93f6060d6fab2af7b0b39b4dd0d998592ce0c9a7610f7b42b701f396986c24a5"
---

# Review Set Plan — engineering-core v1.0 convergence revision 2

## Status and legal effect

```text
decision = 128
review_kind = re-review after revise_rfc
reviewed_artifact = docs/rfc/2026-08-23-v1-convergence-contract-r2.md
reviewed_SHA256 = 93f6060d6fab2af7b0b39b4dd0d998592ce0c9a7610f7b42b701f396986c24a5
outer_host = pi_sdk
AK_active_track = current_track
review_closure_mode = multi_lane_requires_synthesis
intended_effect = closure_candidate
```

This plan precedes review execution. It authorizes no source implementation, participant work,
decision acceptance, ADR, candidate, or release. Any reviewed-RFC byte change invalidates this plan's
execution result and requires a fresh plan/reference rather than silent reuse.

## Inputs

- `docs/project/2026-08-23-v1-convergence-problem-brief.md`
- `docs/project/2026-08-23-v1-convergence-evidence-note.md`
- `docs/project/vision.md`
- `docs/project/product_posture.md`
- `docs/support-policy.md`
- `docs/rfc/2026-08-23-v1-convergence-contract.md` (historical comparison only)
- `docs/project/2026-08-23-v1-convergence-review-synthesis.md` (historical review only)
- AK task `4907`, decision passport `128`, and active direction `AK.V5.SF01`
- governance-kernel decision lifecycle and review-synthesis v6 contract

## Review objective

Determine whether revision 2 preserves Model A while making the architecture decision-grade:

- clean package break from pre-v1 without weakening safe transition or truthful rejection;
- compatible, testable v1/v1.x public semantics;
- stable core separated from adapters and internal qualification tooling;
- public operator/rendering behavior rather than harness proxies;
- prospectively justified empirical/resource protocols; and
- live owner legitimacy without prescribed substantive outcomes.

## Execution lanes

The lanes are execution-time evidence. AK's bounded runtime still records one canonical
`current_track` memo and a later controlling synthesis.

### Lane 1 — Semver and public-product constitution

Assess the clean v0-to-v1 break, public/default-stable classification, v1.x change rules, protocol-ID
independence, candidate release identity, and strongest alternatives.

### Lane 2 — Protocol, adapter, and adversarial federation

Assess canonical v1 envelopes, ingress/egress ownership, negotiation/downgrade resistance,
unsupported history, critical fields, provenance/loss records, hostile fixtures, and portability.

### Lane 3 — Operator journey and rendered product

Assess candidate-shipped planning/apply/recovery/rollback/removal, reviewed-plan binding, mixed-file
ownership, clean replacement, installed wheel/sdist rendering, docs/template parity, and owner exit.

### Lane 4 — Prospective empirical validity

Assess estimand, owner weighting, power/sensitivity decision, model diversity, forecast provenance,
calibration, missingness, harm stops, safety cases, and the boundary between ADR invariants and a
separately accepted empirical protocol.

### Lane 5 — Federated governance and lifecycle legality

Assess participant/content/release/AK authority, non-coercive G4 design, deterministic transition
coverage, immutable negative lineage, task/dependency shape, and current ADR legality.

## Required review questions

1. Is the preferred two-layer Model A explicit and fairly compared with a narrower-core alternative?
2. Are stable public surfaces and adapter/internal boundaries specific enough to enumerate and test?
3. Does dropping pre-v1 compatibility leave a realistic transition, recovery, rollback, and removal contract?
4. Do rendered docs/templates have an installed-artifact oracle rather than static confidence?
5. Are G2/G3 bounds and thresholds prospective, justified, and protected from post-hoc revision?
6. Does G4 prove mechanics and legitimacy without outcome quotas or authority promotion?
7. Can the gate/release graph fail and recover without claiming rollback of irreversible effects?
8. Do all status and AK statements distinguish proposal, review closure, ADR, implementation, and release?

## Synthesis rule

The designated synthesizer must cite the exact RFC digest and all lane conclusions, distinguish
constitutional blockers from downstream protocol/implementation preconditions, and emit one token:

- `ready_for_adr` only when no unresolved constitutional or review-level blocker remains;
- `revise_rfc` when Model A remains viable but the reviewed bytes need change; or
- `reject_current_direction` when the architecture should not continue.

No vote or average controls. A concrete high-consequence contradiction supported by the artifact
controls over a larger count of stylistic approvals. Downstream implementation absence is not itself
an RFC blocker when the RFC makes it an explicit fail-closed gate.

## Canonical outputs

- current-track memo: `docs/project/2026-08-23-v1-convergence-review-memo-r2.md`
- controlling synthesis: `docs/project/2026-08-23-v1-convergence-review-synthesis-r2.md`

The plan must be attached to AK before synthesis. The memo and synthesis use fresh, single-use refs.
Only the synthesis may close ADR legality under `multi_lane_requires_synthesis`.

## Completion conditions

- every lane examines the exact declared digest;
- provenance and coverage limits are recorded;
- the memo answers all required review questions;
- the synthesis names the legal next move;
- `ak decision passport 128` identifies the controlling closure without inference from session logs.
