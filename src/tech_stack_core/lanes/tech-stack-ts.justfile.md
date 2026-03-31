# TypeScript lane — standardized Justfile addendum

Read this addendum only when a repo using the general TypeScript/Bun lane is missing the standardized Justfile surface, the standard targets are absent/drifting, or you are explicitly establishing/reconciling `Justfile` behavior.

Use this addendum with the generic owned-lane Justfile contract.

## Mapping rule

Standardize the outer `just` command names while keeping the implementation thin and Bun-native.
Prefer package scripts or existing repo-local wrappers when they already define the canonical workflow.

## Recommended target mappings

- `just help`
  - prefer: `just --list`
- `just dev`
  - prefer: `bun run dev`
  - or the repo's canonical watch/dev-server command
- `just test`
  - prefer: `bun test`
  - or the repo's package-script wrapper for the default test suite
- `just check`
  - prefer: `bun run check`
- `just build`
  - prefer: `bun run build`
  - fallback: `bun build ...` only if the repo has not wrapped its build contract in scripts
- `just lint`
  - prefer: `bun run lint`
  - fallback: `biome check .`
- `just fmt`
  - prefer: `bun run format`
  - fallback: `biome format --write .`
- `just ci`
  - prefer existing full repo-local validation/CI wrapper when present
  - fallback: package-script orchestration such as check + test + build in the repo's documented order
- `just doctor`
  - prefer an existing repo-local environment/runtime sanity command when present
  - fallback: a lightweight Bun/toolchain check such as `bun --version`

## Omission rule

If the repo has no meaningful long-running dev/watch surface, omit `just dev` rather than inventing a placeholder target.

## Minimal-churn rule

Prefer delegation to existing package scripts and wrappers over embedding large shell flows directly in `Justfile` recipes.
