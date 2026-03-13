# Next Session Prompt — tech-stack-core lane maintenance

Use this as the **first message** in the next session.

---
Continue in this repo: `/home/lightningralf/ai-society/core/tech-stack-core`.

## Objective
Maintain shared lane docs + CLI with low drift for downstream repos.

## Current state
- Shared lane docs live in `src/tech_stack_core/lanes/*`.
- CLI prints lane docs (`list`, `show`, `path`) via `src/tech_stack_core/cli.py`.
- TypeScript now has two lane variants:
  - `ts` (general Bun-first)
  - `pi-ts` (pi extension package repos; Node/npm baseline)
- Elixir now has an explicit lane:
  - `elixir` (OTP / Phoenix / Oban / Telemetry baseline)
- Canonical policy reference for validation tiers is external:
  - `~/ai-society/holdingco/governance-kernel/docs/dev/validation-tier-policy.md`

## Working agreement
- Canonical lane content lives in `src/tech_stack_core/lanes/`.
- `lanes/` symlink is convenience only (no second source of truth).
- Keep README + CLI + lane files aligned when lane IDs or lane guidance changes.

## Open next steps
1. Decide whether Python lane should include a concrete `typecheck` script example (`ty`) alongside `lint`/`format`.
2. Decide whether general `ts` lane should remain Bun-first or split further beyond `pi-ts`.
3. Cut a patch release + tag after lane changes that downstream repos should consume.
4. Run periodic consistency audit:
   - `rg -n "\\bmypy\\b" -S`
   - `rg -n "\\bty\\b" -S`

## Read first (high signal)
- `README.md`
- `src/tech_stack_core/cli.py`
- `src/tech_stack_core/lanes/tech-stack-py.md`
- `src/tech_stack_core/lanes/tech-stack-ts.md`
- `src/tech_stack_core/lanes/tech-stack-pi-ts.md`
- `src/tech_stack_core/lanes/tech-stack-elixir.md`

## Desired output format
- Decision-first summary
- Proposed lane/doc/CLI edits
- Validation commands run
- Release/tag recommendation
---
