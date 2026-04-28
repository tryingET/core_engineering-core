# tech-stack-core

Shared “lane” docs for day-to-day coding conventions and commands.

For repo-local status and next actions, start with:
`next-session-prompt.md`.

For cross-repo ownership/consolidation planning, start with:
`~/ai-society/core/agent-scripts/next-session-prompt.md`.

Canonical validation-tier policy lives in:
`~/ai-society/holdingco/governance-kernel/docs/dev/validation-tier-policy.md`.

## Why this is a git repo + CLI (not Codex slash commands)

We intentionally keep the “core + divergence” mechanism **outside** Codex prompts:

- **Codex skill (`tech-stack-discovery`)** is the right place for *interactive, in-agent* stack detection and “how to work in this repo” guidance.
- **This repo + git tags** is the right place for *distribution and versioning* of the shared lane docs.
- **CLI (`tech-stack-core`)** is the right place for *automation outside Codex* (scripts/CI/quick printing), and can be installed/run via `uv tool …` from a local path or from `git+…@<tag>`.

Slash commands were removed because they duplicated the skill/CLI, increased cognitive overhead (“which entry point do I use?”), and risked drifting out of sync with the canonical workflow.

## Layout

- `lanes/tech-stack-py.md` (symlink to packaged files)
- `lanes/tech-stack-ts.md` (Bun-first general TS lane)
- `lanes/tech-stack-pi-ts.md` (Node/npm lane for pi extension packages)
- `lanes/tech-stack-go.md` (symlink to packaged files)
- `lanes/tech-stack-cpp.md` (C++ lane; load CUDA addendum only for GPU/CUDA work)
- `lanes/tech-stack-rust.md` (Rust lane)
- `lanes/tech-stack-elixir.md` (Elixir / OTP / Phoenix lane)
- optional lane companions such as `lanes/tech-stack-rust.justfile.md`, `lanes/tech-stack-cpp.cuda.md`, or `lanes/tech-stack-ts.ts-quality.md` for conditionally loaded addenda

## Which lane?

- `py`: Python lane
- `ts`: general TypeScript lane (Bun-centric)
- `pi-ts`: TypeScript lane for pi extension package repos (Node 22 + npm + release-check/release-please)
- `go`: Go lane
- `cpp`: C++ lane; use `tech-stack-cpp.cuda.md` only for CUDA/GPU work
- `rust`: Rust lane
- `elixir`: Elixir / OTP / Phoenix lane

## Conditional addenda

Some lane guidance is intentionally split into conditionally loaded companions so the main lane docs stay lean.

Current pattern:
- main lane doc = always-safe baseline for stack/tooling/commands
- companion addendum = read only when a narrower concern actually applies

Examples:
- `tech-stack-<lane>.justfile.md` is the lane-specific Justfile addendum and should be read only when a repo is missing the standardized Justfile surface, the standard targets are absent/drifting, or a workflow is explicitly establishing/reconciling that Justfile.
- `tech-stack-<lane>.ts-quality.md` is the lane-specific `ts-quality` adoption addendum and should be read only when a repo is explicitly adopting deterministic screening with `ts-quality`.
- `tech-stack-cpp.cuda.md` is the C++ lane CUDA/GPU addendum and should be read only when a repo builds CUDA code, PyTorch C++/CUDA extensions, GPU kernels, PTX/SASS inspection, or GPU benchmark evidence.

## Cross-lane quality-tool characteristics

Each lane should choose ecosystem-native quality tools, but the desirable characteristics are shared:

- deterministic CLI invocation, not editor-only enforcement
- checked-in configuration where the tool supports it
- separate write/fix mode and CI-safe check mode
- generated, vendored, and build-output paths excluded explicitly
- local/package-manager/toolchain invocation instead of global-install assumptions
- pinned or toolchain-governed versions when dependencies are introduced
- minimal baseline tooling; optional tools stay conditional until a repo proves the need

Examples: TypeScript uses Biome for the format/lint realization; Python uses Ruff; Go uses `gofmt`, `go vet`, and `go test` with optional pinned lint tools; Rust uses rustfmt/clippy; C++ uses clang-format/clang-tidy when configured.

## Per-repo overrides

Add repo-specific adjustments in one of:

- `.codex/tech-stack.local.md`
- `.claude/docs/tech-stack.local.md`
- `docs/tech-stack.local.md`

Treat the override as higher priority than the lane docs.

## Versioning

- Bump version: `uv version --bump patch` (or `minor`/`major`)
- Tag: `git tag X.Y.Z`

## Build / publish (uv)

- Build: `uv build`
- Publish (requires token/index creds): `uv publish`

## CLI

### Run from this repo (no install)

- List lanes: `uv tool run --from . tech-stack-core list`
- Print a lane (prefer `./lanes` when present): `uv tool run --from . tech-stack-core show py --prefer-repo`
- Print pi-extension TS lane: `uv tool run --from . tech-stack-core show pi-ts --prefer-repo`
- Print C++ lane: `uv tool run --from . tech-stack-core show cpp --prefer-repo`
- Print Rust lane: `uv tool run --from . tech-stack-core show rust --prefer-repo`
- Print Elixir lane: `uv tool run --from . tech-stack-core show elixir --prefer-repo`
- Get path (prefer `./lanes` when present): `uv tool run --from . tech-stack-core path py --prefer-repo`

If you’re iterating locally without bumping the version, add `-n` to avoid uv cache surprises:

- `uv tool -n run --from . tech-stack-core show py --prefer-repo`

### Install once, then run

- Install: `uv tool install --from . tech-stack-core`
- Then: `tech-stack-core list` (or `show py`, `path py`, etc.)

Note: `uv tool run tech-stack-core ...` only works if `tech-stack-core` is already installed (or published to a registry).
