---
summary: "Weekly engineering-core adoption posture sweep across softwareco/owned."
read_when:
  - "Running the recurring adoption audit"
type: "procedure"
---

# Activity Prompt: Adoption Audit (weekly posture sweep)

- Goal: produce a truthful weekly picture of engineering-core adoption across `softwareco/owned`, with owner-ready follow-ups and zero mutations.
- Inputs:
  - lane root `/home/tryinget/ai-society/softwareco/owned`
  - committed projections: `<lane-root>/governance/engineering-core-adoption-scan.json` and `<lane-root>/docs/project/engineering-core-adoption-dashboard.md`
  - engineering-core checkout `~/ai-society/core/engineering-core`

## Procedure

1. From the lane root, run the read-only preview:

   ```bash
   ./scripts/engineering-core-adoption-scan.sh --include-packages
   ```

   Add `--format json` when you need machine-readable detail. Never pass `--write`.
2. Diff the preview against the committed projection: record counts, structural/semantic status changes, and any new or vanished records (a new child repo counts as drift).
3. For every record that is not `adopted` + `ok` — `partial`, `doc-only`, `policy-only`, `legacy-only`, `legacy-mixed`, `invalid-policy`, `missing`, or semantic `likely-incomplete`/`needs-review` — read that repo's `<repo>/AGENTS.md`, `<repo>/docs/engineering.local.md`, and `<repo>/policy/engineering-lane.json` before judging. The scanner is a planning surface, not a mutation order.
4. Run `engineering-core doctor --repo <path> --pretty` for records with unknown catalog ids, invalid policy, or declared capability contracts that need static checks.
5. Compose the report (shape below) and file it as a diary entry in this repo.

## Output shape

- headline counts: repos, packages, structural/semantic status deltas versus the last committed scan
- review-candidates table: path | structural | semantic | loop-validation | first evidence
- per-candidate finding: what drifted, the evidence (command + path), the proposed owner action
- proposed operator commands (owner-executed), e.g. the lane-root refresh with `--write`
- an explicit "not done" list of everything left to owners

## Boundaries

- No `--write`, no `--apply`, no edits outside this repo. Findings are proposals to repo owners and the lane owner.
