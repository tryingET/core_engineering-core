---
summary: "EC positions answering the v1 G4 v2 open-ambiguity register (Q1-Q5, D1-D2) via multi-lens analysis; recommendations on record, gate ratification points unchanged."
read_when:
  - "Before G5 fan-in, any G4 PASS attempt, or any re-emission of G0-A3/G4-B/g1_run records."
  - "When deciding gate-population counting, promotion standing, or result-correction conventions."
type: "reference"
---

# v1 G4 v2 ambiguity resolutions (2026-08-24, task 5044)

Method: each question is attacked with several independent reasoning
frameworks (first principles; Goodhart/incentive design; Chesterton's fence;
adversarial red-team; append-only audit integrity; maximin decision theory;
in-program precedent) and the positions that survive all applied lenses are
recorded. Authority status: these are **engineering-core positions on
record**, solicited by the operator 2026-08-24. They are not G4 PASS claims,
not G5 inputs-final, and not promotions. Where a gate review must still
ratify, that is stated.

## Q1 — Does the TeachingCo `other_disposition` cycle count toward gate population?

**Position: yes — for origination-population (independence proof); no — as
shared-content candidacy. Population counting and content candidacy are
different axes.**

- *First principles:* the population requirement exists to prove independent
  origination capability, not content quality — content quality is the
  content-owner decision's job (which then differentiated the three
  dispositions). The frozen template's own words support this reading:
  `each_originates_one_substantial_candidate` — the verb is *originates*;
  "candidate" is the cycle itself (a candidate *for decision*), not a
  promotion candidate. "Substantial" is satisfied by a full minimum decision
  record with digest-bound evidence and falsifiers, which TeachingCo's cycle
  has.
- *Goodhart/incentives:* if only shared-content candidates counted, an honest
  group whose real state is "already adopted locally, nothing to promote"
  must either fabricate a promotable need or forfeit gate participation. The
  gate would then select for invented content. `other_disposition` exists in
  the lawful disposition set precisely to express this honest outcome;
  double-charging honesty for it defeats that.
- *Systems/deadlock:* rule §1 caps each group at one cycle. If a group's
  single lawful `other_disposition` cycle did not count, that group could
  never re-enter the population without violating its own cap — a reading
  that makes the gate structurally unsatisfiable for an honest participant is
  the wrong reading.
- *Adversarial counter:* could a group then game population with vacuous
  no-op cycles? No — the content-owner can lawfully answer `rejected`, and a
  rejected cycle is a failed origination, not a counting one. The guard
  already exists at the decision layer.
- **Ratification:** the future G4 PASS review should state this counting in
  its PASS record. Contingency if it reads otherwise: population is 2/3 and a
  third qualifying origin is owed — that consequence should be weighed
  *before* adopting the stricter reading, for the incentive reasons above.

## Q2 — Do declared `pilot_groups` confer promotion standing?

**Position: no. Declarations are routing metadata with zero promotion
standing; standing requires independently claimed, digest-bound repetition
by a second group.**

- *First principles:* promotion generalizes a local observation into a
  shared default. The only evidence that generalization is safe is
  independent repetition. A declaration is intent, not observation. The
  frozen rule `participant_evidence_alone_changes_nothing` already says even
  participant *evidence* cannot auto-promote — a fortiori declarations
  cannot.
- *Adversarial red-team:* the original process bug was three "owners"
  declaring support in one minute from one controller. Treating declarations
  as standing would rebuild that attack surface with new syntax. The control
  that actually defeated it — distinct claimed-by, per-group digest-bound
  evidence — is therefore the minimum bar for any promotion input.
- *Maximin decision theory:* promotion is the least reversible lifecycle
  transition (shared default). For the least reversible moves, require the
  strongest evidence class: a second distinct positive owner group's own
  originated cycle (preferred) or an equivalent digest-bound
  adoption-scan/doctor/journey record, independently claimed; then, and only
  then, an EC content-owner promotion decision (≥2 groups,
  non-originator-present, no emergency path — all already frozen).
- **Trigger/falsifier:** the moment a second group files such evidence,
  promotion becomes *eligible for consideration* — never automatic.

