---
summary: "How repositories adopt engineering-core lanes, addenda, disciplines, and repo-local overrides."
read_when:
  - "A repo is adding or refreshing docs/engineering.local.md."
  - "An agent needs to choose engineering-core lanes, addenda, or disciplines for a concrete repo."
type: "guide"
---

# engineering-core adoption

Use engineering-core as a versioned upstream source for shared engineering guidance, not as a compatibility shim for legacy names.

Related governance docs:

- `docs/authority-map.md` — where shared guidance, repo-local deviations, templates, validation policy, and runtime truth belong.
- `docs/discipline-lifecycle.md` — when to add, split, merge, or relocate discipline guidance.

## Adoption surface

A repo that adopts engineering-core should carry:

1. `policy/engineering-lane.json` when a machine-readable lane declaration is useful.
2. `docs/engineering.local.md` for human-readable local overrides.
3. A local validation command surface (`just`, package scripts, or equivalent) that records what must pass before handoff.

## Read order

1. Repo-local `docs/engineering.local.md`.
2. Declared lane(s), for example `engineering-core show ts --prefer-repo` from this repo.
3. Conditional addenda only when relevant, for example `ts-frontend` for browser UI work.
4. Cross-language disciplines only when they own the current concern.

## Selection rule

Choose the smallest truthful upstream set:

- one or more language lanes for implementation ecosystems;
- conditional lane addenda for narrower surfaces;
- cross-language disciplines for invariants such as validation, testing, accessibility, documentation, or security/privacy.

Do not load every lane or every discipline by default.

## Ownership rule

Adoption should preserve the authority map:

- engineering-core owns shared lanes and disciplines;
- repo docs own local deviations and selected subsets;
- governance-kernel owns canonical validation policy;
- templates own generated defaults;
- Agent Kernel owns runtime task/evidence/decision truth.

Do not move repo-specific commands into shared disciplines, and do not fork shared doctrine into generated templates.

## Hard rename rule

The rename to `engineering-core` is intentionally breaking. Do not recreate old CLI aliases, package aliases, file names, or policy names. Consumers should update references directly.

## Adoption scanning

Use `engineering-core scan-adoption` for reusable adoption mechanics across repo, lane, company, or workspace scopes, including `~/ai-society/core` itself. The scanner reports structural adoption, legacy surfaces, invalid policy JSON, catalog/list command presence, selected lanes/disciplines, and heuristic semantic discipline flags.

Examples:

```bash
engineering-core scan-adoption --scope /path/to/lane-root --include-packages --format json
engineering-core scan-adoption --scope ~/ai-society/core --repo-discovery recursive --include-scope-root --include-packages
engineering-core scan-adoption --scope ~/ai-society/core --scope ~/ai-society/softwareco/infra --repo-discovery recursive --include-scope-root --include-packages --format json
```

Keep generated rollout state in the scope owner, not in engineering-core. For example, a lane root may write `governance/engineering-core-adoption-scan.json` and `docs/project/engineering-core-adoption-dashboard.md`, but engineering-core owns the scanner semantics and generic report shape. Start with warning/ratchet use before hard CI gates so scope owners can distinguish true adoption debt from intentional local posture.

## Version pinning

For local workspace adoption, record the source honestly as `workspace-local-unpinned`. For released adoption, pin to a git tag or package version and record the retrieval command in repo-local policy.
