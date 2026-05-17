---
summary: "How repositories adopt engineering-core lanes, addenda, disciplines, and repo-local overrides."
read_when:
  - "A repo is adding or refreshing docs/engineering.local.md."
  - "An agent needs to choose engineering-core lanes, addenda, or disciplines for a concrete repo."
type: "guide"
---

# engineering-core adoption

Use engineering-core as a versioned upstream source for shared engineering guidance, not as a compatibility shim for legacy names.

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

## Hard rename rule

The rename to `engineering-core` is intentionally breaking. Do not recreate old CLI aliases, package aliases, file names, or policy names. Consumers should update references directly.

## Version pinning

For local workspace adoption, record the source honestly as `workspace-local-unpinned`. For released adoption, pin to a git tag or package version and record the retrieval command in repo-local policy.
