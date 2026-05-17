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
  - check local toolchain availability without installing anything globally
- `just fmt`
  - prefer: `clang-format -i` over tracked C/C++/CUDA files
- `just lint`
  - prefer: repo-local lint wrapper, otherwise `run-clang-tidy.py -p {{build_dir}}` when configured
- `just test`
  - prefer: `ctest --test-dir {{build_dir}} --output-on-failure`
- `just build`
  - prefer: `cmake --build {{build_dir}} --parallel`
- `just check`
  - prefer: configure + format check + lint + test
- `just ci`
  - prefer the repo's canonical full local validation/CI wrapper when present
- optional `just bench`
  - include only when the repo has benchmark targets or benchmark-labeled CTest tests
- optional `just run`
  - include only when the repo has a meaningful default executable/service target
- optional `just clean`
  - remove repo-local build artifacts only

## Reference implementation sketch

Use this as a starting point, not a mandatory copy. Repos with CMake presets or existing scripts should delegate to those instead.

```just
set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

build_dir := env_var_or_default("BUILD_DIR", "build")
build_type := env_var_or_default("CMAKE_BUILD_TYPE", "RelWithDebInfo")
generator := env_var_or_default("CMAKE_GENERATOR", "Ninja")
cmake_args := env_var_or_default("CMAKE_ARGS", "")
ctest_args := env_var_or_default("CTEST_ARGS", "--output-on-failure")

help:
    @just --list

doctor:
    @command -v cmake
    @command -v ninja || true
    @(${CXX:-c++} --version || c++ --version)
    @command -v clang-format || true
    @command -v clang-tidy || true

configure:
    cmake -S . -B "{{build_dir}}" -G "{{generator}}" \
      -DCMAKE_BUILD_TYPE="{{build_type}}" \
      -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
      {{cmake_args}}

build: configure
    cmake --build "{{build_dir}}" --parallel

test: build
    ctest --test-dir "{{build_dir}}" {{ctest_args}}

fmt:
    files="$$(git ls-files '*.c' '*.cc' '*.cpp' '*.cxx' '*.h' '*.hh' '*.hpp' '*.cu' '*.cuh' 2>/dev/null || true)"; \
    if [ -n "$$files" ]; then clang-format -i $$files; fi

fmt-check:
    files="$$(git ls-files '*.c' '*.cc' '*.cpp' '*.cxx' '*.h' '*.hh' '*.hpp' '*.cu' '*.cuh' 2>/dev/null || true)"; \
    if [ -n "$$files" ]; then clang-format --dry-run --Werror $$files; fi

lint: configure
    if command -v run-clang-tidy.py >/dev/null 2>&1; then \
      run-clang-tidy.py -p "{{build_dir}}"; \
    elif command -v clang-tidy >/dev/null 2>&1 && [ -f "{{build_dir}}/compile_commands.json" ]; then \
      echo "clang-tidy found; add a repo-local source selection or run-clang-tidy.py wrapper"; \
    else \
      echo "no clang-tidy wrapper configured; relying on compiler warnings"; \
    fi

check: fmt-check lint test

ci: check

bench: build
    if cmake --build "{{build_dir}}" --target help | grep -q '^\.\.\. bench$$'; then \
      cmake --build "{{build_dir}}" --target bench; \
    else \
      ctest --test-dir "{{build_dir}}" -L benchmark --output-on-failure || \
        echo "no benchmark target or benchmark-labeled tests configured"; \
    fi

run: build
    echo "delegate this target to the repo's canonical executable/service command"

clean:
    rm -rf "{{build_dir}}"
```

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
