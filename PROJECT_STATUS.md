# PROJECT_STATUS

## What this repo is

Shared “lane” docs (py/ts/go) + a small CLI for printing them.

## Current state (2026-01-12)

- Lane docs present: `src/tech_stack_core/lanes/*`
- Python lane: uses `Ruff` + `ty` (replaced `mypy`)
- CLI packaging via `uv` works; installable as `uv tool ...` from repo/tag

## Working agreement

- Canonical content lives in `src/tech_stack_core/lanes/`
- `lanes/` is a symlink for convenience (don’t edit a second copy)
