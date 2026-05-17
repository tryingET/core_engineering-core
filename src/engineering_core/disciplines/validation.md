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
