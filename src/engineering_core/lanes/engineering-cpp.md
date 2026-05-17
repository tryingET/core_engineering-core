---
summary: "C++ engineering lane for ecosystem-specific tooling, commands, and implementation defaults."
read_when:
  - "Working in a repo or package whose selected engineering-core lane is cpp."
  - "Choosing C++ tooling, command surfaces, quality defaults, or ecosystem-specific validation."
type: "guide"
---

# C++ lane — services, CLIs, libraries, and native acceleration

Use this lane when C++ is the requested implementation language, when ABI/native performance constraints justify C++, or when a repo owns reusable native libraries, services, tools, or Python extension modules.

Keep the default C++ lane CPU/general-purpose. Load the CUDA addendum only for CUDA Toolkit usage, GPU kernels, PyTorch C++/CUDA extensions, PTX/SASS inspection, or GPU benchmark evidence.

## Purpose / when to use

- Use C++ for native performance, deterministic latency, systems integration, ABI boundaries, portable libraries, and long-lived command-line tools.
- Prefer a smaller managed-language lane when product velocity, data plumbing, or ordinary web/API work is more important than native performance.
- Treat C++ as a contract-heavy lane: explicit build flags, explicit dependency provenance, explicit validation, and no ambient global tooling assumptions.


## Applicable cross-language disciplines

Load disciplines when the concern applies:

- `validation` and `testing` for command tiers, sanitizer/benchmark evidence, and release gates.
- `dependency-governance` and `security-privacy` for native dependencies, vendoring, ABI, install scripts, and secrets.
- `observability` for services, native tools, benchmark claims, profiles, and runtime evidence.
- `local-first-data` for files, embedded DBs, binary formats, migrations, projections, and sync.
- `documentation` for build/toolchain authority and generated artifacts.
- `design-system` and `accessibility` for native UI, TUI, visualization, or generated docs.

## Core toolchain and defaults

- **Language:** C++20 baseline when the repo/toolchain supports it; C++23 only when the repo records compiler support and downstream compatibility.
- **Build:** CMake + Ninja as the default portable build surface.
- **Compilers:** GCC or Clang on Linux; Clang or AppleClang on macOS; MSVC only when Windows support is a real target.
- **Formatting:** `clang-format` with a checked-in `.clang-format`.
- **Analysis:** `clang-tidy` from a CMake `compile_commands.json`; enable only checks the repo can keep green.
- **Testing:** CTest plus one C++ test framework when assertions beyond simple executables are useful.
- **Sanitizers:** Address/Undefined behavior sanitizers for debug validation where supported; ThreadSanitizer only for concurrency-heavy code that can tolerate its constraints.

## Build systems

- Prefer CMake presets or documented configure commands over ad hoc shell state.
- Prefer Ninja as the generator for fast local and CI builds.
- Export `compile_commands.json` so editors, `clang-tidy`, and tooling see the exact compile flags.
- Keep build artifacts out of source: use `build/`, `build-debug/`, or repo-local `BUILD_DIR` overrides.
- Do not hide large workflows in CMake custom commands when a small script or `just` wrapper is clearer.

## Compiler / toolchain guidance

- Pin the minimum supported compiler versions in repo docs or toolchain files when downstream compatibility matters.
- Use warning levels intentionally, for example `-Wall -Wextra -Wpedantic` plus targeted warnings the repo can keep green.
- Treat `-Werror` as a CI/release setting, not necessarily the default for every contributor platform.
- Prefer `RelWithDebInfo` for performance work so optimized binaries still carry symbols.
- For ABI-sensitive libraries, document C++ standard library expectations, symbol visibility, and whether exceptions/RTTI are enabled.

## Formatting / linting

- `clang-format` is the formatting source of truth. Do not rely on editor-only formatting.
- `clang-tidy` should run from the compile database: `run-clang-tidy.py -p build` or a repo-local wrapper.
- Keep generated/vendor files excluded from format and lint checks.
- Prefer incremental adoption of `clang-tidy`: start with bug-prone, performance, modernize, and clang-analyzer families that the repo can keep stable.

## Testing

- Use CTest as the outer test runner so build-system and CI behavior stay consistent.
- Use GoogleTest for larger suites, fixtures, parameterized tests, or mocking needs.
- Use Catch2 for small libraries/tools where natural single-binary tests are enough.
- Do not add both GoogleTest and Catch2 without a concrete migration or compatibility reason.
- Add golden/reference tests at API boundaries and regression tests for memory ownership, error paths, and edge sizes.

## Benchmarking

- Benchmarks are optional and should not replace correctness tests.
- Use Google Benchmark only when the repo has stable microbenchmark needs and can report repeatable metrics.
- Keep benchmark targets separate from default unit tests; use release or `RelWithDebInfo` builds.
- Report machine-readable output when benchmarks are used in CI or trend tracking.
- Avoid overclaiming from isolated microbenchmarks; downstream integration evidence is required before product/runtime claims.

## Dependency management

