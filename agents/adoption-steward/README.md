# agent-adoption-steward

The standing **cross-company steward** of engineering-core adoption: an
advisory agent that keeps EC adoption across every consumer (core, holdingco,
teachingco, softwareco, healthco) honest, current, and inspectable. It does
standing-ly what humans and controllers did ad hoc before it existed —
posture sweeps, doctor runs, migration proposals, deviation-ledger reviews,
and routing content feedback into engineering-core.

Lives in engineering-core itself (`agents/adoption-steward/`) because the
steward is EC's own field agent, versioned with the product whose adoption
it stewards (AK 5100 authored it from `softwareco/copier/tpl-agent-repo`;
AK 5102 relocated it core-side and widened its scope — `softwareco/owned`
gitignores `agents/`, so core is also its only committed home). Manifest per
the agent convention v1 (`pi-extensions/docs/project/2026-08-27-agent-manifest-convention.md`).

## What it is

- A persona (`docs/person/system-prompt.md`), a manifest (`agent.json`),
  four recurring activity prompts (`prompts/activities/`), and a learnings
  flow (`diary/` → `docs/learnings/` → EC feedback).
- Advisory by construction: its tools are `read` and `bash` only. It
  proposes; owners dispose.

## How it dispatches

- The manifest (`agent.json`, schema `ai-society.agent/1`) is resolved by
  pi-agent-registry into a spawn for `dispatch_subagent` / fork / scout:
  system prompt from `docs/person/system-prompt.md`; skills
  `softwareco-owned-repo-router` + `ai-society-runtime-recipes` with a
  **null** skill profile — this role stewards adoption rather than executing
  an EC language lane, so an EC code-skill profile would misdescribe it;
  tools `[read, bash]`; thinking `medium`; territory `softwareco/owned/*`.
- Recurring work enters through the activity prompts:
  - `adoption-audit.md` — weekly posture sweep (read-only scan preview,
    dashboard drift, doctor on candidates)
  - `migration-proposal.md` — owner-executable init/migrate plans with a
    rollback story
  - `deviation-review.md` — `engineering_core.deviations` ledger honesty
  - `ec-feedback.md` — route learnings back to the engineering-core owner
- Findings and proposals are filed in this repo (`diary/`, `docs/learnings/`);
  execution decisions stay with AK, repo owners, and the operator.

## What it never does

- Never mutates Agent Kernel state or `society.v2.db` — task
  claim/evidence/complete are operator actions.
- Never applies adoption changes: no `--apply`, `--force`,
  `--remove-legacy`, `rollback`, or `remove` in consumer repos; no
  lane-wrapper `--write`.
- Never edits files outside this repo; never pushes; never opens PRs/MRs.
- Never presents dry-runs as applied, projections as authority, or
  heuristic scan flags as runtime facts.
- Never commits secrets.

## Surfaces

- `agent.json` — executable identity (manifest convention v1)
- `docs/person/` — persona; `system-prompt.md` is the single identity source
- `prompts/activities/` — recurring work templates
- `policy/` — hard do-not-touch rules
- `governance/` — minimal template-family governance; AK projections
- `docs/decisions/`, `docs/learnings/`, `diary/` — decisions, crystallized
  learnings, raw sessions

## Validation

```bash
./scripts/ci/smoke.sh
./scripts/ci/full.sh
```
