---
summary: "Accepted Model A revision 5: a two-layer semver v1.0 convergence contract (public product constitution plus cumulative four-pillar release qualification) with a clean pre-v1 break."
read_when:
  - "Executing any engineering-core v1.0 convergence task, protocol, harness, candidate, release, or post-release verification."
  - "Deciding whether a v1 pillar is demonstrated, whether a surface is public stable, or whether a change is compatible within v1.x."
  - "Assessing rollback, stop, or release-blocking behavior for v1.0 convergence work."
type: "adr"
---

# ADR — Adopt the engineering-core v1.0 Model A convergence contract

## Status

Accepted.

- AK decision: `128` (architecture, cross-repo, strict convergence with multi-lane synthesis), outcome **accepted** under this ADR.
- Authoritative contract: `docs/rfc/2026-08-23-v1-convergence-contract-r5.md`
  (SHA-256 `d8a17d69b12d9235de75e123acb28362876f0062d504ac45d991cec15736b5e4`,
  frozen in commit `6ea86917cc062516a0f04d6352e5fadf1d7ff0de`).
- Review lineage: RFC revisions R2–R5 with immutable review-set plans, memos, and syntheses;
  R5 closed `ready_for_adr` from five exact-digest specialist lanes
  (semver/core authority, protocol and candidate admission, operator/runtime behavior,
  empirical-study integrity, governance and legality) plus legal synthesis.
- This ADR records the owner decision. It does not authorize participant mutation, candidate
  creation, tag, release, or rollout; those remain gated by the exact AK tasks defined in the RFC.

## Decision

Adopt **Model A** as a two-layer semver `v1.0` contract:

1. a **public product constitution** defining the stable v1 surface, compatibility floor,
   authority boundaries, and owner exit; and
2. a **release-qualification program** requiring cumulative proof of four pillars —
   **Dependable Adoption**, **Federated Interoperation**, **Evidence Calibration**, and
   **Review-Governed Evolution** — without making every fixture, study, adapter, or release
   tool a public API.

Binding properties of the accepted contract:

- **All four pillars are cumulative requirements for `v1.0`.** Strength in one cannot waive
  another; pillars are categorical properties of one product, not delivery versions or an
  average score.
- **Clean pre-v1 break.** `1.0.0` makes no backward-compatibility promise to any `0.x`
  package release: no preserved v0 command syntax, output bytes, package layout, policy
  shape, catalog behavior, downgrade path, deprecation window, or mixed-runtime mode.
  Pre-v1 repositories and records may serve only as owner-approved transition starting
  states, explicitly shipped migration inputs, adversarial/historical fixtures returning
  structured `unsupported`/`incomplete` results, or immutable evidence.
- **Compatible evolution within v1.** After the accepted v1 baseline, v1.x follows the
  RFC's compatibility rules: patches correct behavior, minors add optional behavior,
  removal or semantic contraction waits for a major decision, documented
  parser/schema acceptance guarantees can tighten but never be lowered.
- **Package semver and protocol identifiers are independent namespaces.** Retained
  identifiers such as `*-v1` must either keep their already-declared meaning and be
  ratified into the v1 manifest or be replaced by a new unambiguous identifier.
- **Default-deny classification.** Unlabeled documented consumer-facing surfaces default
  to public stable; experimental/pilot, internal qualification, and owner-adapter classes
  are defined in the RFC and frozen at G0-B as the immutable v1.0 compatibility baseline.
- **Stable core and adapter membrane.** Portable core readers consume only canonical v1
  envelopes; conversion happens once at bounded ingress; loss of identity, authority,
  provenance, or critical fields yields `unsupported`, never guessed state.
- **No v2+ definition.** This contract defines no v2/v3/v4; an incompatible public-contract
  change requires a new major-version decision.
- **Initial proof scope** is independently governed AI Society owner groups; no external
  organization is required, and public portability remains mandatory.

