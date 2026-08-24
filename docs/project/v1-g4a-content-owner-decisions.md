---
summary: "Engineering-core content-owner decisions for the three G4-A live cycles: all revised, none promoted, lineage preserved."
read_when:
  - "Checking G4-A completion before G0-A3 or G0-B."
  - "Deciding whether a G4-A candidate may become default shared content."
type: "plan"
---

# G4-A content-owner decisions

Authority: engineering-core is the sole shared-content owner. Participant
dispositions cannot land catalog, lane, discipline, or template changes.

Review event / expiry for all three pilots: **2026-09-30**. None may become
default silently.

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
