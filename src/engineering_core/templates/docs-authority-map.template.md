---
summary: "Template for mapping repo documentation to authority classes and regeneration paths."
read_when:
  - "A repo is clarifying README, AGENTS, engineering.local, generated docs, decisions, or projections."
type: "template"
---

# Docs Authority Map

Repo: `<repo/path>`

## Authority table

| Path | Doc kind | Authority class | Owner | Regenerate/check | Notes |
|---|---|---|---|---|---|
| `README.md` | entrypoint | descriptive, must match commands | repo | `<check>` | `<notes>` |
| `AGENTS.md` | agent contract | normative in repo scope | repo | `<check>` | `<notes>` |
| `docs/engineering.local.md` | stack override | repo-local override | repo | `<check>` | `<notes>` |
| `<path>` | generated projection | projection | `<source owner>` | `<command>` | `<notes>` |
| `<path>` | decision/ADR | rationale/audit | `<decision owner>` | `<check>` | `<notes>` |

## Generated/projection docs

- Source authority: `<DB/tool/source>`
- Regeneration command: `<command>`
- Drift check command: `<command>`
- Manual edits allowed: `<yes/no>`

## Front matter coverage

Docs intended for agent discovery should include:

```yaml
---
summary: "..."
read_when:
  - "..."
---
```

Validation command:

```bash
node /home/tryinget/ai-society/core/agent-scripts/scripts/docs-list.mjs --docs . --strict
```
