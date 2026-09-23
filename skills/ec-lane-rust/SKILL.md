---
name: ec-lane-rust
description: "[ec-lane] Rust engineering lane for ecosystem-specific tooling, commands, and implementation defaults. Load when: Working in a repo or package whose selected engineering-core lane is rust.; Choosing Rust tooling, command surfaces, quality defaults, or ecosystem-specific validation."
---

---
summary: "Rust engineering lane for ecosystem-specific tooling, commands, and implementation defaults."
read_when:
  - "Working in a repo or package whose selected engineering-core lane is rust."
  - "Choosing Rust tooling, command surfaces, quality defaults, or ecosystem-specific validation."
type: "guide"
---

# Rust lane — services, CLIs, and systems code

Use this lane when Rust is the requested implementation language or when reliability/performance constraints justify a compiled systems language.

## Core toolchain and defaults

- **Toolchain / package manager:** `rustup` + stable Rust pinned in `rust-toolchain.toml` + `cargo`
- **Edition baseline:** Rust 2024 when available in repo policy; otherwise latest stable supported edition
- **Web/API:** Axum for HTTP services; Clap for CLIs
- **Data:** PostgreSQL • SQLx (compile-time checked SQL) or Diesel when schema-first ORM ergonomics matter
- **Async/runtime:** Tokio
- **Validation / contracts:** Serde + schemars where JSON schema/contracts matter
- **Code quality:** `rustfmt` • `clippy` • `cargo deny check` for supply chain checks (needs `deny.toml` and `package.license`)
- **Testing:** `cargo test` • `cargo nextest` for larger suites • `proptest` for property testing • `cucumber-rs` when executable BDD scenarios are worth the maintenance cost
- **Template/rendering:** `minijinja` for Jinja-style text/config templating • `askama` when compile-time checked templates are worth the extra structure
- **Observability:** `tracing` + OpenTelemetry exporters
- **Deployment:** multi-stage Docker builds with slim runtime images


## Applicable cross-language disciplines

Load disciplines when the concern applies:

- `validation` and `testing` for command tiers, property/fuzz decisions, and evidence.
- `dependency-governance` and `security-privacy` for crates, native dependencies, secrets, and supply chain.
- `service-api` for Axum/RPC/event boundaries, contracts, auth, idempotency, jobs, migrations, deployment, and rollback.
- `observability` for services, CLIs, tracing, benchmarks, and runtime evidence.
- `performance` for profiling, latency/throughput/memory/startup budgets, benchmark hygiene, and regression gates.
- `ai-ml` when Rust hosts inference, wraps model runtimes, or enforces LLM/tooling boundaries.
- `data-governance` for canonical data, schemas, identifiers, lineage, migrations/backfills, projections, retention, and quality.
- `domain-modeling` for vocabulary, invariants, workflows, state transitions, and anti-corruption boundaries.
- `design-patterns` when reviewing named patterns such as factory, adapter, actor, repository, saga, state machine, or policy object.
- `local-first-data` for files, SQLite/embedded DBs, migrations, projections, and sync.
- `release-package` for crates, binaries, containers, changelogs, artifact provenance, compatibility, and rollback.
- `documentation` for docs authority and generated artifacts.
- `build-graph-acceleration` plus `engineering-rust.build-graph.md` only when measured build/test-time pain justifies evaluating Buck2, Bazel, remote cache/execution, or another secondary build graph; Cargo remains canonical until an accepted decision changes that.
- `design-system` and `accessibility` for native UI, TUI, generated docs, or web UI surfaces.

## Command baseline

- Toolchain: pin it in `rust-toolchain.toml` (below); rustup installs and selects it automatically. Without a pin, a machine whose rustup default is nightly silently runs every command on nightly.
- Format (fixer): `cargo fmt --all`; gate: `cargo fmt --all --check`
- Lint: `cargo clippy --workspace --all-targets --all-features --locked -- -D warnings`
- Test: `cargo test --workspace --all-features --locked`
- Fast test runner (optional): `cargo nextest run --workspace --all-features --locked`. nextest doesn't run doctests; pair it with `cargo test --workspace --doc --locked`.
- Supply chain: `cargo deny check` (bootstrap a config with `cargo deny init`, or start from the `deny.toml` below)
- Build release artifact: `cargo build --workspace --release --locked`

