---
summary: "TypeScript lane ts-quality adoption addendum."
read_when:
  - "A TypeScript repo is adopting deterministic screening with ts-quality."
  - "Reconciling TypeScript quality gates with lane guidance and validation expectations."
type: "guide"
---

# TypeScript lane — ts-quality addendum

Read this addendum only when a general TypeScript repo is adopting deterministic screening with `ts-quality`.

Use it with the main TS lane and `disciplines/validation.md`, not instead of them.

## When to load this addendum

Load this addendum when:
- the repo wants explicit evidence-based screening for high-risk TypeScript changes
- the repo is deciding how to introduce `ts-quality` without widening to the whole codebase at once
- the repo needs a repo-local rollout truth file and a central catalog registration path

Do not load this addendum by default for every TS repo.
If the repo is not adopting `ts-quality`, the main lane is sufficient.

## Recommended starting point

Choose the guide that matches the repo state:
- brownfield rollout: `~/ai-society/softwareco/owned/ts-quality/docs/adoption/agent-integration-how-to.md`
- greenfield bootstrap: `~/ai-society/softwareco/owned/ts-quality/docs/adoption/greenfield-bootstrap-how-to.md`

## Recommended repo-local contract

When a repo adopts `ts-quality`, prefer:
- repo-local rollout truth: `docs/dev/ts-quality-current-vs-target.md`
- repo-local control plane: `ts-quality.config.json`, `.ts-quality/**`, and repo-local wrapper scripts when needed
- screening centered on behavior-bearing implementation files rather than facade barrels

If tests execute built output such as `dist/**`, keep screening on `src/**` and use real source-map line remapping back onto authored source.

## Central catalog registration

After the first live slice is real, register the repo in the central overview:

```bash
cd ~/ai-society/softwareco/owned/ts-quality
node scripts/register-screening-catalog.mjs --entry docs/adoption/entries/<repo>.json
node scripts/register-screening-catalog.mjs --check
```

Use the template:
- `~/ai-society/softwareco/owned/ts-quality/docs/adoption/repo-screening-entry.template.json`

## Anti-patterns

Avoid these when adopting `ts-quality` in a TS repo:
- screening facade barrels when the real logic lives in implementation files
- widening to the whole repo before one slice is trustworthy
- path-only coverage rewrites when the repo depends on dist-backed runtime tests
- copying the full upstream integration doctrine into each repo instead of linking to it
