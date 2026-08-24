---
summary: "Independent three-lens review of Gate G4 after G4-B. Formal pillar PASS is not granted."
read_when:
  - "Deciding whether G4 has passed or whether G4-A cycles must be re-originated."
type: "review"
---

# G4 independent review synthesis

Dispatched 2026-08-24. Producer/controller did not score the gate.

| Lens | Dispatch ID | Outcome |
|---|---|---|
| Governance / lifecycle legality | `dispatch-1787587764212` | **revise_before_pass** |
| Evidence / digest binding | `dispatch-1787587764214` | **revise_before_pass** |
| Independence / anti-coercion | `dispatch-1787587764216` | **reject_g4_claim** |

## Combined verdict

**reject_g4_claim** for formal pillar PASS on the current live-cycle package.

G4-B harness checks (candidate tip, empty inclusion map, 12/12 suite polarity,
three live cycle *JSON* digests) are real and currently green. They do not
overcome: (1) producer-authored lockstep “owner” cycles, (2) suite digests not
fail-closed, (3) MDR/lineage path-only binding, (4) task 4974 result SHA
misbound to `eddc79c` instead of G4-B commit `481d5ef`.

These reviews satisfy universal rule 9 **for this review act only**. They do
not convert the 4952–4954 cycles into independently governed origination.

## Must-fix before any later G4 PASS attempt

1. Re-originate live cycles from **claimed owner-repo sessions** (not one
   controller writing three packs in one minute). Keep TeachingCo at one
   origin (mathe only) — that counting is lawful.
2. Bind sibling `g4a-candidate.md` and lineage artifacts by content digest,
   not `"see sibling"` / name-only refs.
3. Make `g4b_verify.py` reject suite-digest drift/omission; test illegal-case
   polarity.
4. Rebind task 4974 (or a successor) to commit `481d5ef` and verification
   digest `c97b72094c16b2cf57fa2be49b2bc747e17ed91c66b66b2606e78e7f955ee81c`.
5. Do not treat all-revise as a pre-declared quota; do not hardcode
   `disposition==revised` as the only G4-B-legal live outcome.

## Explicitly not claimed

G1, G2, G3, G5, tag, `main` update, or “G4 PASS.”
