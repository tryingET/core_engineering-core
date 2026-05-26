---
summary: "Elixir lane standardized Justfile addendum."
read_when:
  - "A repo using the Elixir lane is missing, establishing, or reconciling the standardized Justfile surface."
  - "Standard targets are absent, drifting, or need lane-specific command mapping."
type: "guide"
---

# Elixir lane — standardized Justfile addendum

Read this addendum only when a repo using the Elixir lane is missing the standardized Justfile surface, the standard targets are absent/drifting, or you are explicitly establishing/reconciling `Justfile` behavior.

Use this addendum with `disciplines/validation.md` and the repo's applicable standardized Justfile contract.

## Mapping rule

Standardize the outer `just` command names while keeping the implementation thin and Mix-native.
Prefer existing repo-local aliases and scripts when they already express the canonical workflow.

## Recommended target mappings

- `just help`
  - prefer: `just --list`
- `just dev`
  - include when the repo has a meaningful long-running server/app loop
  - common examples: `mix phx.server`, `iex -S mix phx.server`, or another repo-local dev entrypoint
- `just test`
  - prefer: `mix test`
- `just check`
  - prefer the repo's existing fast validation command when present
  - common fallback: `mix test`
- `just build`
  - prefer the repo's meaningful build/release contract when present
  - common example: `MIX_ENV=prod mix release`
- `just lint`
  - prefer the repo's existing lint wrapper when present
  - common fallback: `mix credo --strict`
- `just fmt`
  - prefer: `mix format`
- `just ci`
  - prefer the repo's canonical full local validation/CI alias when present
  - common examples: `mix ci` or a thin wrapper over the repo's documented full sequence
- `just doctor`
  - prefer an existing repo-local environment/runtime sanity command when present
  - fallback: a lightweight Elixir toolchain check such as `elixir --version && mix --version`

## Optional repo-loop-validation-v1 mappings

Elixir repos that participate in agent/prompt orchestration loops may adopt `repo-loop-validation-v1` as thin `just loop-*` recipes that delegate to Mix aliases or repo-local wrappers.

Recommended Elixir mappings:

- `loop-doctor`
  - prefer a non-failing diagnostic that reports Erlang/Elixir/Mix versions, dependency/database posture, dirty tree, task-scope binding, and known blockers
  - fallback: capture `just doctor` output and documented scope diagnostics without making `loop-doctor` fail
- `loop-verify-fast`
  - prefer the fastest truthful focused gate, such as targeted `mix test <path>`, `mix compile --warnings-as-errors`, `mix credo` for touched apps, or existing `just check`
- `loop-impact-plan`
  - prefer a repo-local changed-file classifier that maps apps, tests, config, migrations, assets, generated files, and docs to bounded/expanded/wide checks
- `loop-impact-run`
  - prefer the bounded/expanded checks named by the plan, usually app-local tests/compile/credo plus migration checks when touched
- `loop-impact-wide`
  - prefer `just ci`, `mix ci`, or the repo's full local validation wrapper when wide impact is accepted
- `loop-landing-check`
  - prefer the repo-declared pre-commit/pre-push readiness gate, including migration, generated-code, task-scope, and evidence checks where applicable

Shared loop semantics and authority boundaries live in `disciplines/validation.md`; this section only maps lane-specific implementation choices.

## Omission rule

Do not invent fake `dev` or `build` targets if the repo has no meaningful long-running application surface or release contract.

## Minimal-churn rule

Prefer delegation to:
- existing `mix` aliases
- repo-local scripts
- documented release/validation entrypoints

Do not duplicate existing Mix alias logic inside large Justfile shell recipes.
