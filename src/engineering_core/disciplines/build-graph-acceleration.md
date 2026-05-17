---
summary: "Discipline for evidence-gated adoption of build graph accelerators such as Buck2, Bazel, Pants, Nx, Turborepo, and remote cache/execution."
read_when:
  - "A repo proposes Buck2, Bazel, Pants, Nx, Turborepo, remote cache, remote execution, or another secondary build graph."
  - "Build times, test times, or CI times are becoming a material engineering bottleneck."
  - "A repo needs to decide whether native package-manager builds remain sufficient."
type: "reference"
---

# Discipline — Build Graph Acceleration

## Purpose

Build graph tools can radically improve large-repo build and CI performance. They can also become a second platform with its own language, cache semantics, generated files, onboarding tax, IDE friction, and failure modes.

This discipline keeps adoption evidence-gated.

## Core rule

Native ecosystem tooling remains canonical until a repo accepts a build-graph decision with evidence.

Examples:

- Rust: Cargo remains canonical.
- TypeScript: package-manager scripts remain canonical.
- Python: uv/pytest/native scripts remain canonical.
- Go: `go test` / `go build` remain canonical.
- C++: CMake/Ninja may already be the native build graph; extra graph tooling still needs justification.

Buck2, Bazel, Pants, Nx, Turborepo, remote cache, and remote execution are acceleration layers or orchestration layers unless a repo decision explicitly promotes one to build authority.

## Load when

- clean build time blocks iteration;
- incremental rebuilds are too slow;
- CI compile/test time is material;
- the repo is large or multi-language;
- remote cache/execution is being considered;
- generated build files or secondary build metadata appear;
- a build graph tool is proposed as a default command surface.

## Adoption threshold

Before adopting a secondary build graph, collect:

1. current clean build timing;
2. current incremental timing for representative edits;
3. CI timing and cache hit/miss behavior;
4. test compile vs test execution split;
5. bottleneck classification: dependency compile, codegen, proc macros, linking, feature unification, test harness, frontend bundling, container build, or remote artifact fetch;
6. cheaper mitigations tried or rejected;
7. expected improvement and acceptable maintenance cost;
8. rollback/fallback path to native tooling.

## Cheaper fixes first

Prefer native, low-ceremony improvements before a second build graph:

- cache compiler outputs where supported (`sccache`, compiler cache, package-manager cache);
- use faster linkers where appropriate (`lld`, `mold`);
- split slow feature sets or test targets;
- reduce codegen/proc macro hot paths;
- use next-generation native test runners where appropriate;
- avoid rebuilding generated/vendor artifacts unnecessarily;
- make CI cache keys explicit and observable;
- isolate changed-slice validation from full release validation.

## Tool selection

| Tool family | Strong fit | Cost |
|---|---|---|
| Buck2 | fast local incremental graphs, large monorepos, future remote execution | newer ecosystem, more repo-local convention, smaller example base |
| Bazel | mature remote cache/execution, hermetic multi-language CI, large org scale | high onboarding tax, rules complexity, IDE friction |
| Pants | Python/JVM/polyglot build orchestration with less BUILD-file burden | ecosystem fit varies by language and repo shape |
| Nx/Turborepo | JS/TS workspace task graph and cache | weaker for non-JS native builds; can hide package-manager truth |
| CMake/Ninja | C/C++ native graph baseline | not a cross-language monorepo solution by itself |

## Authority and fallback

A build graph tool may become canonical only after:

- parity with native build/test behavior is proven;
- generated build metadata has a source/ownership rule;
- cache correctness is validated;
- CI uses the same command surface operators use;
- fallback to native tooling exists until the repo explicitly retires it.

For most repos, the correct posture is:

```text
native tooling = authority
build graph = optional acceleration/check path
```

## Required repo-local documentation

Record in `docs/engineering.local.md` or an ADR/decision:

- selected build graph tool;
- native fallback command;
- canonical local commands;
- CI commands;
- cache/remote execution policy;
- generated-file ownership;
- measured baseline timings;
- measured target or actual improvement;
- rollback path.

## Validation

At minimum:

- native build/test still passes or accepted fallback retirement is documented;
- build graph build/test passes;
- changed-slice behavior is exercised;
- generated build metadata drift is checked;
- cache behavior is observable enough to debug;
- release artifacts are built by the declared release-authority path.

## Failure modes

- adopting Bazel/Buck2 because it is prestigious, not because measurements justify it;
- build graph passes while native package-manager truth breaks silently;
- generated build files are hand-edited without source authority;
- remote cache hides non-hermetic actions;
- IDE and local developer workflow regress severely;
- CI and local commands diverge;
- acceleration layer becomes an unowned platform.
