---
summary: "Evidence-gated TypeScript pilot for evaluating Ultracite without changing the lane default prematurely."
read_when:
  - "A TypeScript repo is comparing its current quality toolchain with Ultracite."
  - "A greenfield or brownfield cohort needs comparable lint/format adoption evidence."
type: "guide"
status: "pilot"
---

# TypeScript lane — Ultracite pilot addendum

This addendum is experimental. It does **not** replace the TypeScript lane's current quality-tool realization and does not establish Ultracite, Biome, Oxlint, ESLint, or any backend as a new organization-wide default.

Use it with `ts`, `validation`, `testing`, `dependency-governance`, and `performance`. Record the pilot with the `typescript-quality-pilot` template.

## Objective

Measure whether a maintained preset and lifecycle (`init`, `check`, `fix`, and `doctor`) reduces configuration drift and agent/human inconsistency without creating unacceptable diagnostics, dependencies, migration cost, or lock-in.

## Cohorts

Run at least two representative cohorts before proposing a default change:

- **greenfield:** a small new TypeScript package or service with no existing quality configuration;
- **brownfield:** an actively maintained repository with checked-in formatting/linting, real exceptions, generated paths, and CI history.

Do not treat a successful toy repository as sufficient evidence for brownfield adoption.

## Compared realizations

Capture the current repository baseline first. Then compare only variants justified by the repository:

1. existing direct tool configuration, commonly direct Biome in the current lane;
2. Ultracite using the closest equivalent backend and framework presets;
3. an Ultracite/Oxlint realization only when a speed or plugin hypothesis warrants a separate controlled trial;
4. ESLint-based comparison only when the repo already depends on that ecosystem or requires plugins unavailable elsewhere.

Query and record exact versions at pilot time. Preserve the repository package manager, lockfile posture, editor settings, agent instructions, and unrelated configuration.

## Measurements

Record for each variant:

- exact tool, preset, plugin, runtime, and package-manager versions;
- installation/configuration diff and dependency count;
- cold and warm check/fix runtime over the same file set;
- diagnostics by rule and severity before and after auto-fix;
- false positives, ambiguous findings, required suppressions, and unfixable findings;
- changes to generated/vendor/build-output ignores;
- editor and agent integration behavior;
- `doctor` or equivalent configuration-diagnosis outcome;
- CI behavior, deterministic non-interactive setup, and rollback steps;
- reviewer time and migration effort.

Do not compare runs with different file scopes, caches, generated outputs, or lockfile states without labeling the difference.

## Agent-assisted fixes

Evaluate autonomous repair separately from the core linter/preset comparison. A tool should not be selected merely because an agent can rewrite failures. Every agent-applied change must be rechecked, reviewed, and attributable to the same deterministic rule set.

## Decision rule

Promote a realization only when the evidence shows a repeatable benefit across both cohorts and the owning scope accepts the tradeoffs. Otherwise:

- keep the current TypeScript default;
- retain the realization as an optional repo-local choice;
- narrow the pilot hypothesis; or
- stop and document why the migration was not worthwhile.

Record the decision, owner, evidence paths, and review date. Promotion to the stable catalog requires a separate reviewed change that removes the pilot status.
