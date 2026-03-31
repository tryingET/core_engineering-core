# Elixir lane — standardized Justfile addendum

Read this addendum only when a repo using the Elixir lane is missing the standardized Justfile surface, the standard targets are absent/drifting, or you are explicitly establishing/reconciling `Justfile` behavior.

Use this addendum with the generic owned-lane Justfile contract.

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

## Omission rule

Do not invent fake `dev` or `build` targets if the repo has no meaningful long-running application surface or release contract.

## Minimal-churn rule

Prefer delegation to:
- existing `mix` aliases
- repo-local scripts
- documented release/validation entrypoints

Do not duplicate existing Mix alias logic inside large Justfile shell recipes.