## Q3 — G0-A3 `base_commit` drift: re-emit or define semantics?

**Position: define, don't re-emit. `base_commit` is the admission-time main
snapshot, not candidate provenance; provenance is authoritatively bound
elsewhere.**

- *Chesterton's fence:* establish the field's job before changing it. Its job
  is to document the main state at the moment G0-A3 released the candidate
  path. It never claimed to be the candidate's parent — candidate-3 was
  frozen later (task 5016) and G4-B independently validates the candidate
  branch tip (`7a41ea3`, ≠ main).
- *Single-source-of-truth:* copying candidate provenance into G0-A3 would
  create a second truth that can drift — the confusion this question
  records is the symptom of *almost* having two. Keep provenance where it is
  already enforced.
- *Audit integrity:* the 5039 binding re-emit was necessary (a factual
  digest break); a cosmetic `base_commit` refresh is not. Retroactively
  rewriting an admission that already did its gate job trades correctness
  for nothing.
- **Contingency:** any future validator that consumes `base_commit` for
  ancestry must check the candidate's *actual parent* (per the 5016 freeze),
  never current `main`. If a tool is found that consumes it as provenance,
  re-emit under its own task with corrected semantics.

## Q4 — `g1_run.py` pins `CANDIDATE_COMMIT = b313bec`: re-pin now?

**Position: defer to the G1 production task; until then any new `g1_run`
output is non-evidence by construction.**

- *Evidence typing:* a pinned label inside a generator is a hidden invariant
  silently inherited by every artifact it emits. The risk only materializes
  when the runner executes — and the gate sequencing says the next legitimate
  execution is G1 production against the frozen candidate-3.
- *Minimal intervention:* the runner is the frozen instrument that produced
  the four historical baselines. A third churn this wave, ahead of the task
  that actually needs the change, reopens verified evidence for zero gate
  value.
- *Sequencing:* the G1 production task's natural first step is
  parameterization — `--candidate-commit` with default `b313bec` (bit-for-bit
  reproduction preserved, mislabeling impossible when explicit).
- **Falsifier/trigger:** a pre-gate diagnostic need before that task → run
  in scratch with an explicit one-off edit; never commit or cite the output
  as gate evidence while the pin is stale.

## Q5 — 4974 result misbinding: rewrite or additive correction?

**Position (already implemented as evidence 7724, hereby ratified as the
standing convention): corrections are additive; results are immutable
history.**

- *Append-only ledger principle:* corrections are reversing entries, never
  erasures. One mutable result row would make every result row potentially
  mutable — the task ledger's entire evidentiary value rests on never
  exercising that option.
- *In-program precedent:* 4952–4954 were retained as non-qualifying history
  rather than deleted; the rollback law requires `history_preserved=true`;
  session JSONL is append-only by contract. The house style is consistent:
  preserve, point forward.
- **Convention:** a correction = evidence row of a correction type on the
  same task, stating the defect, the corrective chain, and the authoritative
  current state. Authority flows through the newest pointer. If AK later
  ships a native correction command, prefer it; until then this is the rule.

## Debts D1/D2 — dispositions

- **D1 (participant schema-string variance):** accept as frozen history. Norm
  going forward: participants emit `engineering-core.v1.g4/1` from the start;
  EC will not normalize silently again (5036-style normalization is
  decision-time only, and the normalization is recorded in the decided
  record's lineage).
- **D2 (duplicated `LINEAGE_LAWFUL_DISPOSITIONS`):** keep deferred until a
  harness revision is otherwise required. Ready-to-apply drift guard for that
  task: a cross-module test asserting
  `g0a3.LINEAGE_LAWFUL_DISPOSITIONS == g4b.LINEAGE_LAWFUL_DISPOSITIONS ==
  set(governed_evolution.LAWFUL_FINAL_DISPOSITIONS) - {"promoted"}`.

## Explicit non-claims

No G4 PASS. No G5 fan-in input finalized. No promotion granted or made
eligible. No frozen record re-emitted. Q1/Q2 positions in particular await
restatement inside any future G4 PASS record, where their consequences
(population 3/3 vs 2/3) take effect.
