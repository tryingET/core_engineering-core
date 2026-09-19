---
summary: "G4-B non-mutating verification of the 1.0.0 candidate: inclusion map, revise lineage, deterministic suite replay."
read_when:
  - "Checking whether Gate G4 has passed after G4-A revise cycles."
  - "Replaying G4 lifecycle fixtures against candidate fa7c9a9."
type: "implementation-plan"
---

# G4-B verification

Candidate: `proof/v1-candidate-4` `bc43bb972121bf6c02792bf318cb14aa974b7e17`.
Harness: `scripts/v1/g4b_verify.py` (does not modify the frozen G4-A harness).

## Checks

- Candidate commit exists, is not `main`, `v1.0.0` tag absent
- Accepted G4 content map is empty (no promotions landed)
- Three G4-A cycle files still validate and keep their frozen digests
- Deterministic 12-case transition suite replays with the frozen legal table
- Rollback fixture restores prior selection without erasing history

No candidate bytes, catalog, or shared content are changed.

## Unit/CI conformance versus live historical verification

Ordinary CI does not possess the unpublished candidate branch or the three
participant-owned workspace cycle files. Unit tests must not depend on those
ambient resources or publish them merely to make CI green.

`tests/test_v1_g4b_verify.py` exercises the unchanged verifier in a temporary,
synthetic Git workspace supplied by `tests/g4b_fixture.py`. It substitutes only
the test's candidate SHA and lineage bindings; actual Git queries, cycle
validation, digest comparisons and transition replay still execute. The fixture
has distinct candidate/main commits and three synthetic cycle files under
sibling-shaped paths confined to that temporary workspace. No live participant
record is copied. Missing/drifted refs, a release tag, missing cycle files and
changed on-disk cycle content must still fail.

Separate unpatched tests compare emission against the full checked-in historical
record and exercise the actual subprocess CLI's refusal when its historical
candidate is unavailable. Positive CLI argument parsing and serialization are
tested through `main()` with explicitly synthetic bindings, not represented as
a live historical CLI pass. A passing unit suite proves conformance behavior;
it does not requalify Gate G4 or establish current historical evidence custody.

The live verifier is unchanged and remains an explicit workspace operation:

```bash
python scripts/v1/g4b_verify.py validate docs/project/v1-g4b-verification.json \
  --repo-root .
```

That command still requires the exact frozen branch and participant records and
fails closed when they are absent. Do not skip its checks, invent matching refs,
substitute synthetic results for historical evidence, or automatically fetch and
publish cross-owner artifacts. AK5778 repairs test isolation only.
