---
summary: "Keep engineering_core.deviations ledgers across owned repos honest."
read_when:
  - "Periodic deviation-ledger review, or after scan semantic flags appear"
type: "procedure"
---

# Activity Prompt: Deviation Review

- Goal: every `engineering_core.deviations` entry under `softwareco/owned` is complete, evidenced, and unexpired.
- Inputs: `<repo>/policy/engineering-lane.json` files across owned repos (plus package/member surfaces the scan reported); the latest scan preview; today's date.

## Procedure

1. Collect the ledgers:

   ```bash
   for f in /home/tryinget/ai-society/softwareco/owned/*/policy/engineering-lane.json; do
     jq -c --arg repo "$f" '.engineering_core.deviations // [] | map(. + {repo: $repo})' "$f"
   done
   ```

2. Validate each entry for the useful-minimum shape: `id`, `reason`, `owner`, `evidence` (paths or links), `review_after`.
3. Flag:
   - missing or vague fields, especially evidence without resolvable paths
   - `review_after` in the past (stale) or absent
   - evidence paths that no longer resolve in the repo
   - deviations whose `reason` contradicts the repo's current shape — cross-check scan semantic flags (`likely-incomplete`, `needs-review`)
4. Compose the review and file it as a diary entry. Repo owners edit their own policy files; this agent never edits consumer repos.

## Output shape

- findings table: repo | deviation id | field | problem | suggested owner action
- summary: total entries, complete, stale, under-evidenced
- diary entry filing the review

## Boundaries

- Read-only outside this repo; recommendations only. An unreviewed deviation is a review signal, not a violation.
