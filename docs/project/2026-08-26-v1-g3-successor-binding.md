---
summary: "Operator-accepted binding: G3 successor instrument targets candidate-5 (main@cde7f14); gate records stay candidate-4; G3 reopened as successor instrument."
read_when:
  - "Executing or reviewing the G3 successor campaign (AK 5095) and its candidate identity."
  - "Reconciling G3 gate lineage (candidate-4) with the successor instrument (candidate-5)."
type: "decision-record"
---

# G3 successor instrument binding (2026-08-26, AK 5096)

**Status: ACCEPTED (operator, 2026-08-26 — "accept both").**
**Companion DSPx-side acceptance:** successor empirical protocol, conditioned
on this binding (replaces the superseded-intent decision 137; DSPx evidence
note documents that sequence).

## What is bound

1. **Candidate identity for the G3 successor instrument = candidate-5**:
   engineering-core `main@cde7f142ebd07527d865eded4bbbadf9fda9409f`,
   wheel `engineering_core-0.10.0-py3-none-any.whl`,
   sha256 `921bff5ef60ee8dea112cdaf8825e809bb484f1e518a06080e853c7e52288ab0`.
   This is the AK-5082 advise-surface fix commit (uniform falsification
   grammar, self-describing request contract, shipped SKILL.md grammar).
2. **G3 is reopened as a successor instrument** per
   `softwareco/owned/dspx/docs/v1-proof/g3-successor-campaign-design.md`
   (12 convention-space tasks × 2 families × 3 reps = N=72 pairs, 144
   executions max, pooled exact McNemar pre-registered criterion, one
   pre-registered interim look at N=48, anti-circularity corpus rules,
   runner hardening AK 5092 as hard precondition).

## Scope discipline (what does NOT move)

- **Gate records stay candidate-4.** G1 (40/40), G2, G4-B records and their
  digests bind `bc43bb9` / `proof/v1-candidate-4` and remain the closed G0–G4
  lineage. The successor instrument is a *new* binding for the G3 question
  only; it does not rewrite, re-emit, or supersede any frozen gate record.
- G5 (4877) remains closed with its recorded verdict; a successor G3 PASS/FAIL
  would require a new fan-in task to be consumed, not an edit to the record.
- Construct boundary travels unchanged from the design doc: the instrument
  measures **convention-conformance lift** — a necessary, not sufficient,
  proxy for engineering value.

## Evidence basis (diagnostic, n=1 per cell — grounds for pinning, not causal proof)

- v3 pilot (AK 5081): separation 6/10 tasks on contract-conformance tasks.
- 5082 investigation (evidence 7809): falsification array-vs-string grammar
  asymmetry + zero shipped schema documentation; glm evidence-arm degradation
  attributed substantially to presentation defect.
- v3b (AK 5085, evidence 7839, commit 5516ee65): glm evidence recovery on both
  v3-failure pairs (A2 0→1, B2 0→1; family 1/5→3/5); sol B1/B3 held (4/5
  v3 wins held; C1 regressed). Honest caveat: fix + wheel identity confounded;
  the successor campaign's single-variable design is the mitigation.

## Revert path

Repin to `bc43bb9` + re-freeze guidance bundles/checker pins (v3 freeze intact
and reproducible). No campaign data invalidated in either direction.
