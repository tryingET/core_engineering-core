---
summary: "Propose (never apply) an engineering-core init or migrate transition for one owned repo."
read_when:
  - "A repo needs first adoption or legacy tech-stack migration"
type: "procedure"
---

# Activity Prompt: Migration Proposal

- Goal: hand a repo owner an exact, reviewable, reversible adoption plan that they execute themselves.
- Inputs: target repo path; its `<repo>/AGENTS.md`; existing `<repo>/docs/engineering.local.md` and `<repo>/policy/engineering-lane.json`; any legacy `<repo>/docs/tech-stack.local.md` or `<repo>/policy/stack-lane.json`.

## Procedure

1. Read the target repo's local guidance first. Preserve rich repo-local content; never propose replacing hand-written guidance — `--force` exists for the owner to decide after reviewing the diff.
2. Choose the smallest truthful upstream set: explicit `--lane`/`--discipline` values derived from repo evidence; a catalog profile only when it genuinely matches the repo's shape.
3. Dry-run without apply flags:

   ```bash
   engineering-core init --repo <repo> --lane <lane> --discipline <discipline> --format json
   engineering-core migrate --repo <repo>   # only when legacy surfaces exist
   ```

4. Review the emitted diff field by field: existing machine-readable fields preserved, `engineering_core.deviations` structure intact, release pin honest (workspace-local during development; immutable commit coordinate for released adoption).
5. Write the proposal into this repo (diary entry or learnings note) containing:
   - the diff or its summary
   - the exact owner-executed commands, including `--apply` (and `--remove-legacy --apply` only when the owner has confirmed legacy retirement)
   - the rollback story: every applied init/migrate writes `<repo>/.engineering-core/adoption-journal.json`; `engineering-core rollback --repo .` restores exact pre-adoption bytes and removes the journal; `remove` deletes the adoption surfaces
   - risks and follow-ups (repo validation contract, lane dashboard refresh)

## Output shape

- one proposal document: context → diff → owner-executed apply commands → rollback → risks
- a routing note naming the owner/repo that must execute

## Boundaries

- Never execute `--apply`, `--force`, `--remove-legacy`, `rollback`, or `remove` in consumer repos. Never push or open PRs.
