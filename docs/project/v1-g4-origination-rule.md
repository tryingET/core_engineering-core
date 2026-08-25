---
summary: "Process rule that closes G4 independence theater: owner-claimed origination, split content-owner decision, digest-bound records."
read_when:
  - "Creating, claiming, or closing any G4-A live cycle task."
  - "Deciding whether existing G4-A cycles may count toward Gate G4 PASS."
type: "reference"
---

# G4 origination rule

Independent review (`docs/project/v1-g4-independent-review-synthesis.md`)
rejected the 4952–4954 cycles: one controller wrote three owner packs in one
minute. That is the process bug.

## Rule

1. Each positive owner group originates **at most one** G4-A cycle. TeachingCo
   counts as one group (mathe or wib, not both).
2. The originator task must be **claimed in that owner repo** by a `claimed_by`
   that is recorded and is **not** the engineering-core protocol-authoring
   agent for tasks 4874 / 4951 / 4974 / 5004.
3. The three origin `claimed_by` values must be **pairwise distinct**.
4. Participant disposition is written **before** the engineering-core
   content-owner task exists. The content-owner decision is a **later**
   engineering-core task. It must not be pre-filled into the participant JSON.
5. Cycle JSON must digest-bind the sibling candidate markdown and any lineage
   artifact (content SHA-256, not `"see sibling"` / name-only refs).
6. G4-B must not hardcode `disposition == revised` as the only legal live
   outcome.

## Status of 4952–4954

**Non-qualifying.** They remain historical evidence of a failed process. They
must not be counted toward G4 PASS. They were superseded 2026-08-24 by the
re-originated v2 cycles: tasks 5018/5019/5020 originated in distinct
owner-repo sessions and were judged by EC content-owner task 5036
(`v1-g4a-content-owner-decisions.md`). G4-B verification lineage is bound to
the decided v2 cycles (task 5043).

## What this does not do

It does not create three new cycles. It does not grant G4 PASS. It makes a
repeat of lockstep origination fail the written rule and the new task
guardrails.
