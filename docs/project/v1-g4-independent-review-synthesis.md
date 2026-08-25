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
---

# v2 re-review (2026-08-25, task 5049)

Independent re-reviewer `g4-v2-rereview-5049`. The reviewer did not produce
the v2 repair; every claim below was re-verified against live artifacts
(AK rows, git bytes in three owner repos, session JSONLs, harness runs) —
not taken from producer documentation.

## Lens A — governance/lifecycle legality: **pass**

Origination rule clauses 1–6 checked against the live v2 cycles
(holdingco/fcos-control-board, teachingco/mathe, softwareco/owned/pi-extensions):

1. One cycle per positive group ✓ (exactly one `g4a-cycle-v2.json` per repo;
   wib has G1 artifacts but no cycle — TeachingCo originates once, mathe only).
2. Origin claimed in each owner repo by a recorded `claimed_by` ✓ — verified
   beyond the result JSON: three repo-scoped session JSONLs each contain their
   own claim act (`ak task claim 5018 --agent holdingco-g4a-5018`, 5019/5020
   likewise); none is an engineering-core session.
3. Pairwise distinct `claimed_by` ✓ (holdingco-g4a-5018 / teachingco-g4a-5019 /
   softwareco-g4a-5020; corroborated by evidence rows 7670–7672).
4. Participant disposition precedes the content-owner task ✓ — origin-commit
   bytes (d702dad / 4088c62 / b9705cbb) contain no `content_owner_decision`
   and no `final_state`; task 5036 was created ~8 h later.
5. Digest-bound, no `"see sibling"` refs ✓ (see Lens B).
6. No `revised`-only hardcoding ✓ (see Lens B / must-fix 5).

`governed_evolution.py validate-cycle`: **pass ×3** with decided digests
`d7081a6f…` / `a7de8b71…` / `74abfae0…`. Content-owner decision (task 5036)
lawful: `decided_by=engineering_core_content_owner`, `coerced=false`, task
5036, dispositions differentiated on per-cycle merits; the TeachingCo
`other_disposition` (owner_local_diagnosis) is a lawful disposition with a
correct rationale (nothing shared to revise; promotion structurally
unavailable). Residual (accepted debt D1, on record): EC normalized `schema`/
`stage` strings on two records at decision time; participant fields verified
untouched by byte-diff.

## Lens B — evidence/digest binding: **pass**

Every digest recomputed independently and matched: 3 candidate markdowns
(d4eff767/7d865484/b87f1477, byte counts too), 5 lineage/evidence artifacts
(teachingco g1-run/admission/baseline; softwareco g1-run/admission), the 2
TeachingCo MDR prose refs (engineering.local.md 91ac811a…, tech-stack.local.md
9fa4fc23…), 3 originated-record digests at the origin commits
(57fb85e1/fe3ccb05/3eb90dd1), all 4 G0-A3 bindings, and the live FCOS board
sha256 `10135081…` cited in the HoldingCo decision.

`g0a3_admission.py validate` → pass (admission digest bb5d2a55…);
`g4b_verify.py validate` → pass (verification digest eb0c7b65…, candidate
7a41ea32…, 12/12 suite cases). G4-B `revised_lineage` digests **equal** the
decided-cycle digests from validate-cycle output and task 5036's result.
Fail-closed behavior probed empirically from scratch ($TMPDIR): suite-digest
drift → exit 2 `suite_digest_mismatch`; omitted case → exit 2
`suite_incomplete`; promoted disposition → exit 2 `invalid_lineage` (lawful
set = revised/rejected/deprecated/retired/other_disposition). Illegal-case
polarity tests present; 40/40 pass in the two v1 harness test modules.

## Lens C — independence/anti-coercion: **pass** (one flag)

Independence verified at session level: three distinct repo-scoped session
files launched 2026-08-24T20:30:55Z (parallel dispatch), each performing only
its own claim, each committing in its own repo (d702dad / 4088c62 / b9705cbb1).
No pre-filled decisions (verified at origin bytes). Dispositions are
differentiated (revised / other_disposition / revised+follow-up 5037), not a
quota; promotion was considered and rejected on structural grounds per cycle.

Q1/Q2 assessment (`2026-08-24-v1-g4-ambiguity-resolutions.md`): Q2
(declarations confer no promotion standing) is anti-coercive and consistent
with frozen rules. Q1 (other_disposition counts for origination population)
is framed as a position awaiting restatement/ratification in a future PASS
record, with the contingency (2/3 + third origin owed) explicitly preserved —
advisory, not coercive. **Flag:** Q1-yes is structurally pre-embedded in the
frozen validators (exactly-3 lineage entries), so a future review adopting
the stricter reading must re-freeze harness/records rather than merely write
a sentence. That is ratification inertia, not coercion of any review act;
the register itself demands confirm-or-overturn with reasons.

## Must-fix closure (v1 list)

1. **Re-origination from claimed owner-repo sessions** — closed (Lens A/C).
2. **Digest-bound sibling/lineage artifacts** — closed (Lens B).
3. **Suite-digest drift/omission rejection + illegal-case polarity tests** —
   closed (Lens B, probed).
4. **4974 rebinding** — closed via successor + additive correction per the
   ratified Q5 convention: result row left immutable (history), evidence 7724
   (task_ref 4974) is the authoritative correction pointer; current chain is
   5017 (dbc6d2f → candidate-3 7a41ea3) → 5043 (v2 lineage, eb0c7b65…). The
   v1-named pair 481d5ef/c97b7209 was itself superseded by the v2 rebind.
5. **No all-revise quota / no `revised`-only legality** — closed (Lens A/B).

## Overall verdict

**g4_pass_consideration_earned: yes.** All five must-fixes are closed against
live evidence. Remaining revise list: **none blocking**. Advisory carry-forwards
for the G4 PASS / G5 review: (a) explicitly confirm-or-overturn Q1 population
counting with reasons, noting the exactly-3 harness coupling; (b) D1
schema-string debt norm already on record; (c) the three origin tasks were
bulk-created and parallel-dispatched within seconds by a controller —
legitimate here because distinct-session origination held, but task-creation
guardrails are worth considering if the pattern repeats; (d) 4974 consumers
must follow evidence 7724, not the stale result row.

## Explicitly not claimed (v2)

No G4 PASS granted by this re-review; G5 consumes this verdict. No G1–G3,
tag, `main` update, or promotion.
