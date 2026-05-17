---
summary: "pi extension TypeScript lane ts-quality adoption addendum."
read_when:
  - "A TypeScript repo is adopting deterministic screening with ts-quality."
  - "Reconciling TypeScript quality gates with lane guidance and validation expectations."
type: "guide"
---

# TypeScript lane for pi extension packages — ts-quality addendum

Read this addendum only when a pi extension package repo is adopting deterministic screening with `ts-quality`.

Use it with the main pi-ts lane and `disciplines/validation.md`, not instead of them.

## When to load this addendum

Load this addendum when:
- the package repo wants explicit evidence-based screening for high-risk TypeScript changes
- the package repo is deciding how to introduce `ts-quality` without widening to the whole package at once
- the package repo needs a repo-local rollout truth file and a central catalog registration path

Do not load this addendum by default for every pi extension package repo.
If the repo is not adopting `ts-quality`, the main lane is sufficient.

## Recommended starting point

Choose the guide that matches the repo state:
- brownfield rollout: `~/ai-society/softwareco/owned/ts-quality/docs/adoption/agent-integration-how-to.md`
- greenfield bootstrap: `~/ai-society/softwareco/owned/ts-quality/docs/adoption/greenfield-bootstrap-how-to.md`

## Recommended repo-local contract

When a pi extension package repo adopts `ts-quality`, prefer:
- repo-local rollout truth in the generated package docs surface, typically `docs/project/ts-quality-current-vs-target.md`
- repo-local control plane only after the package commits to a first real slice
- screening centered on behavior-bearing implementation files rather than public extension entrypoints or facade barrels

If package tests execute built output such as `dist/**`, keep screening on `src/**` and use real source-map line remapping back onto authored source.

## Central catalog registration

After the first live slice is real, register the repo in the central overview:

```bash
cd ~/ai-society/softwareco/owned/ts-quality
node scripts/register-screening-catalog.mjs --entry docs/adoption/entries/<repo>.json
node scripts/register-screening-catalog.mjs --check
```

Use the template:
- `~/ai-society/softwareco/owned/ts-quality/docs/adoption/repo-screening-entry.template.json`

## Template propagation note

If this lane is being propagated through template repos, keep the doctrine upstream in `ts-quality` and let templates consume it lightly.
Do not duplicate the full adoption guide into every template family.
