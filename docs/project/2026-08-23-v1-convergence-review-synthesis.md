---
summary: "Adversarial review synthesis for the proposed engineering-core v1.0 convergence contract under AK task 4869."
read_when:
  - "Deciding whether the v1.0 convergence RFC is ready for an owner decision and ADR."
  - "Checking the review findings, authority boundaries, or unresolved prerequisites before G0-A1."
type: "review-synthesis"
---

# Review synthesis — engineering-core v1.0 convergence contract

## Status and authority

- **Execution binding:** AK task `4869`, repository `/home/tryinget/ai-society/core/engineering-core`.
- **Reviewed artifact:** `docs/rfc/2026-08-23-v1-convergence-contract.md`.
- **Decision:** AK `128`, still `review_pending` at synthesis time.
- **Review disposition:** `ready_for_adr` after this synthesis and the RFC are committed and their canonical AK attachment binds the exact commit and RFC content digest. This is the review outcome only; it does not assert that decision 128's full passport is ready while other required lifecycle artifacts remain absent.

This is decision support, not acceptance of Model A. It does not advance decision 128, record an ADR, release task 4870, authorize participant mutation, create a candidate, or authorize publication.

## Bound scope

Task 4869 permits changes only to the RFC and this synthesis. Source, tests, workflows, catalogs, policy, package metadata, lockfiles, participant repositories, AK dependencies, decision state, and release state remain outside the mutation scope.

The review therefore hardened the proposed contract and made current implementation gaps explicit fail-closed prerequisites. It did not implement later G0–G5 work under the review task.

## Review process

The review used:

1. the durable vision and current product posture;
2. AK task 4869, decision 128, direction reconciliation, and linked-task graph 4870–4877;
3. independent authority/task-graph, empirical-method, security/privacy, release, operator-journey/lifecycle, and contract-consistency analyses;
4. the governed `deep-review` workflow for the current iteration;
5. one earlier bounded read-only Nexus completion check (`dispatch-1787513423705`).

The earlier completion check found no blocker and made no mutation. The later governed review exposed a candidate-freeze phase contradiction plus weaker pin-failure and residual-effect oracles; this task-owned Nexus fix resolved those findings without expanding scope.

## Controlling findings and resolution

| Finding | Resolution in the reviewed RFC |
|---|---|
| G0 required protocols/population before the tasks that could create them. | Split G0 into G0-A1 accepted-decision admission, G0-A2 protocol/population/owner-task admission, and G0-B candidate freeze. |
| Pre-candidate evidence could not bind a future candidate. | Added stage-correct bindings for G0-A, G4-A, G0-B, and post-candidate gates. |
| G0-A2 froze candidate-dependent G2 fixtures and expected digests while candidate identity was unassigned. | Added a machine-checkable transition-template manifest: G0-A2 freezes only candidate-independent templates/rules; G0-B read-only materialization emits separately custodied candidate-bound instances and independently reviewed expected digests. |
| Population and gate artifacts could be mistaken for live owner/AK truth. | Declared the population manifest a canonical protocol input only; added live-state re-resolution, canonical bytes, authority ceilings, and machine-decidable gate envelopes. |
| G1's 40/40 threshold lacked frozen oracles and sequenced removal after rollback. | Added per-journey manifests, disposable replicas, exact failure boundaries, independent rollback/removal branches, final proof-workspace state, and exact negative-control semantics. |
| One bad-pin case conflated local syntax rejection with realistic remote unavailability. | Split malformed-local and well-formed-unavailable fixture-remote cases with distinct network/effect boundaries and structured outcomes. |
| Hostile inputs, transfer, path races, process limits, secret observation, and custody were underdefined. | Added default-deny exact-byte transfer, no-follow/root containment, TOCTOU and injection fixtures, resource/process bounds, synthetic canaries, authenticated custody, and incident closure. |
| G3's estimand, power target, missingness, safety cases, allocation, and forecasts were gameable. | Defined an arm-neutral task-cluster estimand, powered compound rule, separate safety set, pessimistic missingness, prospective freeze, balanced model allocation, and bounded calibration metrics. |
| Equal G3 cell weighting still allowed sparse baseline × model cells. | Required at least six independent clusters per required cell, pre-output allocation checks, cell-level reporting, and non-waivable cell harm stops. |
| G4 could count same-owner contexts and conflate rejection with rollback. | Defined independence by owner group, separated lifecycle facts, required distinct rejection/retirement and rollback observations, and added immutable inclusion/lineage mapping. |
| G4/G5 fan-in relied on titles or deferral prose. | Made exact AK dependency edges mandatory and non-waivable. |
| G5 readiness could be read as release authority. | Made G5 evidence-only and required a separate exact release task plus dependent post-release verification. |
| G5 cleanliness could pass with ignored files, caches, processes, services, network activity, or other undeclared residue. | Added a candidate-bound effect allowlist, same-boundary before/after inventories, custody/disposal receipts, and fail-closed readiness checks for undeclared effects or surviving processes. |
| Release automation could select an ancestral tag, rebuild different bytes, or detect mismatch only after publication. | Added one candidate-contained executable conformance membrane with `candidate`, `readiness`, and `pre-publish` modes; exact SHA equality; pre-existing-tag failure; pinned toolchain identity; and pre-tag/upload comparison with G5-approved artifact bytes. |
| G5 depended on a machine-local docs command. | Required a repository-contained docs/reference check executed through the frozen candidate conformance path. |
| Partial publication lacked explicit point-of-no-return states. | Defined candidate, release-blocked, tag-created/release-absent, published-verification-pending, and published-and-verified states. |

