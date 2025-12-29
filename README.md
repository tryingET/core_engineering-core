# tech-stack-core

Shared “lane” docs for day-to-day coding conventions and commands.

## Why this is a git repo + CLI (not Codex slash commands)

We intentionally keep the “core + divergence” mechanism **outside** Codex prompts:

- **Codex skill (`tech-stack-discovery`)** is the right place for *interactive, in-agent* stack detection and “how to work in this repo” guidance.
- **This repo + git tags** is the right place for *distribution and versioning* of the shared lane docs.
- **CLI (`tech-stack-core`)** is the right place for *automation outside Codex* (scripts/CI/quick printing), and can be installed/run via `uv tool …` from a local path or from `git+…@<tag>`.

Slash commands were removed because they duplicated the skill/CLI, increased cognitive overhead (“which entry point do I use?”), and risked drifting out of sync with the canonical workflow.

## Layout

- `lanes/tech-stack-py.md` (symlink to packaged files)
- `lanes/tech-stack-ts.md` (symlink to packaged files)
- `lanes/tech-stack-go.md` (symlink to packaged files)

## Per-repo overrides

Add repo-specific adjustments in one of:

- `.codex/tech-stack.local.md`
- `.claude/docs/tech-stack.local.md`
- `docs/tech-stack.local.md`

Treat the override as higher priority than the lane docs.

## Versioning

- Bump version: `uv version --bump patch` (or `minor`/`major`)
- Tag: `git tag X.Y.Z`

## Build / publish (uv)

- Build: `uv build`
- Publish (requires token/index creds): `uv publish`

## CLI

- List lanes: `uv tool run tech-stack-core list`
- Print a lane: `uv tool run tech-stack-core show py`
- Get path: `uv tool run tech-stack-core path py --prefer-repo`
