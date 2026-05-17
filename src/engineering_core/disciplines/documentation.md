---
summary: "Cross-language documentation discipline for authority, front matter, generated projections, and update hygiene."
read_when:
  - "Creating or changing docs, generated documentation projections, read-first surfaces, or docs validation rules."
  - "Deciding whether documentation is authoritative, narrative, generated, or local override material."
type: "guide"
---

# Discipline — Documentation

## Purpose

Keep docs useful, scoped, and honest about authority. Documentation is part of the runtime interface for agents and operators; stale or over-authoritative docs create system bugs.

## Authority classes

| Doc kind | Role | Authority rule |
|---|---|---|
| README | entrypoint and command map | descriptive; must match commands |
| AGENTS.md | agent/operator contract | normative within repo scope |
| engineering.local.md | repo engineering deviations | local override over core lanes/disciplines |
| architecture docs | design explanation | explains accepted structure |
| decision docs | rationale/audit | human-readable unless decision system owns runtime state |
| generated docs/projections | reviewable output | regenerate from source authority |
| diary/session notes | raw capture | not canonical until promoted |

## Front matter

Markdown intended for agent discovery should include:

```yaml
---
summary: "One sentence describing the document."
read_when:
  - "Specific condition that should trigger reading it."
---
```

## Invariants

- Docs state what owns truth when authority matters.
- Commands in docs are runnable or explicitly illustrative.
- Generated docs say how to regenerate/check them.
- Repo-local docs do not silently override source-owner surfaces.
- Decision/process docs distinguish proposal, accepted decision, projection, and archive.

## Decision rules

- Put volatile implementation commands near the repo that owns them.
- Put cross-repo conventions in core/template/governance owners.
- Prefer links to canonical owner docs over copying long rules.
- Update docs in the same change that changes behavior.

## Failure modes

- README says one install path while CI uses another
- generated JSON/markdown hand-edited as truth
- parent AGENTS files duplicate repo-specific detail
- docs omit read triggers and become undiscoverable
- obsolete planning docs revived as authority
