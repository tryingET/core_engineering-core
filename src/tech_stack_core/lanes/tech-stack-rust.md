# Rust lane — services, CLIs, and systems code

Use this lane when Rust is the requested implementation language or when reliability/performance constraints justify a compiled systems language.

## Core stack

- **Toolchain / package manager:** `rustup` + stable Rust + `cargo`
- **Edition baseline:** Rust 2024 when available in repo policy; otherwise latest stable supported edition
- **Web/API:** Axum for HTTP services; Clap for CLIs
- **Data:** PostgreSQL • SQLx (compile-time checked SQL) or Diesel when schema-first ORM ergonomics matter
- **Async/runtime:** Tokio
- **Validation / contracts:** Serde + schemars where JSON schema/contracts matter
- **Code quality:** `rustfmt` • `clippy` • `cargo deny` for supply chain checks
- **Testing:** `cargo test` • `cargo nextest` for larger suites • `proptest` for property testing • `cucumber-rs` when executable BDD scenarios are worth the maintenance cost
- **Template/rendering:** `minijinja` for Jinja-style text/config templating • `askama` when compile-time checked templates are worth the extra structure
- **Observability:** `tracing` + OpenTelemetry exporters
- **Deployment:** multi-stage Docker builds with slim runtime images

## Command baseline

- Install/update toolchain: `rustup update`
- Format: `cargo fmt --all`
- Lint: `cargo clippy --all-targets --all-features -- -D warnings`
- Test: `cargo test --all-features`
- Fast test runner (optional): `cargo nextest run --all-features`
- Build release artifact: `cargo build --release`

## Testing guidance

- Default unit/integration runner: `cargo test`
- Property/fuzz testing: `proptest` for invariant-heavy logic; honggfuzz/libFuzzer integrations only when the risk profile warrants them
- Behavior/Gherkin testing: `cucumber-rs` only when executable user/workflow scenarios materially improve shared understanding
- Prefer the smallest deterministic test surface that proves the contract

## Template / rendering guidance

- Text/config/prompt templating: `minijinja` when Jinja-style reusable templates pay for themselves
- HTML/text templates with compile-time checking: `askama` when the repo ships real template assets and wants stronger compile-time guarantees
- Prefer plain Rust formatting/builders for small local rendering paths

## Project skeleton

- `Cargo.toml`
- `src/main.rs` or `src/lib.rs`
- `tests/`
- optional: `clippy.toml`, `.cargo/config.toml`, `deny.toml`

## Quality gate architecture

- Enforce checks in CI and git hooks, not editor-only wiring
- Prefer one repo script as the source of truth for format/lint/test/build orchestration
- Keep release/build contracts explicit in repo docs and manifests

## Stack contract surface

When adopting this lane in a repo/package, prefer an explicit contract surface:

- `policy/stack-lane.json` pins the upstream lane and retrieval command
- `docs/tech-stack.local.md` records repo-local deltas
- validation scripts should at least verify the pinned lane metadata; optional smoke checks may also run the `tech-stack-core` CLI when available

## Conditionally loaded addenda

### Justfile addendum

Read the lane-specific Justfile addendum only when:
- `Justfile` is missing
- the standardized targets are absent or drifting
- you are explicitly establishing or reconciling the repo-local `Justfile`

Otherwise, do not load the addendum by default.

Companion doc:
- `tech-stack-rust.justfile.md`
