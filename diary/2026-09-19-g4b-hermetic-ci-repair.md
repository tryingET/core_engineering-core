---
summary: "AK5777/5778: replace ambient G4B test dependencies with confined synthetic Git/cycle fixtures without changing historical verification."
read_when:
  - "Diagnosing candidate_missing in GitHub CI or distinguishing G4B unit proof from live historical qualification."
type: "evidence"
---

# G4B hermetic CI repair

## Reproduced failure

GitHub CI run `35436600335` at `8bb532ff956a2edd1a3b4aef86b840a0370deac1`
failed G4B validation tests while package-smoke passed. Diagnosis AK5777 reproduced
13 focused tests with seven failures and one error in a `--no-local
--single-branch --branch main` clone. The clone had no candidate ref or sibling
participant repositories. AK evidence 10081 retains the baseline.

The tests invoked the live historical validator against the source checkout.
That validator requires local `proof/v1-candidate-4` at its frozen SHA and three
participant-owned cycle files outside this repository. Local success therefore
depended on workspace state unavailable to CI. Fetching a branch would not fix
the missing cycle-file dependency and could accidentally publish private proof
artifacts. Skipping checks would weaken coverage.

## Bounded repair — AK5778

Only tests, their synthetic fixture helper and explanatory docs change:

- `tests/g4b_fixture.py` creates an isolated temporary workspace, a real Git repo
  with distinct main/candidate commits, and three valid synthetic cycle files.
  Paths are checked before writing; user Git hooks, signing and inherited Git
  overrides cannot affect the fixture. Scoped bindings/environment are restored
  and the temporary workspace is removed even after exceptions.
- `tests/test_v1_g4b_verify.py` substitutes only candidate/lineage data bindings.
  Actual Git lookup, file access, cycle validation, digest checks and transition
  replay execute. Negative cases cover missing/drifted candidate refs, candidate
  equal to main, an actual release tag, each missing/drifted cycle, existing
  lineage and replay failures, and non-mutating validation.
- Historical emission equality is tested unpatched against the entire checked-in
  record. Actual subprocess template/emit tests remain. An unpatched subprocess
  using the historical record must return `candidate_missing` in the isolated
  workspace. Positive CLI parsing/serialization uses in-process `main()` with
  explicitly synthetic bindings, not a claim of historical CLI qualification.

Production scripts, frozen candidate refs, historical JSON, source doctrine,
workflow files, dependency/lock/version surfaces and external participant records
are unchanged. No historical artifact is copied or republished. Passing ordinary
CI does not requalify Gate G4 or issue release/publication authority.

## Validation before push

- Isolated main-only clone: 25 focused tests and the full 366-test suite pass.
- Focused suite under `python3 -O`: 25 tests pass.
- Owner checkout: full 366-test suite passes.
- Repo self-check, release lineage, lane addenda, skill sync, bounded adoption
  scan, build and `release-local.py verify` pass.
- All uv validation uses inherited `UV_NO_CONFIG=true` (AK5775 workaround), and
  `uv.lock`/`pyproject.toml` remain unchanged.
- `git diff --check` passes; forbidden production/evidence/workflow paths have no
  diff.

Independent review `dispatch-1789813413713` accepted the test-only design and
implementation. The reviewer independently ran focused tests in both checkouts,
checked confinement and exception-path cleanup/environment restoration, and
confirmed production refs and historical bytes were unchanged. Its optional
confinement-assert concern was resolved by using an explicit exception, followed
by normal and optimized-Python focused reruns.

Reproduction uses the repo-declared `python -m unittest discover -s tests` surface;
the helper is test-only, not packaged runtime or an alternative verifier. The
main-only clone baseline and repaired run use the same production files and
historical record. Post-push GitHub outcome belongs in AK5778 evidence; this note
does not claim that remote CI had passed before the commit was pushed.

## Separately discovered existing defects

The reviewer confirmed these against synthetic fixtures, not live participants:

- AK5780: three copies of the first lineage entry can pass even after the other
  two cycle files are removed; length is checked but distinct coverage is not.
- AK5781: an invalid cycle can raise the governed-evolution module's distinct
  `ValidationError` out of G4B `main()` without structured stderr.

These findings predate this test-isolation repair. They are separate production
fixes; historical evidence and validator semantics were not silently rewritten
under the CI task.
