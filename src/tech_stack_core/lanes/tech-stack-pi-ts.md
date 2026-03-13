# TypeScript lane — pi extension packages (Node + npm)

Use this lane when building **pi extension packages** (slash-command extensions and prompt bundles),
not general web backends.

## Core stack

- **Runtime/package manager:** Node.js 22 LTS + npm
- **Language mode:** TypeScript with strict settings (ESM)
- **Package contract:** `package.json` with `pi.extensions` and optional `pi.prompts`
- **Validation baseline:** `npm run check` + deterministic release preflight (`npm run release:check`)
- **Release baseline:** release-please (`vX.Y.Z`) + npm trusted publishing (`npm publish --provenance`)

## Command baseline

- Install deps: `npm install`
- Validate structure/docs/policies: `npm run check`
- Typecheck (when the repo carries a TypeScript compile contract): prefer `tsgo --noEmit`; keep `tsc --noEmit` available as fallback when `tsgo` is not yet viable
- Release preflight (full): `npm run release:check`
- Release preflight (artifact-only): `npm run release:check:quick`
- Local extension smoke (direct): `echo "/<command> --help" | pi -e ./extensions/<command>.ts -p`

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

- For repos with a real TypeScript compile boundary, prefer `tsgo --noEmit` as the primary typecheck command.
- Keep `tsc --noEmit` as a compatibility fallback during rollout or incident recovery.
- Repos that intentionally ship without `tsconfig.json` should document that choice in `docs/tech-stack.local.md` instead of pretending to follow a compile-time lane they do not implement.

## Stack contract surface

When adopting this lane in a repo/package, prefer an explicit contract surface:

- `policy/stack-lane.json` pins the upstream lane and retrieval command
- `docs/tech-stack.local.md` records repo-local deltas
- validation scripts should at least verify the pinned lane metadata; optional smoke checks may also run the `tech-stack-core` CLI when available

## Policy notes

- Prefer minimal runtime deps unless required by extension behavior
- Keep command surfaces explicit and conflict-aware
- Keep repo docs and policy files in sync with shipped behavior

## Quality-gate architecture (first principles)

- **Hard enforcement at trust boundaries:** enforce checks in **git hooks + CI** (commit/push/PR), not editor-specific wiring.
- **Version hooks in-repo:** prefer `.githooks/` + `git config core.hooksPath .githooks` over unmanaged `.git/hooks/*` scripts.
- **Single source of truth:** keep checks in one script (for example `scripts/quality-gate.sh`) and call it from hooks/CI/tooling.
- **Pi is fast feedback, not authority:** Pi write-time checks should call the same quality gate in file-scoped mode.

### Multi-order effects to optimize for

- If checks only run in Pi, non-Pi edits bypass policy.
- If checks only live in local `.git/hooks`, each clone drifts.
- If write-time and commit-time logic diverge, developers get false confidence.
- If write-time checks are too heavy, teams disable them and lose feedback.
