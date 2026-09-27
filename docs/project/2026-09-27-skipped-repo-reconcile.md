---
summary: "Handoff for the Pi tabs that reconcile each repo the v0.12.0 rollout skipped, move it to engineering-core v0.12.1, and push it to main."
read_when:
  - "You are a Pi session whose prompt names one repo and one AK task from this round."
  - "Auditing or resuming the skipped-repo reconcile round."
type: "handoff"
---

# Skipped-repo reconcile and upgrade

## Why

The v0.12.0 fleet rollout (AK6050–AK6054, [rollout handoff](2026-09-27-v0.12.0-fleet-rollout.md)) skipped 16 repos because another agent was active in them, their trees were dirty, or they had unpushed commits that weren't the rollout's. Each of those repos now gets its own session. The operator's order is: reconcile first (commit what's lying around, push what's stranded), then upgrade, then push. Development is mainline: commit to `main` and push to `main`.

## Your repo, one AK task

Your prompt names exactly one repo and one AK task. Claim it with `session-$PI_SESSION_ID` (`ak task claim <id> --agent session-$PI_SESSION_ID --lease 3600`; renew the lease if you run long), stay inside that repo, and complete or fail it with the same `--agent`.

## 1. Reconcile

1. `git status --short --branch`, `git fetch`, `git log --oneline @{u}..HEAD`, `git log --oneline HEAD..@{u}`.
2. **Live agents.** List processes working in the repo: `for p in $(pgrep -f .); do printf '%s %s\n' "$p" "$(readlink /proc/$p/cwd)"; done | grep "<repo path>"`. Don't commit a file that changed in the last 30 minutes (`find . -newermt '-30 minutes' -type f -not -path './.git/*' -not -path '*/node_modules/*'`). If fresh edits belong to a live session, wait and recheck every 10 minutes for up to an hour, then commit what's settled and report the rest.
3. **Uncommitted work.** Read the diff and split it into coherent commits by topic, with explicit paths (`git commit -- <paths>`) and normal hooks (never `--no-verify`). Name the content in each message (`fix(x): ...`, `docs(y): ...`) and add `Checkpointed uncommitted work (AK<task>).` in the body. Regenerate generated output (for example `ontology/dist`) with the repo's own command rather than committing a stale copy. Never discard, stash, reset, or `git clean` anything. Leave obvious scratch (logs, local caches, editor files) uncommitted and list it in your result. Work that is clearly half-done and breaks the gate stays uncommitted: report it with its paths.
4. **Stranded commits** (ahead of upstream). Check the AK task named in each message (`ak task show <id>`). Push them along if that task is done, or if the commits are older than a day and the gate passes. If a task that's still claimed has been active within the last day, leave its commits and report them.
5. **Behind upstream.** After committing, `git pull --rebase`. If the rebase conflicts, resolve it only when the resolution is obvious; otherwise `git rebase --abort` and report the repo as blocked.
6. **Baseline gate.** Run the repo's gate (`just check`, `just ci`, `./scripts/ci/full.sh`, or what AGENTS.md names) and record the result. Pre-existing failures are baseline.

## 2. Upgrade to v0.12.1

Target pin: `v0.12.1` at `5be0f0a294014f2f7aee1ca5adcb6f3c76553e11`, source `git+https://github.com/tryingET/core_engineering-core.git@5be0f0a294014f2f7aee1ca5adcb6f3c76553e11`. It is the v0.12.0 rollout target plus the fixed `migrate --ref`.

- Edit the pin by hand in `policy/engineering-lane.json` (`engineering_core`): `repository` `https://github.com/tryingET/core_engineering-core`, `ref` `v0.12.1`, `release_pin` `{kind: git-commit, ref: v0.12.1, resolved_commit: <sha>, source: <source>}`, and every `command`/`*_command` using that source, never `git+file`. Keep every other key. If the repo's own validator requires `ref` to be a raw 40-character SHA, keep that shape with the new SHA. Don't use `engineering-core migrate` here: it refuses a hand-written `docs/engineering.local.md`, and with `--force` it replaces that file with the managed template, losing the repo's content.
- Update the release-pin line in `docs/engineering.local.md` to `v0.12.1` (`5be0f0a294014f2f7aee1ca5adcb6f3c76553e11`).
- Adopt the lane changes that apply, exactly as in step 4 of the [rollout handoff](2026-09-27-v0.12.0-fleet-rollout.md#per-repo-procedure): uv `exclude-newer`, TypeScript 7 only, Biome 2.x, cargo `--workspace --locked`, and so on. Where the repo deliberately differs, record the deviation in `docs/engineering.local.md`.
- **Stale rule.** If the repo's `AGENTS.md` says ``Never push to `main`; MRs only.``, delete that line: development is mainline and GitLab is gone. (A separate task fixes the templates and every other repo.)
- Rerun the gate: no worse than baseline. Run `uv run --project ~/ai-society/core/engineering-core engineering-core scan-adoption --scope <repo> --include-scope-root --format json --prefer-repo` and confirm the new ref and no `uv_lock_records_undeclared_setting` flag.
- Commit: `chore(engineering-core): adopt v0.12.1 (AK<task>)`, with a body listing what changed and any deviation.

## 3. Push

Push to `main` when the branch fast-forwards (`git fetch` first; rebase if needed). Ignore any stale "MRs only" wording. Don't force-push. If the remote is missing or rejects the push, leave the commits local and report it.

## Stop and report instead of guessing

- A change would need a product decision (replacing a tool, renaming a public package, deleting someone's work).
- The gate gets worse and the cause isn't clear after a short look.
- A quiet-window request arrives from another session: pause AK and heavy work until it's released.

## AK result

Complete the task with JSON: `repo`, `reconcile` (commits made, stranded commits pushed or left, uncommitted paths left with why), `upgrade` (pin, lane changes, deviations), `gate` (baseline vs after), `push` (range or why not), and `engineering_core_defects` (anything wrong in engineering-core itself, or `[]`). Record per-step evidence with `ak evidence record` where useful. Use `fail` only when you couldn't reconcile or upgrade at all.
