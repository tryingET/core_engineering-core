---
summary: "pi extension TypeScript lane standardized Justfile addendum."
read_when:
  - "A repo using the pi extension TypeScript lane is missing, establishing, or reconciling the standardized Justfile surface."
  - "Standard targets are absent, drifting, or need lane-specific command mapping."
type: "guide"
---

# TypeScript lane for pi extension packages — standardized Justfile addendum

Read this addendum only when a repo using the pi extension TypeScript lane is missing the standardized Justfile surface, the standard targets are absent/drifting, or you are explicitly establishing/reconciling `Justfile` behavior.

Use this addendum with `disciplines/validation.md` and the repo's applicable standardized Justfile contract.

## Mapping rule

Standardize the outer `just` command names while keeping the implementation thin and aligned with the Node 22 + npm package contract used by pi extension repos.
Prefer existing package scripts and release-check wrappers over duplicating logic in the `Justfile`.

## Recommended target mappings

- `just help`
  - prefer: `just --list`
- `just test`
  - prefer the repo's canonical test command when it exists (`npm test`, `node --test`, or an equivalent package script)
  - if the repo has no independent test contract yet, delegate to the smallest truthful validation surface instead of inventing fake tests
- `just check`
  - prefer: `npm run check`
- `just build`
  - include when the repo has a meaningful build/package artifact contract
  - prefer the repo's existing build or pack command
- `just lint`
  - prefer the repo's existing lint/typecheck surface when it is independently meaningful
  - otherwise let `just check` remain the canonical combined validation surface and keep `lint` as a thin alias only if that improves clarity
- `just fmt`
  - prefer the repo's existing formatter command when present
- `just ci`
  - prefer: `npm run release:check`
  - or the repo's canonical full local release/validation preflight
- `just doctor`
  - prefer an existing repo-local runtime/environment sanity command when present
  - fallback: a lightweight Node/npm sanity check such as `node --version && npm --version`
- `just dev`
  - usually omit unless the extension package has a real watch/dev loop worth exposing

## Optional repo-loop-validation-v1 mappings

Pi extension TypeScript repos that participate in agent/prompt orchestration loops may adopt `repo-loop-validation-v1` as thin `just loop-*` recipes that delegate to package scripts and pi/release-check wrappers.

Recommended pi extension TypeScript mappings:

- `loop-doctor`
  - prefer a non-failing diagnostic that reports Node/npm versions, package install posture, pi extension packaging posture, dirty tree, task-scope binding, and known blockers
  - fallback: capture `just doctor` output and documented scope diagnostics without making `loop-doctor` fail
- `loop-verify-fast`
  - prefer the fastest truthful focused gate, usually `npm run check`, targeted `node --test`, or the repo's existing `just check`
- `loop-impact-plan`
  - prefer a repo-local changed-file classifier that maps extension source, prompts/skills, package metadata, lockfiles, tests, and docs to bounded/expanded/wide checks
- `loop-impact-run`
  - prefer the bounded/expanded checks named by the plan, usually targeted tests plus package check/build for touched extension packages
- `loop-impact-wide`
  - prefer `npm run release:check`, `just ci`, or the repo's full local release/validation preflight when wide impact is accepted
- `loop-landing-check`
  - prefer the repo-declared release/readiness gate, including package metadata, generated bundle, task-scope, and evidence checks where applicable

Shared loop semantics and authority boundaries live in `disciplines/validation.md`; this section only maps lane-specific implementation choices.

## Omission rule

Do not create a fake `dev` target for small extension/prompt packages that do not have a meaningful long-running development mode.

## Minimal-churn rule

Prefer thin aliases to:
- `npm run check`
- `npm run release:check`
- existing package scripts
- explicit smoke commands already documented by the repo

Do not bury release/package policy inside ad-hoc Justfile shell blocks if the package contract already expresses it clearly.