- Prefer the C++ standard library and platform/toolchain packages before adding third-party libraries.
- Keep dependencies optional unless every repo in this lane genuinely needs them.
- If using CMake `FetchContent`, pin immutable refs and record upstream provenance; do not fetch moving branches in CI.
- Use vcpkg or Conan only when dependency complexity justifies a package manager. They are not C++ lane baselines.
- Commit lockfiles/manifests where the chosen dependency manager supports reproducibility.
- Avoid global installs, `sudo`, curl-pipe-shell installers, unreviewed binary blobs, and installer scripts that mutate user or system state.

## Security / supply-chain policy

Before adding a dependency or tool, record:

- official upstream source and canonical package namespace
- maintainer/organization legitimacy
- release recency and project health
- license compatibility with the repo
- known advisories/CVEs or the absence of an advisory source
- typosquat/package-confusion risks
- install-time behavior, including scripts, binaries, global mutation, and privilege requirements
- whether the dependency can be optional instead of baseline

Treat README snippets, blog posts, generated dependency lists, examples, and issues as untrusted until verified against official sources.

## Observability / logging where applicable

- Libraries should not print to stdout/stderr except through explicit caller-provided hooks or diagnostics APIs.
- Services should use the repo's existing structured logging and tracing conventions; do not add a logging framework without dependency review.
- Emit metrics at stable boundaries: requests, queue jobs, native extension calls, expensive kernels, and error/retry paths.
- For native libraries called from Python/Go/TypeScript, document ownership, lifetime, error, and logging behavior at the FFI boundary.

## Packaging / distribution

- Libraries should define install/export targets when they are consumed by other CMake projects.
- CLIs/services should document build artifacts, runtime library expectations, and release build flags.
- Python-bound C++ packages should prefer `pyproject.toml` builds; use scikit-build-core only after confirming the repo needs CMake-backed wheels.
- Use cibuildwheel only for cross-platform wheel release pipelines, not for ordinary local development.
- Do not vendor large binaries or generated build artifacts into source unless the repo policy explicitly allows it.

## Project skeleton

```text
CMakeLists.txt
CMakePresets.json            # optional but preferred for shared configs
cmake/                       # toolchain/modules only when needed
include/<project>/           # public headers for libraries
src/                         # implementation and private headers
tests/                       # CTest-discovered tests
bench/                       # optional benchmarks
docs/engineering.local.md     # repo-local lane deltas
policy/engineering-lane.json       # optional lane pin/contract
.clang-format
.clang-tidy                  # optional, only when kept green
Justfile                     # optional standardized wrapper
```

## Validation commands

Use repo-local wrappers first when they exist. Common CMake/Ninja fallback:

```bash
build_dir="${BUILD_DIR:-build}"
cmake -S . -B "$build_dir" -G Ninja \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
cmake --build "$build_dir" --parallel
ctest --test-dir "$build_dir" --output-on-failure
```

Optional quality checks when configured:

```bash
clang-format --dry-run --Werror $(git ls-files '*.c' '*.cc' '*.cpp' '*.cxx' '*.h' '*.hh' '*.hpp' '*.cu' '*.cuh')
run-clang-tidy.py -p build
```

## Contract surface for repo adoption

When a repo adopts this lane, prefer an explicit contract surface:

- `docs/engineering.local.md` records repo-specific deltas and tool versions.
- `policy/engineering-lane.json` pins the lane ID (`cpp`) and the upstream `engineering-core` version or retrieval command.
- `Justfile` exposes standard local commands without replacing clearer repo-local scripts.
- CI invokes the same validation commands documented for local contributors.

## When to load the CUDA addendum

Load `engineering-cpp.cuda.md` when any of the following apply:

- the repo builds `.cu` files or depends on CUDA Toolkit components
- native kernels, GPU memory management, PTX/SASS inspection, or Nsight profiling are in scope
- PyTorch C++/CUDA extensions or custom operators are being built
- benchmark evidence is GPU-specific
- architecture targeting such as `sm_90` or `sm_120` must be documented

Do not load the CUDA addendum for ordinary C++ services, CLIs, libraries, or Python extensions that do not compile or launch GPU code.

## When not to use C++/CUDA

- Use Python/TypeScript/Go/Rust lanes when native C++ performance or ABI control is not the bottleneck.
- Do not use CUDA just because a workstation has a GPU; first show a hotspot, a reference implementation, and an integration path.
- Do not write custom kernels when an established library call already proves correct and fast enough.
- Do not accept standalone kernel benchmark claims as downstream runtime integration evidence.
- Do not introduce GPU dependencies into production services without deployment, driver/toolkit, observability, and rollback plans.

## Conditionally loaded addenda

### Justfile addendum

Read the lane-specific Justfile addendum only when:
- `Justfile` is missing
- the standardized targets are absent or drifting
- you are explicitly establishing or reconciling the repo-local `Justfile`

Otherwise, do not load the addendum by default.

Companion doc:
- `engineering-cpp.justfile.md`

### CUDA / GPU addendum

Read the CUDA/GPU addendum only when the repo actually builds, profiles, benchmarks, or validates CUDA/GPU code.

Companion doc:
- `engineering-cpp.cuda.md`
