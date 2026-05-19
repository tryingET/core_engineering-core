---
summary: "Vision for engineering-core as the shared engineering guidance and adoption-visibility substrate."
read_when:
  - "Aligning engineering-core roadmap, scanner ownership, or cross-company adoption strategy."
type: "reference"
---

# Vision

Engineering-core is the versioned engineering guidance substrate for AI Society: a small, inspectable core of language lanes, conditional addenda, cross-language disciplines, adoption templates, and CLI automation that every company/lane can consume without copying doctrine.

The target operator experience:

1. choose a repo, lane, company, or workspace scope;
2. ask engineering-core what guidance applies;
3. inspect local deviations in `docs/engineering.local.md` and `policy/engineering-lane.json`;
4. scan adoption coverage across `core`, `softwareco`, `holdingco`, `teachingco`, `healthco`, and future companies;
5. leave rollout dashboards and generated snapshots in the owning scope, not in engineering-core.

## North star

```text
shared engineering doctrine -> repo-local selection/deviation -> multi-scope adoption visibility -> owner-local rollout action
```

Engineering-core should make broad adoption visible without becoming the runtime authority for every repo. It owns reusable scanner semantics and catalog-aware validation. Scope owners own generated dashboards, follow-up tasks, local exceptions, and adoption waves.

## Design principles

- Keep shared guidance portable across languages, repo shapes, and companies.
- Keep repo/package-specific commands and deviations repo-local.
- Keep generated adoption snapshots in the scope being scanned.
- Treat semantic adoption flags as advisory review signals, not policy enforcement.
- Make scanner commands safe by default: read-only stdout unless explicit output paths are provided.
- Prefer warning/ratchet rollout before hard CI gates.

## Adoption horizon

The scanner should support at least these scopes without hardcoded company knowledge:

- `~/ai-society/core`
- `~/ai-society/softwareco/owned`
- `~/ai-society/softwareco/infra`
- `~/ai-society/holdingco`
- `~/ai-society/teachingco`
- `~/ai-society/healthco`
- future company or lane roots such as finance-oriented scopes when they appear

Success means an operator can see which repos/packages are adopted, partial, legacy, invalid, or missing, then route remediation to the owning repo/lane without confusing scanner visibility with runtime authority.
