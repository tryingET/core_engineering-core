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
Prefer existing repo-local scripts when they already define the canonical workflow. uv has no task runner, so recipes call tools directly (`uv run …`).

## Recommended target mappings

- `just help`
  - prefer: `just --list`
- `just dev`
  - prefer the repo's canonical long-running development command, such as `uv run granian --interface asgi --reload <package>.asgi:app`
  - omit if the repo has no meaningful dev/watch surface
- `just test`
  - prefer: `uv run python -m pytest tests/`
  - or the repo's existing truthful test wrapper/script
- `just check`
  - prefer the repo's fast validation gate when present
  - common fallback: `uv run --locked ruff check . && uv run --locked ruff format --check . && uv run ty check`
- `just typecheck`
  - prefer: `uv run ty check`
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
  - fallback: run the lane's **Quality gates** in order (toolchain, lint, `ruff format --check`, typecheck, test)
- `just doctor`
  - prefer an existing repo-local environment/runtime sanity command when present
  - fallback: `uv --version && uv run python --version` (a bare `python --version` reports the system interpreter, not the project's pinned one)

## Optional repo-loop-validation-v1 mappings

Python repos that participate in agent/prompt orchestration loops may adopt `repo-loop-validation-v1` as thin `just loop-*` recipes that delegate to repo-owned uv/Python validation surfaces.

Recommended Python mappings:

- `loop-doctor`
  - prefer a non-failing diagnostic that reports `uv`/Python versions, dependency sync posture, dirty tree, task-scope binding, and known blockers
  - fallback: capture `just doctor` output and documented scope diagnostics without making `loop-doctor` fail
- `loop-verify-fast`
  - prefer the repo's fastest truthful focused gate, such as a changed-slice pytest wrapper, `uv run ruff check`, targeted typecheck, or existing `just check`
- `loop-impact-plan`
  - prefer a repo-local changed-file classifier that maps Python modules, tests, docs, packaging, and migrations to bounded/expanded/wide checks
- `loop-impact-run`
  - prefer the bounded/expanded checks named by the plan, usually targeted pytest plus lint/typecheck for the touched package
- `loop-impact-wide`
  - prefer `just ci`, `just verify-full`, or the repo's full local validation wrapper when wide impact is accepted
- `loop-landing-check`
  - prefer the repo-declared pre-commit/pre-push readiness gate, including task-scope/evidence checks where the repo uses AK or another task authority

Shared loop semantics and authority boundaries live in `disciplines/validation.md`; this section only maps lane-specific implementation choices.

## Omission rule

Do not invent fake package/build or dev-server targets.
If `dev` or `build` is not meaningful for the repo, omit it and state that omission in the implementation summary.

## Minimal-churn rule

Prefer delegation to:
- existing `uv run ...` script surfaces
- repo-local validation wrappers
- existing package/build helpers

Do not move large orchestration flows into the `Justfile` if `pyproject.toml` scripts or repo-local scripts already express them cleanly.
