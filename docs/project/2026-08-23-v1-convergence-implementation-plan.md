---
summary: "Implementation plan binding the accepted v1.0 convergence contract (ADR 2026-08-23) to AK task gates, execution order, and required future decisions."
read_when:
  - "Claiming, sequencing, or closing any v1.0 convergence task under decision 128."
  - "Deciding which task or decision releases the next convergence stage."
type: "plan"
---

# Implementation plan — engineering-core v1.0 convergence execution

## Authority

- Decision: AK `128`, outcome **accepted**; ADR `docs/adr/2026-08-23-v1-convergence-contract.md`.
- Contract of record: `docs/rfc/2026-08-23-v1-convergence-contract-r5.md`
  (SHA-256 `d8a17d69b12d9235de75e123acb28362876f0062d504ac45d991cec15736b5e4`).
- Direction: `AK.V5.SF01` (active), linked through the decision's execution tasks.
- This plan binds the RFC's gate structure to concrete AK tasks. It does not waive or
  reinterpret any RFC rule; on any conflict the RFC and AK runtime state win.

## Stage-to-task mapping

### G0-A1 — accepted-decision membrane (complete)

Satisfied by decision 128 acceptance, this ADR, legal review closure, and the direction
link. G0-A1 releases exactly the authoring tasks below; it authorizes no participant
mutation, empirical or gate outcome capture, candidate creation, PASS claim, publication,
or rollout.

| Task | Title | Gate released by G0-A1 | Scope anchor |
|---|---|---|---|
| `4871` | Build the v1 dependable-adoption proof protocol and harness | G1 authoring | `docs/plans/2026-08-23-v1-dependable-adoption-proof.md`, `scripts/v1/dependable_adoption.py`, `tests/test_v1_dependable_adoption.py` |
| `4872` | Build the v1 federated-interoperation conformance protocol | G2 authoring | `docs/plans/2026-08-23-v1-federated-interoperation-proof.md`, `scripts/v1/federated_interoperation.py`, `tests/test_v1_federated_interoperation.py` |
| `4873` | Define the v1 evidence-calibration empirical handoff | G3 handoff definition | `docs/plans/2026-08-23-v1-evidence-calibration-handoff.md`, `scripts/v1/calibration_manifest.py`, `tests/test_v1_calibration_manifest.py` |
| `4874` | Build the v1 review-governed evolution proof protocol | G4 authoring | `docs/plans/2026-08-23-v1-review-governed-evolution-proof.md`, `scripts/v1/governed_evolution.py`, `tests/test_v1_governed_evolution.py` |
| `4875` | Prepare bounded v1 owner-canary handoffs and population manifest | G0-A2 population input | `docs/plans/2026-08-23-v1-owner-canary-handoffs.md`, `docs/project/v1-proof-population.json` |

Tasks 4871–4875 author frozen protocols, harnesses, oracles, fixtures, and the population
manifest input. They MUST NOT set `1.0.0`, form a candidate, capture G1–G4 outcomes,
mutate participants, publish, or claim PASS.

### G0-A2 — protocol, population, and owner-task admission (next gate)

After 4871–4875 complete, G0-A2 additionally requires:

- an accepted **qualification-population decision** replacing the provisional candidates
  with the reviewed `docs/project/v1-proof-population.json` manifest and digests;
- every participant owner's recorded acceptance of an exact scoped task, with declared
  validation, custody, transfer, isolation, rollback, and final proof-workspace posture;
- the separately accepted **G3 prospective empirical protocol decision** held by the
  empirical owner before any development-arm, forecast, or confirmatory output;
- frozen compatibility-manifest schema/inventory, oracles, fixture templates, impact
  matrix, rendered-product schema, and gate-conformance source under the RFC's rules;
- AK dependency edges (not titles, notes, or deferrals) making G0-A3 depend on every
  convergence-implementation, G4-A owner, content-owner, and review task.

G0-A2 releases bounded **convergence-implementation** tasks (to be created at that gate
with exact scopes) and separately owner-accepted **G4-A pilots** in participant repos.

### G0-A3 — implementation and candidate-preparation admission

After all G0-A2 implementation and G4-A production/review/disposition tasks complete, the
read-only G0-A3 verifier emits the immutable candidate-admission record that releases one
exact candidate-preparation task on an isolated non-`main` branch. That task performs only
the admitted source transition and pushes one immutable proof commit.

### G0-B — immutable release candidate

| Task | Title | Gate |
|---|---|---|
| `4876` | Freeze the exact engineering-core 1.0.0 release candidate | G0-B (candidate materialization, manifests, synchronization; admits no tag/release) |

Task 4876 remains blocked until the G0-A3 admission record exists; its current scope paths
(final metadata, catalogs, changelog, support policy, lockfile) are exactly the
G0-B candidate-only surface. It MUST NOT merge to `main`, tag, or publish.

### G1–G4 production/review and G5 fan-in

| Task | Title | Gate |
|---|---|---|
| `4877` | Assess cumulative engineering-core v1 readiness without releasing | G5 (evidence fan-in; never release authority) |

G1–G4 production and review tasks run after G0-B against the exact candidate, each bound
to one candidate/population digest. G5 (4877) fans in their PASS artifacts, independent
reviews, and AK dependency edges. Release, publication, and post-release verification
require separate exact tasks and operator approval after G5 — none exist yet and none are
created by this plan.

## Required future decisions (not yet created)

1. **Qualification-population decision** — replaces provisional candidates; freezes the
   population manifest and its canonical digest (G0-A2 precondition).
2. **G3 prospective empirical protocol decision** — held by the empirical owner; freezes
   power, weights, thresholds, forecasts, harm stops before any output (G0-A2 precondition).
3. **Any G4-A content promotion decisions** — content-owner decisions per live cycle,
   completed before G0-B.
4. **Release decision** — only after G5 PASS; opens the serialized release window.

Each decision requires its own accepted AK record; this plan names them, it does not
pre-accept them.

## Sequencing summary

```text
[done] G0-A1: decision 128 accepted + ADR
  -> 4871–4875 (authoring)                      [ready after this plan]
    -> qualification-population + empirical
       protocol decisions; participant owner
       acceptance                              [G0-A2 preconditions]
      -> G0-A2 admission
        -> convergence-implementation tasks
           + G4-A pilots                        [created at gate]
          -> G0-A3 admission record
            -> candidate-preparation task       [created at gate]
              -> 4876 (G0-B candidate)
                -> G1/G2/G3 + G4-B production
                  -> 4877 (G5 fan-in)
                    -> separate release task
                       + operator approval
```

## Constraints carried from the RFC

- All four pillars are cumulative; no task may trade one against another.
- Engineering-core is producer/validator only; it cannot count as a positive adopter,
  execute participant commands by default, or convert supplied evidence into approval.
- Default-deny transfer and custody govern every cross-owner byte movement.
- Drift restarts affected proof; failed studies and counterevidence stay in lineage.
- No task may relabel observed failure, waive a required journey, or claim PASS outside
  its gate's machine-decidable envelope.
