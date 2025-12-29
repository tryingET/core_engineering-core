# tech-stack-core

Shared “lane” docs for day-to-day coding conventions and commands.

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
- Tag: `git tag vX.Y.Z`

## Build / publish (uv)

- Build: `uv build`
- Publish (requires token/index creds): `uv publish`

## CLI

- List lanes: `uv tool run tech-stack-core list`
- Print a lane: `uv tool run tech-stack-core show py`
- Get path: `uv tool run tech-stack-core path py --prefer-repo`
