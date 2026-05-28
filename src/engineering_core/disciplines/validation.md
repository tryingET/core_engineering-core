---
summary: "Cross-language validation tier and evidence discipline for command surfaces and handoff gates."
read_when:
  - "Choosing validation commands, tiers, evidence, or handoff gates for a repo or task."
  - "Reconciling Justfile/package-script/CI surfaces with expected validation tiers."
type: "guide"
---

# Discipline — Validation

## Purpose

Define portable validation tiers and evidence expectations. Lanes choose tools; this discipline defines what validation means.

## Tier model

| Tier | Scope | Target | Examples |
|---|---|---|---|
| editor/save | file-local | instant | format, local type hints |
| pre-commit | staged slice | p95 under 10s | formatting, lint subset, whitespace, generated checks |
| task-scope | changed behavior | minutes | focused tests, focused typecheck, migration check |
| pre-push | full repo | acceptable local gate | typecheck + default tests + docs checks |
| CI | authoritative matrix | complete enough for merge/release | platform matrix, integration, packaging |
| release | shipped artifact | strongest | provenance, signatures, migrations, package checks |

## Standard command surface

Repos should expose meaningful equivalents:

```text
just help      list supported commands
just check     fast local validation
just test      default test suite
just build     build artifacts
just lint      non-formatting lint
just fmt       write formatting when configured
just ci        full local CI-equivalent gate
just doctor    environment sanity
```

Do not invent fake targets. If a target is intentionally unavailable, say why.

## Normalization before validation

Commit workflows should separate mutation-producing normalization from non-mutating validation:

1. run the repo-declared formatter/fixer or hook stack on the intended file set;
2. inspect the resulting diff;
3. explicitly stage only intended normalized paths;
4. run the repo-declared check/validation mode after normalization.

Hook managers are lane/repo implementation details. Python repos should prefer `prek` when they need a Git hook runner; TypeScript may use Biome/package scripts, Go may use `gofmt`/`goimports`, Rust may use `cargo fmt`, C++ may use `clang-format`, and Elixir may use `mix format`. The invariant is portable: write/fix mode may mutate local files, while validation/CI gates should be non-mutating.

## Loop validation surface

Repos that participate in agent or prompt loops may expose a repo-owned `repo-loop-validation-v1` surface so orchestration can ask for validation by phase without hardcoding repo-specific commands:

```text
loop-doctor         non-failing diagnostics for environment, dirty tree, task scope, and blockers
loop-verify-fast    focused inner-loop validation for the current slice
loop-impact-plan    classify changed-file risk and name checks to run
loop-impact-run     run bounded/expanded impact checks selected by the plan
loop-impact-wide    explicitly accepted wide validation
loop-landing-check  repo-declared landing/readiness gate
```

These commands produce evidence, not authority. Slash commands, visible loops, and agent loops may request them, but repo policy, AK task/decision/evidence surfaces where applicable, CI/release systems, and human/governance approvals retain authority. Use `templates/repo-loop-validation.template.md` to map generic loop phases to local commands or documented fallbacks.

Loop command handoffs should make the invoked phase, validation scope, result, warnings, artifacts, fallback/escalation, and remaining authority boundary recoverable. In particular, `loop-doctor` is diagnostic rather than a validation pass; `loop-impact-plan` should classify bounded/expanded/wide impact and name the next command; `loop-landing-check` should state the repo-declared gate it maps to and any AK, CI, release, or governance handoff that remains.

## Evidence contract

A validation handoff names:

- command
- scope
- result
- timestamp or session context
- artifact path when relevant
- known warnings and why they are accepted

## Decision rules

- Static checks catch shape; tests catch behavior; runtime evidence catches reality. None replaces the others.
- Generated projections must have check mode, not only write mode.
- A fast gate that times out or flakes is not fast validation; narrow it or move it tiers.
- Release gates must validate the artifact that will ship, not merely source files.

## Failure modes

- CI-only truth with no local reproduction path
- green tests while docs/projections drift
- full validation hidden behind slow commands nobody runs
- formatting checks that mutate in CI
- warnings accepted without naming them