## Frozen authority invariants

- Review can freeze exact proposal bytes for decision support; it cannot accept product direction.
- A path-only reference does not satisfy immutable RFC or review binding.
- Engineering-core validates bounded projections but does not replace AK, participant, empirical-owner, content-owner, or release-owner truth.
- No gate artifact, model result, owner receipt, empirical result, loop completion, or G5 PASS self-authorizes the next effect.
- Current workflow/source nonconformance blocks the applicable future gate; prose does not relabel it as shipped behavior.
- Public tag creation is the release-lineage point of no return.

## Current implementation prerequisites outside task 4869

These are explicit future gate conditions, not completed behavior:

- decision 128 still needs the AK-required problem/evidence lifecycle artifacts, lawful review-track and synthesis closure, owner acceptance, and an ADR before G0-A1;
- the candidate-contained gate-conformance validator, stage-transition materializer, candidate-bound effect inventory, and repository-local docs check do not yet exist;
- current auto/manual release workflows do not enforce the proposed equality, artifact-byte, toolchain, or pre-publish membrane and therefore cannot pass G0-B;
- exact participant, empirical, content-owner, release, and post-release tasks/dependencies must be accepted and attached by their owners;
- no G0–G5 PASS, candidate, v1 release, or downstream adoption is claimed.

## Product-posture frontier deferral

- **Bound task and excluded target:** AK task `4869` does not authorize `/home/tryinget/ai-society/core/engineering-core/docs/project/product_posture.md`; that exact path remains owned by the engineering-core product owner.
- **Live authority proof:** launch entity version `3`; revalidated live entity version `4`; authority digest `6be2391aaaf91d91bd92280c9a8cef1e65d8e793eae7ac16c2f24203d7641847`. The live task remained claimed by `pi:01a0302e-39ac-728f-a87d-9661fc27118e` with a future lease and the posture path remained outside its literal whitelist.
- **Deferred frontier update:** review maturity improved only: the proposed contract now has a machine-checkable G0-A2→G0-B stage transition, distinct pin-failure boundaries, and residual-effect accounting, with focused static, docs, and self-check proof. No mechanism, gate PASS, decision acceptance, candidate, or release became current.
- **Remaining gap and trigger:** decision 128 still lacks its required lifecycle/review closure and ADR, and the transition/conformance mechanisms remain unimplemented. After task 4869's exact commit and RFC digest are available, a new exact engineering-core owner task that explicitly allows `docs/project/product_posture.md` must revalidate live maturity and record this frontier before owner-authorized convergence execution selects its next slice.

## Verification

The task-owned change was checked with:

- `git diff --check`;
- static RFC ordering, stage-transition, failure-boundary, residual-effect, status-language, scope, and file-budget assertions;
- strict documentation discovery/reference validation;
- `UV_NO_CONFIG=1 uv run --frozen python -m engineering_core.self_check --repo-root .`;
- the governed deep-review findings and bounded Nexus fix above.

The final repository impact/landing gate remains separate from this review synthesis and must run against the final committed state under the repository's normal landing workflow.

## Rollback

Before owner acceptance, restore the RFC and remove this synthesis under task 4869. After acceptance, revise through decision 128's governed RFC revision path; never rewrite review or failed-evidence lineage.

## Review conclusion

The proposed RFC is internally coherent, fail-closed, owner-bounded, and has a `ready_for_adr` review disposition. Decision/ADR readiness still requires immutable commit/AK bindings and every other prerequisite reported by decision 128's passport. This conclusion is not evidence that the proposed validator, protocols, workflows, empirical campaign, lifecycle campaign, candidate, or release has been implemented or demonstrated.
