---
summary: "Rust lane standardized Justfile addendum."
read_when:
  - "A repo using the Rust lane is missing, establishing, or reconciling the standardized Justfile surface."
  - "Standard targets are absent, drifting, or need lane-specific command mapping."
type: "guide"
---

# Rust lane — standardized Justfile addendum

Read this addendum only when a repo using the Rust lane is missing the standardized Justfile surface, the standard targets are absent/drifting, or you are explicitly establishing/reconciling `Justfile` behavior.

Use this with `disciplines/validation.md` and the repo's applicable standardized Justfile contract, not instead of them.

## Mapping rule

Standardize the outer `just` command names while keeping the implementation thin and Rust-native.
Prefer existing repo-local scripts when they already own validation or CI behavior.

## Recommended target mappings

- `just help`
  - prefer: `just --list`
- `just test`
  - prefer: `cargo test --all-features`
  - if the repo already standardizes a quieter wrapper, delegate to that wrapper instead
- `just check`
  - prefer existing fast repo gate when present
  - fallback: `cargo check --workspace`
- `just build`
  - prefer: `cargo build --release`
- `just lint`
  - prefer: `cargo clippy --all-targets --all-features -- -D warnings`
- `just fmt`
  - prefer: `cargo fmt --all`
- `just ci`
  - prefer existing full repo-local validation/CI wrapper when present
  - fallback: run formatting/lint/test/build in the repo's documented order
- `just doctor`
  - prefer existing repo-local environment/runtime sanity command when present
  - fallback: a small Rust toolchain sanity check such as `rustup show active-toolchain && cargo --version`
- `just dev`
  - include only when the repo has a meaningful long-running dev/watch surface
  - common Rust examples: `cargo run`, `cargo watch -x run`, or a repo-local dev script

## Optional repo-loop-validation-v1 mappings

Rust repos that participate in agent/prompt orchestration loops may adopt `repo-loop-validation-v1` as thin `just loop-*` recipes that delegate to Cargo-native validation or repo-local wrappers.

Recommended Rust mappings:

- `loop-doctor`
  - prefer a non-failing diagnostic that reports Rustup/Cargo/toolchain versions, feature/workspace posture, dirty tree, task-scope binding, and known blockers
  - fallback: capture `just doctor` output and documented scope diagnostics without making `loop-doctor` fail
- `loop-verify-fast`
  - prefer the fastest truthful focused gate, such as package-local `cargo test -p <crate>`, `cargo check -p <crate>`, targeted clippy, or existing `just check`
- `loop-impact-plan`
  - prefer a repo-local changed-file classifier that maps crates, integration tests, build scripts, features, lockfiles, generated code, and docs to bounded/expanded/wide checks
- `loop-impact-run`
  - prefer the bounded/expanded checks named by the plan, usually crate-local check/clippy/test for touched crates
- `loop-impact-wide`
  - prefer `just ci` or the repo's full local validation wrapper when wide impact is accepted
- `loop-landing-check`
  - prefer the repo-declared pre-commit/pre-push readiness gate, including lockfile, generated-code, task-scope, and evidence checks where applicable

Shared loop semantics and authority boundaries live in `disciplines/validation.md`; this section only maps lane-specific implementation choices.

## Omission rule

Do not invent fake long-running behavior.
If the repo has no natural dev/watch mode, omit `just dev` and record that omission in the implementation summary.

## Minimal-churn rule

Prefer wrappers like:
- `./scripts/validate.sh --quiet-success fast`
- `./scripts/ci/full.sh --quiet-success`
- existing repo-local build/dev helpers

Do not move large orchestration logic into the `Justfile` if a script already owns it cleanly.
