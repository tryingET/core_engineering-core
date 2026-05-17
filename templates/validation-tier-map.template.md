---
summary: "Template mapping repo commands to engineering-core validation tiers."
read_when:
  - "Defining or refreshing a repo validation command surface."
type: "template"
---

# Validation Tier Map

Repo: `<repo/path>`
Owner surface: `docs/engineering.local.md`

## Commands

| Tier | Command | Scope | Target runtime | Required before |
|---|---|---|---|---|
| editor/save | `<command or n/a>` | file-local | instant | local editing |
| pre-commit | `<command or n/a>` | staged slice | p95 < 10s | commit |
| task-scope | `<command>` | changed behavior | minutes | task handoff |
| pre-push | `<command>` | repo full gate | acceptable local | push/merge |
| CI | `<command or CI job>` | authoritative matrix | complete | merge/release |
| release | `<command>` | shipped artifact | strongest | tag/publish |

## Standard surface

- `just check`: `<maps to>`
- `just test`: `<maps to>`
- `just build`: `<maps to>`
- `just ci`: `<maps to>`
- `just doctor`: `<maps to>`

## Evidence rule

Every handoff records:

- command
- scope
- result
- warning acceptance, if any
- artifact path, if any
