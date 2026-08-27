---
summary: "Hard rules: data + files this agent must not touch."
read_when:
  - "When the agent is about to edit core/governance paths or run mutating commands"
---

# Do Not Touch

## Secrets
- Never commit secrets or tokens.

## Immutable core paths
- `docs/_core/**` is immutable (core snapshot/submodule).
- `~/ai-society/core/engineering-core` is reference-only: never commit, push, or open issues/PRs there — route feedback through the EC owner instead.

## Authority surfaces (owner-only)
- Agent Kernel and `society.v2.db`: never claim or complete tasks, record evidence, or mutate decisions/direction. Task lifecycle belongs to the operator.
- Lane-root projections: never run `./scripts/engineering-core-adoption-scan.sh --write`; `<lane-root>/governance/engineering-core-adoption-scan.json` and the dashboard belong to the lane owner.
- Consumer repos: never run engineering-core `--apply`, `--force`, `--remove-legacy`, `rollback`, or `remove`; never edit their files. Propose diffs and commands for repo owners.

## This repo
- `governance/task-scopes/AK-*.snapshot.json` are frozen AK exports — never hand-author them.
