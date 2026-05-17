# Rust Lane — Build Graph Acceleration Addendum

Read this addendum only when a Rust repo is evaluating Buck2, Bazel, Pants, remote cache/execution, or another secondary build graph because Cargo build/test time is a measured bottleneck.

Use with:

- `engineering-rust.md`
- `disciplines/build-graph-acceleration.md`
- `disciplines/validation.md`
- `disciplines/testing.md`
- `disciplines/dependency-governance.md`

## Baseline rule

Cargo remains the canonical Rust ecosystem baseline.

Buck2 or Bazel may be introduced as an acceleration layer only after build-time evidence and an accepted repo decision. Do not replace Cargo authority until parity, CI behavior, local workflow, and rollback posture are proven.

## When Buck2/Bazel may be justified

Consider a build graph tool when the repo has several of:

- large Rust workspace;
- expensive clean builds;
- slow incremental rebuilds after ordinary edits;
- test compilation dominates local/CI time;
- multi-language graph around Rust crates;
- repeated CI bottlenecks;
- need for remote cache or remote execution;
- stable enough crate graph to encode in secondary build metadata.

Do not adopt for a small Rust crate, a short-lived prototype, or a repo whose real bottleneck is unrelated to build graph structure.

## Measure first

Collect timings before proposing a tool:

```bash
cargo clean
time cargo build --workspace
time cargo test --workspace --no-run
time cargo check --workspace
```

Then collect representative incremental timings after touching:

- a leaf crate;
- a core crate;
- a CLI/bin crate;
- test-only code;
- a dependency or feature declaration.

Classify the bottleneck:

- dependency compile;
- proc macros/codegen;
- linking;
- test compilation;
- feature unification;
- build scripts;
- generated artifacts;
- CI cache misses.

## Cheaper Rust-native improvements first

Evaluate or explicitly reject:

- `cargo check` for fast inner-loop validation;
- `cargo nextest` for test execution improvements;
- `sccache` for compiler output caching;
- `lld` or `mold` for link-time improvement where supported;
- crate graph cleanup;
- feature hygiene and narrower default features;
- reducing proc macro/codegen hot paths;
- CI cache key improvements.

## Buck2 vs Bazel

### Buck2

Prefer evaluating Buck2 when:

- local incremental speed is the dominant pain;
- the repo accepts newer ecosystem tooling;
- the team can maintain Buck rules;
- future remote execution/cache is plausible but not necessarily immediate.

Risks:

- smaller Rust ecosystem/examples than Bazel;
- more repo-local convention;
- additional onboarding and IDE integration work.

### Bazel

Prefer evaluating Bazel when:

- mature remote cache/execution is a primary goal;
- the repo is multi-language or expected to grow that way;
- hermetic/reproducible CI at scale matters more than low ceremony;
- the team can tolerate BUILD/rules complexity.

Risks:

- high onboarding tax;
- Rust dependency/rules integration complexity;
- IDE friction;
- build platform can become larger than the product problem.

## Parity requirements

Before a Buck2/Bazel path becomes accepted:

- Cargo build/test behavior is matched or deliberate differences are documented;
- generated build metadata has an owner and drift check;
- dependency graph translation is reproducible;
- local and CI commands are documented;
- release artifacts are produced by a declared authority path;
- fallback to Cargo remains available until explicitly retired.

## Repo-local documentation

In `docs/engineering.local.md`, record:

```text
Build acceleration posture:
- Cargo remains canonical.
- Candidate tool: Buck2 | Bazel | other.
- Evidence collected: <commands/artifacts>.
- Cheaper native mitigations tried: <list>.
- Accepted role: experiment | optional acceleration | CI gate | release authority.
- Cargo fallback: <command>.
```

## Agent rule

Do not introduce Buck2/Bazel files as a drive-by optimization. First create or reference an accepted task/decision with measured build-time evidence and rollback posture.
