---
summary: "pi extension TypeScript engineering lane for ecosystem-specific tooling, commands, and implementation defaults."
read_when:
  - "Working in a repo or package whose selected engineering-core lane is pi-ts."
  - "Choosing pi extension TypeScript tooling, command surfaces, quality defaults, or ecosystem-specific validation."
type: "guide"
---

# TypeScript lane — pi extension packages (Node + npm)

Use this lane when building **pi extension packages** (slash-command extensions and prompt bundles),
not general web backends.

## Core toolchain and defaults

- **Runtime/package manager:** Node.js 22 LTS + npm
- **Language mode:** TypeScript with strict settings (ESM)
- **Package contract:** `package.json` with `pi.extensions` and optional `pi.prompts`
- **Validation baseline:** `npm run check` + deterministic release preflight (`npm run release:check`)
- **Release baseline:** release-please (`vX.Y.Z`) + npm trusted publishing (`npm publish --provenance`)

## Command baseline

- Install deps: `npm install`
- Validate structure/docs/policies: `npm run check`
- Typecheck (when the repo carries a TypeScript compile contract): `tsc --noEmit` from an exactly pinned `typescript@7` (the native compiler)
- Release preflight (full): `npm run release:check`
- Release preflight (artifact-only): `npm run release:check:quick`
- Local extension smoke (direct): `echo "/<command> --help" | pi -e ./extensions/<command>.ts -p`

## Applicable cross-language disciplines

Load disciplines when the concern applies:

- `validation` and `testing` for command tiers, quality gates, and test selection.
- `dependency-governance` and `security-privacy` for npm packages, extension risk, secrets, and supply chain.
- `documentation` for README/policy/prompt docs and shipped extension behavior.
- `service-api` when extensions expose/consume durable command, tool, file, network, or event contracts.
- `data-governance` when extensions read/write canonical data, generated projections, evidence artifacts, imports/exports, or caches that could become hidden authority.
- `domain-modeling` when extension commands encode workflow states, permissions, policies, or durable operator vocabulary.
- `design-patterns` when reviewing named patterns such as factory, adapter, actor, repository, saga, state machine, or policy object.
- `ai-ml` when extensions route LLM/model/tool behavior, prompts, evals, or safety/privacy claims.
- `performance` when startup, command latency, bundle/package size, or runtime cost matters.
- `release-package` for npm publishing, release-please, provenance, package contents, compatibility, and rollback.
- `observability` when extensions own runtime telemetry, logs, or external effects.

## Packaging baseline

- Keep `files` whitelist explicit in `package.json`
- Include `LICENSE`, `README.md`, extension entrypoint, prompt/policy assets as needed
- Ignore local tarballs (`*.tgz`) in `.gitignore`

## Testing guidance

- Default unit/integration runner: **Node.js built-in `node:test`** unless the package template or repo explicitly standardizes something heavier.
- Property/fuzz testing: **`fast-check`** when parser/rendering/selection invariants matter.
- Behavior/Gherkin testing: **`cucumber.js`** only when slash-command or operator workflows benefit from executable shared scenarios.
- Prefer the smallest runner that preserves determinism; do not add BDD layers when ordinary unit/regression tests already express the behavior clearly.

## Template / rendering guidance

- Default template engine for reusable text/config/prompt/file generation: **`nunjucks`** when the package genuinely benefits from file-backed templates.
- Prefer plain typed render functions or static assets when that is simpler and more explicit.
- Use templates for durable generation surfaces, not for trivial string interpolation.

## Typecheck policy

- For repos with a real TypeScript compile boundary, typecheck with `tsc --noEmit` from an exactly pinned `typescript@7`. TypeScript 7 ships the native (Go) compiler as `tsc`; the `tsgo` binary from `@typescript/native-preview` was its preview name, and that channel stopped publishing on 2026-07-07. Repos still using `tsgo` should replace `@typescript/native-preview` with `typescript@7` and switch their scripts to `tsc`.
- Don't keep a second compiler as a fallback; to recover from a compiler regression, roll back the `typescript` pin.
- TypeScript 7 only, no fallback. TypeScript 7 doesn't ship the classic compiler API (`import ts from "typescript"` exposes only `version`; its new API is under `typescript/unstable/*`). So:
  - **Dev tooling must run on TypeScript 7.** Don't adopt a tool that needs the classic API, and don't keep TypeScript 6 around for it; replace the tool. The TypeScript 7-compatible defaults: Biome for lint instead of typescript-eslint, and `tsc --declaration --emitDeclarationOnly` (with `rootDir` set explicitly, which TypeScript 7 requires) for `.d.ts` output instead of api-extractor or tsup's dts build. Common classic-API tools to replace: typescript-eslint, ts-morph, typedoc, api-extractor, ts-node, ts-jest.
  - **Runtime use of the compiler API is a product dependency, never under the name `typescript`.** When a package's own product calls the compiler API (for example an in-memory type gate), declare that library under its explicit package name (`@typescript/typescript6` today, `typescript/unstable/*` once stable), so `typescript` always means the TypeScript 7 typechecker. Record the dependency in `docs/engineering.local.md`.
  - Tools run from their own install, such as `ts-quality`, keep their own `typescript` and don't affect the repo's typecheck.
- Repos that intentionally ship without `tsconfig.json` should document that choice in `docs/engineering.local.md` instead of pretending to follow a compile-time lane they do not implement.

## Engineering lane contract surface

When adopting this lane in a repo/package, prefer an explicit contract surface:

- `policy/engineering-lane.json` pins the upstream lane and retrieval command
- `docs/engineering.local.md` records repo-local deltas
- validation scripts should at least verify the pinned lane metadata; optional smoke checks may also run the `engineering-core` CLI when available

## Policy notes

- Prefer minimal runtime deps unless required by extension behavior
- Keep command surfaces explicit and conflict-aware
- Keep repo docs and policy files in sync with shipped behavior
- For npm-based repos, a conservative global freshness gate such as `min-release-age=7` in `~/.npmrc` is reasonable.
- If a pi-extension repo intentionally switches to pnpm workspaces later, prefer a repo-local override rather than inventing a new lane immediately; use `minimumReleaseAge: 10080` at the workspace root.

## Quality-gate architecture

Use `disciplines/validation.md` for trust-boundary enforcement, versioned hooks, single-source quality gates, and evidence expectations. Pi write-time checks are fast feedback, not authority; when used, they should call the same repo quality gate in file-scoped mode.

## Conditionally loaded addenda

### Justfile addendum

Read the lane-specific Justfile addendum only when:
- `Justfile` is missing
- the standardized targets are absent or drifting
- you are explicitly establishing or reconciling the repo-local `Justfile`

Otherwise, do not load the addendum by default.

Companion doc:
- `engineering-pi-ts.justfile.md`

### ts-quality addendum

Read the lane-specific `ts-quality` addendum only when the package repo is explicitly adopting deterministic screening with `ts-quality`.

Companion doc:
- `engineering-pi-ts.ts-quality.md`
