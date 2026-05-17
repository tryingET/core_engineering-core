---
summary: "Template for classifying repo data, storage authority, and local-first posture."
read_when:
  - "A repo stores user data, local state, generated projections, cache, or durable DB/files."
type: "template"
---

# Data Classification

Repo: `<repo/path>`
Date: `<YYYY-MM-DD>`

## Data inventory

| Data | Class | Storage | Authority | Retention | Export/delete | Notes |
|---|---|---|---|---|---|---|
| `<name>` | public/internal/user/sensitive/secret | `<path/db/service>` | canonical/projection/cache/config/evidence | `<duration>` | `<path/command>` | `<notes>` |

## Durable data requirements

- Schema/version source: `<path>`
- Migration command/path: `<command/path>`
- Backup/export command: `<command>`
- Reset/delete behavior: `<command/UX>`
- Corruption behavior: `<recover/quarantine/rebuild/fail closed>`
- Sync/import/export behavior: `<none or policy>`

## Local-first claim

- Works offline: `<yes/no/partial>`
- Network required at startup: `<yes/no and why>`
- Remote sync present: `<yes/no>`
- Conflict semantics if synced: `<policy>`

## Privacy notes

- User consent required: `<yes/no>`
- Telemetry redaction required: `<yes/no>`
- Sensitive local paths/secrets excluded from artifacts: `<yes/no>`