Qualification proceeds through the RFC's gate structure: G0-A1 (accepted-decision membrane,
satisfied by this ADR), G0-A2 (protocol/population/owner-task admission), G0-A3
(candidate-preparation admission), G0-B (immutable release candidate), G1–G4 (four-pillar
proofs), and G5 (cumulative evidence fan-in that is never release authority). Release and
publication remain a separate exact task and operator approval after G5.

## Alternatives rejected

- **Stable core v1 with calibration/governance outside release qualification** — rejected
  because evidence-bounded improvement and reversible multi-owner evolution are advertised
  product properties; certifying only the core would narrow the product claim rather than
  prove it.
- **Remain pre-v1 and mature pillars independently** — rejected; it withholds a stable
  consumer constitution after the product already exposes substantial adoption and protocol
  surfaces.
- **One major version per pillar or compensation across pillars** — rejected; pillars are
  categorical properties, not delivery versions or an average score.
- **Declare v1 from existing v0.10.0 mechanisms** — rejected; mechanism breadth is not
  complete operator, federation, calibration, or lifecycle proof.
- **Require an external organization** — deferred, not rejected; the initial conditional
  claim is limited to independently governed AI Society owner groups.

## Review disposition

Five review rounds (RFC plus R2–R5) ran under strict convergence with multi-lane synthesis.
R2–R4 each closed `revise_rfc` with concrete defects; every prior attempt remains immutable
history. R5 closed `ready_for_adr` from five independent specialist lanes reviewing the
exact frozen digest, with no blocker and no open cross-lane contradiction. The legal review
closure, artifacts, and digests are recorded on decision 128.

Two disclosed non-blocking observations from the accepted round:
- plain `uv sync --locked` is affected by external global uv configuration
  (`exclude-newer`), so isolated locked validation is the repo's evidence channel;
- `ak decision review-lineage --check` still fails over four pre-existing missing historical
  governed-cognition source files, unrelated to this decision's own lineage.

## Consequences

Positive:

- `v1.0` becomes a trustworthy cumulative claim: complete operator journeys, bounded
  cross-owner interoperation, prospectively calibrated evidence advice, and reversible
  governed evolution, each proven rather than implied by mechanism breadth;
- consumers get an explicit compatibility constitution with default-deny classification,
  exact acceptance guarantees, and a clean break from pre-v1 ambiguity;
- owner authority stays distributed: participant owners keep execution, validation,
  adoption, rollback, and landing authority; engineering-core never absorbs them;
- rejection or failed proof leaves `v0.10.0` current — the contract cannot coerce owners
  or manufacture readiness.

Costs:

- v1.0 requires substantial bounded execution: protocol/harness authoring, participant
  admission, a candidate freeze, four-pillar proofs, and evidence fan-in before any release;
- the release date depends on independent owner groups and an empirical owner, not only on
  engineering-core;
- qualification tooling must stay isolated from the public semver surface, and every future
  v1.x release must diff against the frozen compatibility baseline.

## Execution authority

The accepted execution graph is the RFC's AK execution shape. Post-ADR tasks already linked
to decision 128 cover the four proof protocols, owner-canary handoffs, the release-candidate
freeze, and the cumulative readiness assessment; the implementation plan and
validation/rollout/rollback projections under `docs/project/` bind them to gates and
validation contracts. Every arrow is an AK dependency/task gate; deferrals cannot waive it.
Cross-repo tasks exist only in owning repos after owner acceptance.

## Rollback

- Rejection or failure leaves `v0.10.0` current with lineage preserved or defer-closed;
  a failed pre-release candidate stays isolated, and fixes create a new candidate with
  impact-matrix reruns.
- The RFC's universal stop rules apply immediately to disclosure, unauthorized
  transfer/execution/egress, permission bypass, path escape, fabrication, substitution,
  surviving processes, undeclared effects, authority promotions, task drift, or unbound
  proof.
- G1 restores or quarantines replicas without pretending Git reverses external effects;
  G3 failure leaves evidence advice experimental; G4 preserves evidence-supported
  dispositions; a public tag, once created, is never retargeted or reused.
