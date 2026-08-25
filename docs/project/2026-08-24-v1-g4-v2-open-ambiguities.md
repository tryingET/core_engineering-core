---
summary: "Open ambiguities, accepted debt, and resolved-by-verification items after the 2026-08-24 G4 v2 closure wave (tasks 5036/5037/5039/5043)."
read_when:
  - "Before claiming G4 PASS, running G5 fan-in, or re-emitting any v1 admission/verification record."
  - "When deciding whether a G4-A participant cycle counts toward gate population or promotion."
type: "reference"
---

# v1 G4 v2 open ambiguities and debt register (2026-08-24)

Context: the 2026-08-24 wave re-originated the G4-A cycles (5018/5019/5020),
made differentiated content-owner decisions (5036), bound G1
`prove_active_resolution` to owner-apply polarity (5037), rebound G0-A3
admission (5039) and G4-B verification (5043) to the v2 state. This register
records what remains genuinely undecided, deliberately deferred, or resolved
by verification rather than by design.

## Open ambiguities (need an owner decision later; none blocks current records)

1. **Does the TeachingCo `other_disposition` (owner_local_diagnosis) cycle
   count toward G4 gate population?** The origination rule requires each
   positive owner group to originate one substantial candidate; TeachingCo
   originated, but its cycle explicitly requests no shared-content change.
   Working interpretation: it counts for *origination-independence* proof but
   not as a shared-content candidate. Final counting belongs to the G5 fan-in
   / any future G4 PASS review — do not pre-decide it here.
2. **Promotion-group semantics.** The v2 cycles declare `pilot_groups`, but no
   cross-group pilots were executed. Working interpretation: declared pilot
   groups can never satisfy the frozen promotion rule ("≥2 distinct positive
   owner groups, non-originator"); only a real repeated need observed by a
   second group can. No promotion was granted on declaration, and none may be.
3. **G0-A3 `base_commit` drift.** The admission record still names
   `d761bba` as base while `main` has advanced through the v2 closure commits.
   The record's semantics (base for the candidate transition) were emitted at
   G0-A3 time and candidate-3 was frozen from a later `main` (task 5016).
   Whether the eventual release-path candidate task must re-emit the
   admission record is an open sequencing decision; validators do not check
   `base_commit` against `main`.
4. **`g1_run.py` `CANDIDATE_COMMIT` pins `b313bec`.** The historical four-baseline
   fan-in is deliberately immutable, but the runner as-is will label any *new*
   run against the old candidate. Re-pinning belongs to the later G1
   production task against the frozen candidate; until then new runs would
   need an explicit pin decision.
5. **4974 AK result immutability.** Task 4974's result still binds
   `eddc79c`/`fa7c9a9` (candidate-1 era). AK results are history; the
   correction is additive evidence 7724 pointing at the current chain
   (5017 `dbc6d2f` → 5043 rebind). Do not rewrite the result row.

## Accepted debt (tracked, bounded)

- **Participant schema-string variance (historical).** The three v2
  participant files were authored with three different `schema` strings
  (`…g4/1`, `…g4a-owner-cycle/2`, `…g4-participant/1`). EC normalized to
  `engineering-core.v1.g4/1` when appending the decision (the only schema the
  frozen harness validates). Variance is frozen history; future participants
  should emit `g4/1` directly.
- **`g0a3`/`g4b` rebind law lives in validators, not a shared module.** The
  `LINEAGE_LAWFUL_DISPOSITIONS` constant now exists in both
  `g0a3_admission.py` and `g4b_verify.py`. Extracting it into
  `governed_evolution.py` would be cleaner but changes a frozen harness;
  deferred until a harness revision is otherwise required.

## Resolved by verification (not ambiguity; recorded to prevent re-litigation)

- `release-local.py verify` was **not** run for tasks 5036/5037/5039/5043:
  verified fact — the built wheel contains zero `scripts/v1` entries
  (`source-include` ships only the four dogfood scripts), so these changes
  are not package-visible and not release-affecting.
- G4-B machine-local absolute lineage paths and cwd-relative resolution:
  removed in 5043 (workspace-relative paths resolved against `--repo-root`,
  regression-tested from a foreign cwd).
- Independent-review must-fix 3 (suite-digest drift/omission fail-closed) was
  already implemented in `g4b_verify.py` (`suite_digest_mismatch`) — verified,
  no work owed.
- G0-A3/G4-B hardcoded `disposition == "revised"` lineage law (review
  must-fix 5 defect class): replaced with lawful non-promoted disposition
  sets in both validators (5039, 5043), each with promotion-still-rejected
  regression tests.
