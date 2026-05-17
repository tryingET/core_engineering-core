---
summary: "Checklist for adopting one engineering-core discipline in a repo."
read_when:
  - "A repo is adopting or refreshing a cross-language engineering-core discipline."
type: "template"
---

# Discipline Adoption Checklist

Discipline: `<discipline-id>`
Repo: `<repo/path>`
Date: `<YYYY-MM-DD>`

## Scope

- Concern that triggered adoption: `<why this discipline applies>`
- Paths/surfaces in scope: `<paths>`
- Paths/surfaces out of scope: `<paths>`

## Upstream read

```bash
engineering-core show-discipline <discipline-id>
```

Read also:

- selected language lane(s): `<lane ids>`
- conditional addenda: `<addenda ids>`
- related disciplines: `<discipline ids>`

## Repo-local decisions

- Local owner surface: `<docs/engineering.local.md section or policy file>`
- Local command(s): `<just/npm/uv/etc.>`
- Deliberate deviations: `<none or rationale>`
- Evidence required before handoff: `<commands/artifacts>`

## Acceptance

- [ ] Upstream discipline is cited in `docs/engineering.local.md` or equivalent.
- [ ] Repo-local deviations are explicit.
- [ ] Validation command exists or omission is justified.
- [ ] Generated/projection files have check/regeneration story when relevant.
- [ ] Handoff evidence names commands actually run.
