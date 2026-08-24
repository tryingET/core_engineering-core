---
summary: "G0-A3 candidate-admission record: binds G0-A2 freezes, G4-A revise lineage, and the exact candidate-preparation task 4876. Does not create a 1.0.0 candidate."
read_when:
  - "Claiming or executing task 4876 (G0-B candidate freeze)."
  - "Checking whether G0-A3 has released candidate preparation."
type: "implementation-plan"
---

# G0-A3 candidate-admission record

Controlling contract: RFC R5 G0-A3. Harness: `scripts/v1/g0a3_admission.py`.
Record: `docs/project/v1-g0a3-admission.json`.

## Fan-in that this record binds

- G0-A2 admission (decision 134) and every freeze digest it already bound
- Population rev 2 (decision 131) and G3 protocol (decision 132)
- Implementation authoring tasks 4871–4875 (done)
- Three G4-A live cycles (4952–4954) with content-owner **revise** (4956);
  **zero** accepted shared-content landings
- Exact candidate-preparation task: **4876**
- Permitted effect/path allowlist: 4876's existing scope only
- Target channel: isolated non-`main` proof branch (named, not created here)

## What this gate releases

One candidate-preparation task (4876) on an isolated non-`main` channel.
4876 may fill declared candidate-only fields and must not merge, tag, publish,
or claim PASS.

## What this gate does not do

- Does not set package version `1.0.0`
- Does not create the candidate commit or branch
- Does not run G1–G4 journeys
- Does not treat revised G4-A pilots as accepted catalog landings
