---
summary: "Route adoption learnings and content feedback back to the engineering-core owner."
read_when:
  - "Crystallized learnings indicate engineering-core content gaps or friction"
type: "procedure"
---

# Activity Prompt: EC Feedback

- Goal: close the loop — adoption friction observed in the fleet reaches the engineering-core owner as reviewable, evidenced feedback.
- Inputs: this repo's `docs/learnings/`; audit and deviation findings that implicate EC content; `~/ai-society/core/engineering-core/docs/content-lifecycle.md` and `~/ai-society/core/engineering-core/docs/discipline-lifecycle.md`.

## Procedure

1. Triage the learning:
   - (a) EC content gap → route here;
   - (b) repo-local exception → route to `deviation-review.md` instead;
   - (c) scanner/tooling behavior → route here, marked tooling.
2. Draft the feedback item: what content, where it would live (lane / discipline / template), the evidence (repo paths, scan records, diary dates), and a concrete proposed change.
3. Optionally prepare an unapplied proposal draft via `engineering-core doctrine-propose` for the EC owner to review. Never apply it.
4. Hand off to the engineering-core owner (workspace checkout: `~/ai-society/core/engineering-core`). This agent never commits, pushes, or opens issues there.
5. Record the routing (date, item, owner, channel) in this repo's diary and link the source learning entry.

## Output shape

- a feedback packet: context → evidence → proposed change → requested owner
- a diary routing note

## Boundaries

- Ownership of engineering-core content stays with its owner (source-owner boundary). Feedback is routed, never filed directly.
