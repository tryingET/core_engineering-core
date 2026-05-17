---
summary: "Repo-local engineering-core override template."
read_when:
  - "Creating docs/engineering.local.md for a repo adopting engineering-core."
type: "template"
---

# engineering.local

Shared lane owner: `/home/tryinget/ai-society/core/engineering-core`.

This file records repo-local overrides and integration choices on top of engineering-core. It is the repo-local source for the selected subset; do not infer that every engineering-core lane, addendum, or discipline applies here.

## Upstream retrieval

Read upstream guidance from engineering-core only when the relevant surface is in scope:

```bash
cd /home/tryinget/ai-society/core/engineering-core
uv tool -n run --from . engineering-core list
uv tool -n run --from . engineering-core list-disciplines
uv tool -n run --from . engineering-core show <lane> --prefer-repo
uv tool -n run --from . engineering-core show-discipline <discipline> --prefer-repo
```

## Selected upstream set

Selected lanes:

- `<lane>` for `<path or surface>`.

Selected conditional addenda:

- `<addendum>` for `<narrow concern>`, if applicable.

Selected disciplines:

- `<discipline>` for `<cross-language invariant>`.

## Repo-local choices

- Package manager / toolchain: `<local truth>`.
- Standard operator surface: `<just/npm/uv/go/etc.>`.
- Validation before handoff: `<commands>`.
- Deliberate deviations from upstream defaults: `<why>`.

## Evidence expectations

Record the smallest truthful validation set for normal handoff and the stronger release/CI-equivalent set when different.
