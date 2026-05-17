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

## Omission rule

Do not invent fake long-running behavior.
If the repo has no natural dev/watch mode, omit `just dev` and record that omission in the implementation summary.

## Minimal-churn rule

Prefer wrappers like:
- `./scripts/validate.sh --quiet-success fast`
- `./scripts/ci/full.sh --quiet-success`
- existing repo-local build/dev helpers

Do not move large orchestration logic into the `Justfile` if a script already owns it cleanly.
