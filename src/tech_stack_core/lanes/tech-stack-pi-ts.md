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
- Release preflight (full): `npm run release:check`
- Release preflight (artifact-only): `npm run release:check:quick`
- Local extension smoke (direct): `echo "/<command> --help" | pi -e ./extensions/<command>.ts -p`

## Packaging baseline

- Keep `files` whitelist explicit in `package.json`
- Include `LICENSE`, `README.md`, extension entrypoint, prompt/policy assets as needed
- Ignore local tarballs (`*.tgz`) in `.gitignore`

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
