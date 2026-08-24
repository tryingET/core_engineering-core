---
summary: "G4 review-governed evolution protocol: live-cycle contracts, deterministic lifecycle-conformance transition table, and rollback drill; shared content lands only through the engineering-core content owner."
read_when:
  - "Executing, reviewing, or validating Gate G4 live pilots, content-owner decisions, or lifecycle conformance under decision 128."
  - "Authoring a G4-A candidate record, disposition, promotion, rollback drill, or G4-B inclusion-map check."
type: "implementation-plan"
---

# G4 review-governed evolution proof protocol

Controlling contract: `docs/rfc/2026-08-23-v1-convergence-contract-r5.md` (Gate G4),
accepted as `docs/adr/2026-08-23-v1-convergence-contract.md`.
Harness: `scripts/v1/governed_evolution.py` (internal qualification tooling).
Tests: `tests/test_v1_governed_evolution.py`.

## Authority boundaries

- **Participant owners** authorize only their local proposal, pilot, evidence, rollback,
  and disposition. They cannot transition shared engineering-core content.
- **The engineering-core content owner alone** accepts, rejects, revises, deprecates,
  retires, or promotes shared content under an exact task, an accepted decision where
  required, and repository validation.
- Validation, participant disposition, content-owner transition, package distribution,
  and adoption remain separate fields. No pilot content is created and no participant
  repository is mutated by this protocol task; owner pilots require separate
  target-root tasks after this protocol is accepted.
- Negative and retired history remains interpretable without executable pre-v1
  compatibility.

## Live cycle (G4-A)

```text
proposal record -> opt-in bounded pilot -> evidence and counterevidence
  -> participant-local disposition -> engineering-core content-owner decision
    -> rollback/expiry/final state with preserved lineage
```

Three distinct positive owner groups each originate one substantial candidate under an
exact task. Independent contexts means distinct positive owner groups; two baselines
within one company count as one. Before any output, the matrix freezes candidates,
origin/pilot groups, owner and content-owner tasks, reviewers and conflicts, digests,
success/harm/falsification criteria, minimum-supported-v1 consumer, expiry/review event,
rollback, and transfer.

Every candidate carries the minimum decision record from `docs/content-lifecycle.md`:
problem, audience and scope, invariant or decision rule, load triggers, evidence
references, strongest alternative, counterevidence and exceptions, falsification
conditions, adoption and compatibility (v1 compatibility/transition effect, rollback),
review trigger, retirement signal, and semantic references where applicable.

**No distribution of live outcomes is required.** Every candidate is judged only against
its frozen criteria; a lawful promotion, revision, rejection, deprecation, retirement, or
other content-owner disposition completes a cycle. Expiry without the required decision
does not. The gate cannot demand a sacrificial rejection, force a promotion, or
reinterpret evidence to fill a quota.

**Promotion** requires at least two distinct positive owner groups including one other
than the originator; the emergency exception cannot satisfy ordinary promotion proof.
Participant evidence never changes shared state by itself; there is no automatic
promotion.

## Deterministic lifecycle-conformance suite

Covers proposal, pilot selection, promotion, revision/split, rejection, deprecation,
retirement, expiry, rollback, invalid transition, stale evidence, and unauthorized
promotion — via synthetic fixtures or prospectively selected immutable owner-attested
historical cases. It proves transition mechanics and lineage only; it does not count as
live owner evidence or dictate any live outcome.

## Rollback drill (mandatory)

From an explicit pilot selection, restore the exact prior stable selection without
erasing proposal, evidence, decision, or failure history. The drill tests reversibility,
not substantive judgment.

## G4-B (post-candidate, non-mutating)

Checks the exact candidate's inclusion map from every accepted G4-A digest to its
candidate path/digest and from every rejected, reverted, revised, deprecated, retired,
or expired outcome to preserved immutable lineage; replays the deterministic transition
suite; reproduces minimum-v1 compatibility, rollback, and participant-validation
evidence. A defect requiring change creates a new candidate under the impact matrix.

## Fail-closed rules

The harness rejects, among others: a cycle missing its minimum decision record; pilots
that are not opt-in, unbounded, or lack an expiry/review event; any transition performed
by a participant or model rather than the content owner; promotion without two distinct
groups or without a non-originator; promotion via emergency exception; expiry counted as
a completed cycle; erased or truncated negative lineage; rollback that loses history;
stale-evidence transitions without re-review; and any field conflating disposition,
transition, distribution, or adoption status.
