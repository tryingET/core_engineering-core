---
summary: "Repo-local engineering-core override template."
read_when:
  - "Creating docs/engineering.local.md for a repo adopting engineering-core."
type: "template"
---

# engineering.local

Shared lane owner: `https://github.com/tryingET/core_engineering-core.git`.

This file records repo-local overrides and integration choices on top of engineering-core. It is the repo-local source for the selected subset; do not infer that every engineering-core lane, addendum, or discipline applies here.

## Released upstream retrieval

Read upstream guidance only when the relevant surface is in scope. For v0.9.0 adoption, use its immutable remote commit:

```bash
uv tool -n run --from 'git+https://github.com/tryingET/core_engineering-core.git@d74cdcc27a0fe2839707502655c77365ade5cc3a' engineering-core list
uv tool -n run --from 'git+https://github.com/tryingET/core_engineering-core.git@d74cdcc27a0fe2839707502655c77365ade5cc3a' engineering-core list-disciplines
uv tool -n run --from 'git+https://github.com/tryingET/core_engineering-core.git@d74cdcc27a0fe2839707502655c77365ade5cc3a' engineering-core show <lane> --prefer-repo
uv tool -n run --from 'git+https://github.com/tryingET/core_engineering-core.git@d74cdcc27a0fe2839707502655c77365ade5cc3a' engineering-core show-discipline <discipline> --prefer-repo
```

Record the matching remote repository, `v0.9.0` ref, resolved commit, and `git+https` source in `policy/engineering-lane.json` as an explicit `release_pin`.

## Local self-development only

When developing engineering-core itself from a local checkout, use the checkout honestly as `workspace-local-unpinned` rather than calling it a released pin:

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
- `specification-and-dsls` when conventions, schemas, generated files, policy files, or command vocabularies need explicit governance.
- `engineering-reasoning` when the repo needs to cite a reasoning mode or Prompt Vault-supported cognitive procedure without copying prompt bodies.

## Repo-local choices

- Package manager / toolchain: `<local truth>`.
- Standard operator surface: `<just/npm/uv/go/etc.>`.
- Validation before handoff: `<commands>`.
- Deliberate deviations from upstream defaults: `<why>`.

## Evidence expectations

Record the smallest truthful validation set for normal handoff and the stronger release/CI-equivalent set when different.

## Repo loop validation (optional)

If this repo participates in agent, slash-command, visible-loop, nexus-loop, or other prompt-driven implementation loops, map `repo-loop-validation-v1` phases to local commands or explicit fallbacks:

- `loop-doctor`: `<command or n/a: reason>`
- `loop-verify-fast`: `<command or n/a: reason>`
- `loop-impact-plan`: `<command or n/a: reason>`
- `loop-impact-run`: `<command or n/a: reason>`
- `loop-impact-wide`: `<command or n/a: reason>`
- `loop-landing-check`: `<command or n/a: reason>`

These commands produce evidence for handoff; they do not replace repo, AK, CI, release, or governance authority.
