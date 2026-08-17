---
summary: "TypeScript lane standardized Justfile addendum."
read_when:
  - "A repo using the TypeScript lane is missing, establishing, or reconciling the standardized Justfile surface."
  - "Standard targets are absent, drifting, or need lane-specific command mapping."
type: "guide"
---

# TypeScript lane — standardized Justfile addendum

Read this addendum only when a repo using the general TypeScript/Bun lane is missing the standardized Justfile surface, the standard targets are absent/drifting, or you are explicitly establishing/reconciling `Justfile` behavior.

Use this addendum with `disciplines/validation.md` and the repo's applicable standardized Justfile contract.

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

## Optional repo-loop-validation-v1 mappings

TypeScript/Bun repos that participate in agent/prompt orchestration loops may adopt `repo-loop-validation-v1` as thin `just loop-*` recipes that delegate to package scripts or repo-local wrappers.

Recommended TypeScript/Bun mappings:

- `loop-doctor`
  - prefer a non-failing diagnostic that reports Bun/Node/package-manager versions, install posture, dirty tree, task-scope binding, and known blockers
  - fallback: capture `just doctor` output and documented scope diagnostics without making `loop-doctor` fail
- `loop-verify-fast`
  - prefer the fastest truthful focused gate, such as affected package tests, `bun run check`, `bun test` for the touched package, or existing `just check`
- `loop-impact-plan`
  - prefer a repo-local changed-file classifier that maps source, tests, build config, lockfiles, generated artifacts, and docs to bounded/expanded/wide checks
- `loop-impact-run`
  - prefer the bounded/expanded checks named by the plan, usually package-local check/test/build for touched workspaces
- `loop-impact-wide`
  - prefer `just ci` or the repo's full local validation/release-check wrapper when wide impact is accepted
- `loop-landing-check`
  - prefer the repo-declared pre-commit/pre-push readiness gate, including generated-file, lockfile/package-manager metadata, task-scope, and evidence checks where applicable

Shared loop semantics and authority boundaries live in `disciplines/validation.md`; this section only maps lane-specific implementation choices.

## Omission rule

If the repo has no meaningful long-running dev/watch surface, omit `just dev` rather than inventing a placeholder target. If `build`, `lint`, `fmt`, or `test` is not independently meaningful yet, delegate to the smallest truthful existing validation surface or omit the target with an implementation note rather than creating fake green commands.

## Minimal-churn rule

Prefer delegation to existing package scripts and wrappers over embedding large shell flows directly in `Justfile` recipes.
