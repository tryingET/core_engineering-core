---
summary: "Engineering-core overview, model, lane/discipline catalog, CLI usage, and versioning notes."
read_when:
  - "Orienting to engineering-core as the shared engineering lane and discipline source."
  - "Choosing CLI commands, lane docs, discipline docs, or repo-local override locations."
type: "reference"
---

# engineering-core

Shared lane docs and cross-language discipline docs for day-to-day engineering conventions and command surfaces.

Canonical validation-tier policy lives in:
`~/ai-society/holdingco/governance-kernel/docs/dev/validation-tier-policy.md`.

## Model

```text
language lane              = ecosystem-specific tooling and commands
discipline                 = cross-language engineering invariant
conditional lane addendum  = narrower guidance loaded only when relevant
repo engineering.local.md   = repo-specific overrides and chosen subset
```

Use broad discipline guidance without forcing every repo to ingest every detail.

Governance references:

- `docs/authority-map.md` defines which owner surface owns shared guidance, repo-local deviations, templates, validation policy, and runtime truth.
- `docs/discipline-lifecycle.md` defines when to add, split, merge, or relocate discipline guidance.

## Why this is a git repo + CLI (not Codex slash commands)

We intentionally keep the “core + divergence” mechanism **outside** Codex prompts:

- **Agent routing (`ai-society-core-repo-router`)** should send engineering lane, discipline, and repo-local override questions here.
- **This repo + git tags** is the right place for *distribution and versioning* of the shared lane and discipline docs.
- **CLI (`engineering-core`)** is the right place for *automation outside Codex* (scripts/CI/quick printing), and can be installed/run via `uv tool …` from a local path or from `git+…@<tag>`.

Slash commands were removed because they duplicated the skill/CLI, increased cognitive overhead (“which entry point do I use?”), and risked drifting out of sync with the canonical workflow.

## Layout

- `lanes/engineering-py.md` — Python lane
- `lanes/engineering-ts.md` — Bun-first general TypeScript lane
- `lanes/engineering-ts.frontend.md` — conditional frontend application addendum
- `lanes/engineering-pi-ts.md` — Node/npm lane for pi extension packages
- `lanes/engineering-go.md` — Go lane
- `lanes/engineering-cpp.md` — C++ lane
- `lanes/engineering-rust.md` — Rust lane
- `lanes/engineering-rust.build-graph.md` — conditional Buck2/Bazel/build-graph acceleration addendum for Rust
- `lanes/engineering-elixir.md` — Elixir / OTP / Phoenix lane
- `lanes/engineering-<lane>.justfile.md` — standardized Justfile addenda
- `lanes/engineering-ts.ts-quality.md` / `engineering-pi-ts.ts-quality.md` — TypeScript quality addenda
- `lanes/engineering-cpp.cuda.md` — C++ CUDA/GPU addendum
- `disciplines/` — cross-language discipline docs
- `templates/` — adoption, validation, data, observability, security/privacy, and docs-authority templates
- `catalog.json` — machine-readable lane/addendum/discipline/template/profile catalog

## Which lane?

- `py`: Python lane
- `ts`: general TypeScript lane (Bun-centric)
- `ts + ts-frontend`: general TypeScript lane plus frontend application addendum; do not use `ts-frontend` alone
- `pi-ts`: TypeScript lane for pi extension package repos (Node 22 + npm + release-check/release-please)
- `go`: Go lane
- `cpp`: C++ lane; use CUDA addendum only for CUDA/GPU work
- `rust`: Rust lane
- `rust + rust-build-graph`: Rust lane plus evidence-gated Buck2/Bazel/build-graph acceleration addendum; do not use `rust-build-graph` alone
- `elixir`: Elixir / OTP / Phoenix lane

## Cross-language disciplines

Disciplines state what must remain true across programming languages. Lanes map that truth into ecosystem-native tools.

Available disciplines:

