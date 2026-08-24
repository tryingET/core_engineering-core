---
summary: "G3 evidence-calibration empirical handoff: prospective protocol manifest schema and fail-closed validator; campaign execution stays with DSPx/Oracle."
read_when:
  - "Preparing, reviewing, or validating the G3 prospective empirical protocol under decision 128."
  - "Binding power inputs, model identities, forecasts, privacy classifications, or result bindings for evidence calibration."
type: "implementation-plan"
---

# G3 evidence-calibration empirical handoff

Controlling contract: `docs/rfc/2026-08-23-v1-convergence-contract-r5.md` (Gate G3),
accepted as `docs/adr/2026-08-23-v1-convergence-contract.md`.
Validator: `scripts/v1/calibration_manifest.py` (internal qualification tooling).
Tests: `tests/test_v1_calibration_manifest.py`.

## Authority boundaries

- **The empirical owner (DSPx/Oracle) runs the campaign and the analysis.**
  Engineering-core supplies this manifest schema and validator only. No raw cross-owner
  snapshot is transmitted through engineering-core; validator inputs are protocol
  declarations, never participant data.
- The protocol manifest must be **accepted before any output is visible** — development
  arm, static arm, evidence arm, forecast, or confirmatory. The validator therefore
  treats every measured value as `unassigned` at authoring time and requires the frozen
  set only when `protocol_stage: accepted`.
- Owner dispositions, empirical outcomes, evidence receipts, and governance decisions
  remain distinct record classes; no empirical field may claim release, rollout, or
  doctrine authority.

## Manifest sections (frozen schema)

1. **Population and design** — target population, independent clusters, disjoint
   development/confirmatory split, arm-neutral rubric, objective oracle, exclusions,
   the sole treatment contrast, prompts/context, model set, allocations, executors,
   masking/contamination controls, stopping rule (no optional stopping), scoring
   code/environment, multiplicity/error control.
2. **Power** — smallest effect of practical interest derived from owner decision costs,
   interval/error criterion, separately justified design alternative, prospective
   paired-cluster simulation or exact power analysis, attrition inflation, sensitivity
   to discordance and task correlation, resulting total/per-cell sample. **No fixed
   RFC-invented floor**: the sample follows the accepted analysis, and loss of
   prospective power fails G3.
3. **Weighting** — equal top-level primary-estimand weight per owner group; within each
   owner's fixed unit weight, frozen baseline × model weights summing to one, so adding
   a baseline or model cannot increase any owner's influence.
4. **Model identity** — the same frozen set of at least two distinct base-model
   families/identities in every positive owner group; prompt/seed/temperature/endpoint/
   adapter/quantization variants of one base model do not count as diversity.
5. **Calibration** — metric(s), binning or smooth estimator, interval procedure,
   threshold, missing-forecast treatment, and a disjoint-development reference forecast.
   The probability must be emitted by the evidence-advice surface for its exact `Y`
   outcome before execution/validation/review; a separate forecaster makes the result
   explicitly a forecaster-calibration claim that cannot qualify the advice surface.
   Forecasts stay hidden from outcome reviewers.
6. **Harm and safety** — cell and marginal harm boundaries with sensitivity analysis; no
   aggregate effect can waive a frozen harm stop; a separate insufficient-evidence
   safety set with at least one case in every owner-group × base-model cell, excluded
   from improvement and calibration estimates.
7. **Outcome definition** — `Y[a,i]=1` only when the arm satisfies the same frozen owner
   constraints, participant validation, and objective claim/patch verification rule.
   Evidence use, citation, stored claim, owner preference, pre-v1 preservation, or owner
   disposition never sets `Y`. Intention-to-treat; arm-attributable no-output or failed
   validation is `Y=0`; administrative missingness pessimistically bounded.
8. **Privacy manifest** — per transfer: classification, owner-approved exact bytes/digest/
   length, recipients/endpoint/region, purpose, access/encryption, logs/cache/session,
   retention/deletion, route, adapter/model identity, training-use prohibition, custody,
   readers, capture/review/quarantine state, authenticated owner attestation.
9. **Result bindings** — protocol decision reference, power/sensitivity evidence,
   bounded results, replay/configuration receipt, limitations, masking breaches,
   exclusions, missingness, counterevidence; each bound to the frozen protocol digest.

## Fail-closed validation rules

The validator rejects, among others: missing sections; any measured value assigned at
authoring stage; fewer than two base-model families; same-family variants counted as
diversity; weights not summing to one within an owner; unequal top-level owner weights;
missing power-analysis inputs at accepted stage; a constant reference forecast without
prospective justification; safety-set cells uncovered; forecasts sourced after outcome
visibility; privacy entries lacking owner approval digests or training-use prohibition;
any field blurring disposition/outcome/receipt/governance classes; any optional-stopping
or post-hoc relabeling declaration.

## Rollback

Failed studies remain in lineage. Any protocol change requires a fresh accepted
empirical decision, a held-out corpus, and affected reruns; revisions are prospective
only through decision 128 governance.
