---
summary: "Python lane standardized Justfile addendum."
read_when:
  - "A repo using the Python lane is missing, establishing, or reconciling the standardized Justfile surface."
  - "Standard targets are absent, drifting, or need lane-specific command mapping."
type: "guide"
---

# Python lane — standardized Justfile addendum

Read this addendum only when a repo using the Python lane is missing the standardized Justfile surface, the standard targets are absent/drifting, or you are explicitly establishing/reconciling `Justfile` behavior.

Use this addendum with `disciplines/validation.md` and the repo's applicable standardized Justfile contract.

## Mapping rule

Standardize the outer `just` command names while keeping the implementation thin and Python/uv-native.
Prefer existing repo-local scripts and `pyproject.toml` script surfaces when they already define the canonical workflow.

## Recommended target mappings

- `just help`
  - prefer: `just --list`
- `just dev`
  - prefer the repo's canonical long-running development command, such as `uv run dev`
  - omit if the repo has no meaningful dev/watch surface
- `just test`
  - prefer: `uv run python -m pytest tests/`
  - or the repo's existing truthful test wrapper/script
- `just check`
  - prefer the repo's fast validation gate when present
  - common fallback: a thin wrapper over lint + typecheck or the repo's default quality check command
- `just build`
  - include when the repo has a meaningful package/build artifact contract
  - prefer the repo's existing build/package command
- `just lint`
  - prefer: `uv run ruff check .`
  - or the repo's existing lint wrapper
- `just fmt`
  - prefer: `uv run ruff format .`
  - or the repo's existing formatter wrapper
- `just ci`
  - prefer the repo's canonical full local validation/CI wrapper when present
  - fallback: run the repo's documented full validation sequence through thin delegation
- `just doctor`
  - prefer an existing repo-local environment/runtime sanity command when present
  - fallback: a small uv/Python sanity check such as `uv --version && python --version`

## Omission rule

Do not invent fake package/build or dev-server targets.
If `dev` or `build` is not meaningful for the repo, omit it and state that omission in the implementation summary.

## Minimal-churn rule

Prefer delegation to:
- existing `uv run ...` script surfaces
- repo-local validation wrappers
- existing package/build helpers

Do not move large orchestration flows into the `Justfile` if `pyproject.toml` scripts or repo-local scripts already express them cleanly.