- `design-system` — tokens, components, motion, assets, visual consistency.
- `accessibility` — operability and semantics across web, docs, CLI/TUI, native UI, and custom renderers.
- `validation` — validation tiers, command surfaces, and evidence expectations.
- `testing` — test taxonomy and when each test form earns its cost.
- `local-first-data` — local state, persistence, migrations, sync, corruption, and authority.
- `observability` — logs, metrics, traces, profiles, health, and runtime evidence.
- `security-privacy` — secrets, permissions, dependency risk, data classification, privacy posture.
- `documentation` — docs authority, front matter, generated projections, and update discipline.
- `specification-and-dsls` — implicit DSL audits, formalization thresholds, schemas, generators, and executable policy.
- `engineering-reasoning` — lightweight reasoning-mode router for deductive, abductive, inductive, adversarial, and Prompt Vault-supported methods.
- `build-graph-acceleration` — evidence-gated adoption of Buck2, Bazel, Pants, Nx/Turborepo, remote cache, and remote execution.
- `dependency-governance` — dependency addition, pinning, review, upgrades, and removal.
- `service-api` — API boundaries, contracts, auth, errors, idempotency, jobs, health/readiness, migrations, deployment, and rollback.
- `ai-ml` — model assets, inference boundaries, evals, dataset/prompt/model provenance, privacy, safety claims, and reproducibility.
- `performance` — profiling, budgets, benchmark hygiene, regression gates, frontend/backend/GPU measurements, and evidence.
- `release-package` — semantic versions, changelogs, artifact provenance, publishing, compatibility, migration releases, deprecation, and rollback.
- `data-governance` — data authority, schemas, lineage, lifecycle, quality, retention, privacy, migrations, and projections.
- `domain-modeling` — domain vocabulary, invariants, workflows, state transitions, aggregate boundaries, and anti-corruption layers.
- `design-patterns` — shared pattern vocabulary for factory, actor, adapter, repository, saga, state machine, and related recurring solution shapes.

Typical combinations:

```text
browser app       -> ts + ts-frontend + design-system + accessibility + validation + testing + security-privacy + performance
local-first app   -> lane(s) + local-first-data + security-privacy + validation + testing
service/API       -> lane(s) + service-api + validation + testing + observability + security-privacy + dependency-governance + specification-and-dsls
AI/ML feature     -> lane(s) + ai-ml + data-governance + validation + testing + observability + security-privacy + performance
data-heavy system -> lane(s) + data-governance + domain-modeling + validation + testing + security-privacy
native/GPU tool   -> cpp/rust + validation + testing + observability + security-privacy + performance (+ ai-ml or the C++ CUDA addendum when relevant)
released package  -> lane(s) + release-package + validation + testing + dependency-governance + security-privacy
docs/generated UI -> lane(s) + documentation + accessibility + design-system + specification-and-dsls
```

## Conditional addenda

Some lane guidance is intentionally split so the main lane docs stay lean.

Current pattern:

- main lane doc = always-safe baseline for language tooling and commands
- companion addendum = read only when a narrower concern actually applies
- discipline doc = read when a cross-language concern applies

Examples:

- `engineering-<lane>.justfile.md` is read only when a repo is missing or reconciling the standardized Justfile surface.
- `engineering-<lane>.ts-quality.md` is read only when a TypeScript repo is adopting deterministic screening with `ts-quality`.
- `engineering-cpp.cuda.md` is read only when a repo builds CUDA code, PyTorch C++/CUDA extensions, GPU kernels, PTX/SASS inspection, or GPU benchmark evidence.
- `engineering-rust.build-graph.md` is read only when a Rust repo has measured build/test-time pain and is evaluating Buck2, Bazel, remote cache/execution, or another build graph accelerator.
- `engineering-ts.frontend.md` is read only for browser apps, SPAs, interactive UIs, local-first frontend user data, camera/media UI, or design-heavy frontends.
- React/Svelte/Vue/etc. framework addenda are intentionally deferred; add one only after repos prove recurring framework-specific guidance that does not belong in the general frontend addendum or a repo-local override.

