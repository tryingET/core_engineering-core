---
summary: "C++ lane standardized Justfile addendum."
read_when:
  - "A repo using the C++ lane is missing, establishing, or reconciling the standardized Justfile surface."
  - "Standard targets are absent, drifting, or need lane-specific command mapping."
type: "guide"
---

# C++ lane — standardized Justfile addendum

Read this addendum only when a repo using the C++ lane is missing the standardized Justfile surface, the standard targets are absent/drifting, or you are explicitly establishing/reconciling `Justfile` behavior.

Use this addendum with `disciplines/validation.md` and the repo's applicable standardized Justfile contract.

## Mapping rule

Standardize the outer `just` command names while keeping implementation thin and CMake/C++-native.
Prefer existing repo-local scripts, CMake presets, and CI wrappers when they already define the canonical workflow.

## Recommended target mappings

- `just help`
  - prefer: `just --list`
- `just doctor`
  - print the pinned tool and compiler versions without installing anything globally
- `just fmt`
  - prefer: `clang-format -i` over tracked C/C++/CUDA files
- `just lint`
  - prefer: repo-local lint wrapper, otherwise `run-clang-tidy.py -p build-ci -quiet` with a checked-in `.clang-tidy`
- `just test`
  - prefer: `ctest --preset ci` (the preset errors when no tests are found)
- `just build`
  - prefer: `cmake --preset ci && cmake --build --preset ci`
- `just check`
  - prefer: format check + lint + test
- `just ci`
  - prefer the repo's canonical full local validation/CI wrapper when present; otherwise `check` plus the sanitizer workflow
- optional `just bench`
  - include only when the repo has benchmark targets or benchmark-labeled CTest tests
- optional `just run`
  - include only when the repo has a meaningful default executable/service target
- optional `just clean`
  - remove repo-local build artifacts only

## Reference implementation sketch

Use this as a starting point, not a mandatory copy. It delegates to the lane's `CMakePresets.json` and pinned tools; repos with other presets or existing scripts should delegate to those instead. Note that `just` passes `$$` through to the shell unchanged (bash expands it to the process ID), so recipes use a single `$`.

**Justfile:**
```just
set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

sources := "git ls-files --cached --others --exclude-standard '*.c' '*.cc' '*.cpp' '*.cxx' '*.h' '*.hh' '*.hpp' '*.cu' '*.cuh'"

help:
    @just --list

doctor:
    cmake --version
    ninja --version
    clang-format --version
    clang-tidy --version
    ${CXX:-c++} --version

build:
    cmake --preset ci
    cmake --build --preset ci

test: build
    ctest --preset ci

sanitize:
    cmake --workflow --preset asan

fmt:
    files="$({{sources}})"; [ -z "$files" ] || clang-format -i $files

fmt-check:
    files="$({{sources}})"; [ -z "$files" ] || clang-format --dry-run --Werror $files

lint: build
    run-clang-tidy.py -p build-ci -quiet

check: fmt-check lint test

ci: check sanitize

clean:
    rm -rf build-ci build-asan
```

## Optional repo-loop-validation-v1 mappings

C++ repos that participate in agent/prompt orchestration loops may adopt `repo-loop-validation-v1` as thin `just loop-*` recipes that delegate to CMake/preset validation or repo-local wrappers.

Recommended C++ mappings:

- `loop-doctor`
  - prefer a non-failing diagnostic that reports compiler/CMake/generator versions, configured build directory, dirty tree, task-scope binding, and known blockers
  - fallback: capture `just doctor` output and documented scope diagnostics without making `loop-doctor` fail
- `loop-verify-fast`
  - prefer the fastest truthful focused gate, such as targeted compile/test for touched components, `ctest -R <pattern>`, non-mutating format checks/lint, or existing `just check`
- `loop-impact-plan`
  - prefer a repo-local changed-file classifier that maps source/headers, CMake/presets, generated code, ABI/API surfaces, tests, and docs to bounded/expanded/wide checks
- `loop-impact-run`
  - prefer the bounded/expanded checks named by the plan, usually configure/build plus targeted CTest/lint for touched components
- `loop-impact-wide`
  - prefer `just ci` or the repo's full local validation wrapper when wide impact is accepted
- `loop-landing-check`
  - prefer the repo-declared pre-commit/pre-push readiness gate, including build artifact, generated-code, task-scope, and evidence checks where applicable

Shared loop semantics and authority boundaries live in `disciplines/validation.md`; this section only maps lane-specific implementation choices.

## Omission rule

Do not invent fake long-running `run` behavior or fake benchmark targets.
If the repo is a library with no default executable, omit `just run` or make it delegate to a real example target.
If the repo has no benchmark contract, omit `just bench`.

## Minimal-churn rule

Prefer thin wrappers around:

- existing `./scripts/validate*` or CI wrappers
- CMake presets such as `cmake --preset dev`
- `cmake --build` and `ctest`
- existing benchmark or release scripts

Do not move large orchestration logic into the `Justfile` if a script, CMake preset, or CI workflow already owns it cleanly.
