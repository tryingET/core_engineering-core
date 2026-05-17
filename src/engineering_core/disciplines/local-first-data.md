---
summary: "Cross-language local-first data discipline for persistence, migrations, sync, corruption, and authority."
read_when:
  - "Work changes local state, browser storage, filesystem persistence, embedded databases, migrations, export/reset, or sync."
  - "Reviewing privacy, corruption, or authority boundaries for locally stored user data."
type: "guide"
---

# Discipline — Local-First Data

## Purpose

Define how repos handle local state, persistence, migrations, sync, corruption, privacy, and authority.

## Invariants

1. State authority is explicit.
2. Local operation does not require network unless declared.
3. Projections are not authority unless explicitly declared.
4. Durable data has migration and export/backup posture.
5. Corruption behavior is explicit: recover, quarantine, rebuild, or fail closed.
6. Sync conflicts are designed before sync exists.
7. User data is minimized and classified.

## Authority classes

| Class | Examples | Rule |
|---|---|---|
| canonical local DB | SQLite, IndexedDB, DuckDB, local Postgres | DB wins; migrations required |
| human config | TOML/YAML/env/preferences | precedence documented |
| generated projection | JSON, markdown, reports | regenerate from authority |
| cache | API/model/build cache | disposable; never hidden authority |
| evidence/audit | receipts, logs, JSONL | append/additive preferred |

## Storage decision rules

- Use memory for ephemeral UI/session state.
- Use localStorage only for tiny, simple browser values with low migration burden.
- Use IndexedDB, OPFS, SQLite, DuckDB, or platform DB when data is structured, queryable, durable, or large.
- Use plain files when data is human-edited, versioned, and not concurrently written.
- Use generated projections when humans need reviewable output from a canonical source.
- Add remote storage/sync only after identity, conflict, privacy, backup, and offline semantics are explicit.

## Required declarations for durable data

- canonical state path or store
- schema/version source
- migration command/path
- export/backup path
- delete/reset behavior
- corruption behavior
- sync/import/export behavior
- retention/privacy posture

## Failure modes

- cache becomes authority
- local-first claim while startup requires network
- destructive migration without export path
- sync added with no conflict semantics
- generated markdown/JSON treated as runtime truth
- absolute local paths leak into shared artifacts
