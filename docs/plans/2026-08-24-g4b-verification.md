---
summary: "G4-B non-mutating verification of the 1.0.0 candidate: inclusion map, revise lineage, deterministic suite replay."
read_when:
  - "Checking whether Gate G4 has passed after G4-A revise cycles."
  - "Replaying G4 lifecycle fixtures against candidate fa7c9a9."
type: "implementation-plan"
---

# G4-B verification

Candidate: `proof/v1-candidate-3` `7a41ea321015c6a5210d6ea26b6f3e5ac6632045`.
Harness: `scripts/v1/g4b_verify.py` (does not modify the frozen G4-A harness).

## Checks

- Candidate commit exists, is not `main`, `v1.0.0` tag absent
- Accepted G4 content map is empty (no promotions landed)
- Three G4-A cycle files still validate and keep their frozen digests
- Deterministic 12-case transition suite replays with the frozen legal table
- Rollback fixture restores prior selection without erasing history

No candidate bytes, catalog, or shared content are changed.