## Cross-lane quality-tool characteristics

Each lane should choose ecosystem-native quality tools, but the desirable characteristics are shared:

- deterministic CLI invocation, not editor-only enforcement
- checked-in configuration where the tool supports it
- separate write/fix mode and CI-safe check mode
- generated, vendored, and build-output paths excluded explicitly
- local/package-manager/toolchain invocation instead of global-install assumptions
- pinned or toolchain-governed versions when dependencies are introduced
- minimal baseline tooling; optional tools stay conditional until a repo proves the need

Examples: TypeScript uses Biome for the format/lint realization; frontend state/interaction guidance lives in `ts-frontend` and the design/accessibility disciplines. Python uses Ruff; Go uses `gofmt`, `go vet`, and `go test` with optional pinned lint tools; Rust uses rustfmt/clippy; C++ uses clang-format/clang-tidy when configured.

## Per-repo overrides

Add repo-specific adjustments in one of:

- `.codex/engineering.local.md`
- `.claude/docs/engineering.local.md`
- `docs/engineering.local.md`

Treat the override as higher priority than the lane and discipline docs.

A good repo-local override states:

- selected lane(s)
- selected discipline(s)
- deliberate deviations
- canonical local commands
- validation evidence expected before handoff

## Versioning and release

Use the local release workflow in `docs/releases/release-workflow.md`:

```bash
python scripts/release-local.py plan --version <next-version>
python scripts/release-local.py verify --version <next-version>
python scripts/release-local.py tag --version <next-version> --apply
```

`dist/` is generated proof output from `uv build`; do not commit wheels or source distributions unless the release policy changes explicitly. See `docs/releases/artifact-policy.md`.

## CLI

### Run from this repo (no install)

- List lanes: `uv tool run --from . engineering-core list`
- List disciplines: `uv tool run --from . engineering-core list-disciplines`
- List templates: `uv tool run --from . engineering-core list-templates`
- List recommendation profiles: `uv tool run --from . engineering-core list-profiles --prefer-repo`
- Print catalog JSON: `uv tool run --from . engineering-core catalog --pretty --prefer-repo`
- Print discipline overview: `uv tool run --from . engineering-core overview --prefer-repo` or `uv tool run --from . engineering-core show-discipline README --prefer-repo`
- Print a template: `uv tool run --from . engineering-core show-template validation-tier-map --prefer-repo`
- Recommend a profile: `uv tool run --from . engineering-core recommend browser-app --prefer-repo`
- Recommend from repo metadata: `uv tool run --from . engineering-core recommend --repo /path/to/repo --prefer-repo`
- Print a lane: `uv tool run --from . engineering-core show ts --prefer-repo`
- Print frontend addendum: `uv tool run --from . engineering-core show ts-frontend --prefer-repo`
- Print a lane plus selected disciplines: `uv tool run --from . engineering-core show-all-for ts --with validation testing --prefer-repo`
- Print a discipline: `uv tool run --from . engineering-core show-discipline design-system --prefer-repo`
- Print service/API discipline: `uv tool run --from . engineering-core show-discipline service-api --prefer-repo`
- Get a lane path: `uv tool run --from . engineering-core path py --prefer-repo`
- Get a discipline path: `uv tool run --from . engineering-core discipline-path validation --prefer-repo`

If you’re iterating locally without bumping the version, add `-n` to avoid uv cache surprises:

- `uv tool -n run --from . engineering-core show ts --prefer-repo`

### Install once, then run

- Install: `uv tool install --from . engineering-core`
- Then: `engineering-core list`, `engineering-core catalog --pretty`, `engineering-core recommend browser-app`, `engineering-core show-template engineering-local`, `engineering-core show ts`, or `engineering-core show-discipline validation`.

Note: `uv tool run engineering-core ...` only works if `engineering-core` is already installed or published to a registry.