Use `--workspace` on every cargo command. In a workspace whose root is also a package, cargo commands without it cover only the root package, so a member's failing test or lint passes silently. Use `--locked` so gates never re-resolve `Cargo.lock`.

**rust-toolchain.toml:**
```toml
[toolchain]
channel = "1.98.0"
components = ["rustfmt", "clippy"]
profile = "minimal"
```

**deny.toml:**
```toml
[graph]
all-features = true

[licenses]
allow = ["MIT", "Apache-2.0"]

[bans]
multiple-versions = "deny"
wildcards = "deny"

[sources]
unknown-registry = "deny"
unknown-git = "deny"
```

Widen `licenses.allow` deliberately; `cargo deny check` fails on any crate (including your own) whose license isn't listed.

**Tool install:**
```bash
cargo install --locked cargo-deny@0.20.2
```

**Quality gates:**
```bash
# toolchain
rustc --version | grep -F 'rustc 1.98.0' && cargo deny --version | grep -Fx 'cargo-deny 0.20.2'
# fmt
cargo fmt --all --check
# lint
cargo clippy --workspace --all-targets --all-features --locked -- -D warnings
# test
cargo test --workspace --all-features --locked
# supply-chain
cargo deny check
# build
cargo build --workspace --release --locked
```

`scripts/lane-conformance.py rust` runs these gates on a fixture workspace (a root package plus a member) at every engineering-core release.

## Testing guidance

- Default unit/integration runner: `cargo test`
- Property/fuzz testing: `proptest` for invariant-heavy logic; honggfuzz/libFuzzer integrations only when the risk profile warrants them
- Behavior/Gherkin testing: `cucumber-rs` only when executable user/workflow scenarios materially improve shared understanding
- Prefer the smallest deterministic test surface that proves the contract

## Template / rendering guidance

- Text/config/prompt templating: `minijinja` when Jinja-style reusable templates pay for themselves
- HTML/text templates with compile-time checking: `askama` when the repo ships real template assets and wants stronger compile-time guarantees
- Prefer plain Rust formatting/builders for small local rendering paths

## Dependency freshness policy

Cargo does not currently have a stable built-in equivalent to npm/uv-style package age gates.

Recommended practical policy:
- use `--locked` for normal workflows
- refresh `Cargo.lock` intentionally
- if you want a 7-day delay policy, use a wrapper such as:

```bash
cutoff="$(date -u -d '7 days ago' '+%Y-%m-%dT%H:%M:%SZ')"
cargo +nightly generate-lockfile -Z unstable-options --publish-time "$cutoff"
```

This is a workflow convention, not a stable Cargo config key.

Nightly also has a config-based age gate: `[registry] global-min-publish-age = "7 days"` in `.cargo/config.toml`, honored only with `-Z min-publish-age` (for example `cargo +nightly generate-lockfile -Z min-publish-age`). Stable cargo prints `warning: ignoring registry.global-min-publish-age` and resolves without the gate, so don't rely on that key under a stable toolchain.

## Project skeleton

- `Cargo.toml`
- `src/main.rs` or `src/lib.rs`
- `tests/`
- `rust-toolchain.toml`, `deny.toml`
- optional: `clippy.toml`, `.cargo/config.toml`

## Quality gate architecture

- Enforce checks in CI and git hooks, not editor-only wiring
- Prefer one repo script as the source of truth for format/lint/test/build orchestration
- Keep release/build contracts explicit in repo docs and manifests

## Engineering lane contract surface

When adopting this lane in a repo/package, prefer an explicit contract surface:

- `policy/engineering-lane.json` pins the upstream lane and retrieval command
- `docs/engineering.local.md` records repo-local deltas
- validation scripts should at least verify the pinned lane metadata; optional smoke checks may also run the `engineering-core` CLI when available

## Conditionally loaded addenda

### Justfile addendum

Read the lane-specific Justfile addendum only when:
- `Justfile` is missing
- the standardized targets are absent or drifting
- you are explicitly establishing or reconciling the repo-local `Justfile`

Otherwise, do not load the addendum by default.

Companion doc:
- `engineering-rust.justfile.md`
