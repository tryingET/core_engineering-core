---
summary: "Engineering-core content-owner decisions over G4-A live cycles: v2 differentiated dispositions (revised / owner_local_diagnosis / revised+follow-up), v1 lockstep records superseded as history."
read_when:
  - "Checking G4-A completion before G0-A3 or G0-B."
  - "Deciding whether a G4-A candidate may become default shared content."
type: "plan"
---

# G4-A content-owner decisions

Authority: engineering-core is the sole shared-content owner. Participant
dispositions cannot land catalog, lane, discipline, or template changes.

## V2 cycles (2026-08-24, task 5036) — current

Judgment over the three re-originated participant cycles (AK 5018/5019/5020,
distinct owner-repo claims, digest-bound evidence, no pre-filled decision —
origination rule satisfied and mechanically verified before judgment).
Dispositions are differentiated per cycle on merits; promotion was considered
and rejected on structural grounds for each (frozen promotion rules require ≥2
distinct positive owner groups with a non-originator; each cycle has exactly one
origin group and no completed cross-group pilots). This is not a pre-declared
quota and no G4 PASS is claimed here.

| Cycle | Origin | Verified evidence basis | Content-owner decision | Why |
|---|---|---|---|---|
| `cycle-holdingco-coordination-nonclaimable-v2` | holdingco (5018) | live `fcos status --json`: board sha256 `10135081…`, six actionable items all `coordination_only=true`/`claimable=false` | **revised** | Real, currently-true invariant; single origin group; EC doc adoption only after a second owner group's coordination surface repeats the need |
| `cycle-teachingco-g1-already-adopted-refusal` | teachingco (5019) | `g1-run.json` sha256 `3d5132a2…` (6 pass / 1 fail / 3 incomplete, `g1_pass_claimed=false`) + digest-bound admission/baseline | **other_disposition** (owner_local_diagnosis) | Not a shared-content candidate: documents already-adopted owner-local scoring for a released-match repo and requests no shared change; retained as TeachingCo canary, review 2026-09-30 |
| `cycle-softwareco-g1-scanner-completeness-is-not-active-resolution` | softwareco (5020) | `g1-run.json` sha256 `0f06c6cf…`: `prove_active_resolution` passed from scan completeness while `init --apply` exited 2 (`applied=false`) and doctor blocked | **revised** + EC follow-up task **5037** | Real engineering-core G1 journey-semantics gap acknowledged: scanner completeness is diagnostic, never proof of active resolution; follow-up binds `prove_active_resolution` to owner-apply polarity on the candidate line |

Decided records: `content_owner_decision` + `final_state` appended to each
participant `docs/v1-proof/g4a-cycle-v2.json` (participant fields untouched;
originated-record sha256 bound in `preserved_lineage`). Frozen harness
`validate-cycle` **pass** for all three — decided digests `d7081a6f…`,
`a7de8b71…`, `74abfae0…`. Historical 4952–4954 remain non-qualifying; G4-B
rebinding to the v2 lineage belongs to the later G4-B production/review task,
not to this judgment.

## V1 cycles (2026-08-23) — superseded, retained as history

Review event / expiry for all three pilots: **2026-09-30**. None may become
default silently. Superseded 2026-08-24 by the independence review
(`v1-g4-independent-review-synthesis.md`) and the origination rule: these
controller-authored cycles are non-qualifying and the v2 cycles above are the
live records.

| Cycle | Origin | Candidate | Participant disposition | Content-owner decision | Why |
|---|---|---|---|---|---|
| `cycle-holdingco-pin-drift` | holdingco | owner-environment pin drift vs adoption failure | supports, pilot only | **revised** | Real evidence (fcos substrate pin mismatch). Not yet a shared default; keep as bounded pilot. |
| `cycle-teachingco-minimal-validation` | teachingco | minimal validation contract for teaching repos | supports, pilot only | **revised** | Matches observed mathe/wib admission. Needs a second uncoached teaching repo before any template sentence. |
| `cycle-softwareco-package-scopes` | softwareco | package-local validation scopes | supports, pilot only | **revised** | Matches observed monorepo gate/package split. Do not add a G1 field until a second monorepo repeats the need. |

Harness: each cycle JSON `validate-cycle` **pass**; rollback transition fixture
**pass**. No candidate was promoted. No shared `src/`, catalog, or template
bytes were changed. Negative/pilot lineage is the cycle records themselves.

G0-B must not treat these as accepted G4 content landings. They are completed
cycles with evidence-supported **revise** dispositions.
