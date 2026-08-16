---
summary: "Common Lisp lane standardized Justfile addendum."
read_when:
  - "A repo using the Common Lisp lane is missing, establishing, or reconciling the standardized Justfile surface."
  - "Standard targets are absent, drifting, or need lane-specific command mapping."
type: "guide"
---

# Common Lisp lane — standardized Justfile addendum

Read this addendum only when a repo using the Common Lisp lane is missing the standardized Justfile surface, the standard targets are absent/drifting, or you are explicitly establishing/reconciling `Justfile` behavior.

Use this addendum with `disciplines/validation.md` and the repo's applicable standardized Justfile contract.

## Mapping rule

Standardize the outer `just` command names while keeping the implementation thin and ASDF-native. Prefer checked-in Common Lisp or shell wrappers once bootstrap, dependency setup, warning policy, or implementation matrices make direct `--eval` forms difficult to review.

## Recommended target mappings

- `just help`
  - prefer: `just --list`
- `just test`
  - prefer the repo wrapper for `asdf:test-system`
  - when Qlot owns dependencies, execute the wrapper or implementation through `qlot exec`
- `just check`
  - prefer a repo-owned, non-interactive ASDF load/compile under the default implementation
  - require the wrapper to load the repo's `.asd` file and document whether inherited ASDF configuration is suppressed
  - include the repo's warning policy rather than pretending all implementations fail on the same warning classes
  - widen to dependent-system recompilation when macros, compiler macros, packages, readtables, types, declarations, or class protocols change
- `just build`
  - include only when the repo has a meaningful artifact operation
  - prefer the repo's ASDF `program-op`, image builder, or release script
- `just lint`
  - include only when the repo has selected and pinned a linter/static analyzer
  - otherwise omit it and rely on the documented compile/warning gate
- `just fmt`
  - include only when the repo has selected and pinned a formatter
  - keep check and write modes distinct where the tool supports them
- `just ci`
  - prefer the repo's canonical full local validation/CI wrapper
  - include every supported implementation only when portability is an accepted package contract
- `just doctor`
  - prefer an existing repo-local environment sanity command
  - fallback: `sbcl --version`, plus `qlot --version` when Qlot is required
- `just dev`
  - include only for a meaningful interactive, server, or watch workflow
  - prefer a repo bootstrap file or wrapper that loads the declared ASDF system reproducibly

## Optional repo-loop-validation-v1 mappings

Common Lisp repos that participate in agent/prompt orchestration loops may adopt `repo-loop-validation-v1` as thin `just loop-*` recipes that delegate to ASDF operations or repo-local wrappers.

Recommended Common Lisp mappings:

- `loop-doctor`
  - prefer a non-failing diagnostic that reports implementation, ASDF, dependency-environment, dirty-tree, task-scope, and known-blocker posture
- `loop-verify-fast`
  - prefer the fastest truthful focused gate, such as loading the touched system or running a targeted test through the repo's declared dependency/isolation wrapper in a fresh process
- `loop-impact-plan`
  - classify `.asd`, package, macro/readtable, source, test, dependency lock, image-build, and documentation changes into bounded/expanded/wide checks
- `loop-impact-run`
  - run the system-local load/compile/test operations named by the plan, including downstream recompilation for macro or compile-time protocol changes
- `loop-impact-wide`
  - prefer `just ci`, including the supported implementation matrix only when required by the repo contract
- `loop-landing-check`
  - prefer the repo-declared pre-commit/pre-push gate, including dependency locks, clean-image tests, generated artifacts, and evidence checks where applicable

Shared loop semantics and authority boundaries live in `disciplines/validation.md`; this section only maps lane-specific implementation choices.

## Omission rule

Do not invent fake formatter, linter, build, or dev targets. Common Lisp repositories vary in delivery shape and quality tooling, so omitted targets should be explicit rather than misleading.

## Minimal-churn rule

Prefer thin delegation to:
- a checked-in script around `asdf:load-system` or `asdf:test-system`
- `qlot exec` when Qlot owns the dependency environment
- an existing image/build/release helper

Do not hide long Lisp bootstrap expressions or dependency installation logic in the `Justfile` when a reviewed repo-local script is clearer.
