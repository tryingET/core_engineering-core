---
summary: "AK projection and task-scope guidance for generated agent product repositories."
read_when:
type: "reference"
---

# Governance


## Workflow

```bash
```

Do not repair drift by hand-editing JSON and pretending it is authoritative.

## Explicit task-scope snapshots

```bash
mkdir -p governance/task-scopes
ak task scope export <TASK-ID> > governance/task-scopes/AK-<TASK-ID>.snapshot.json
./scripts/check-task-scope-snapshots.sh
```

Snapshots are frozen AK exports. They do not appoint the agent, grant delegation, or replace live task scope.

## Optional schema validation

```bash
```

Missing required AK access fails closed. Cross-repo coordination belongs in FCOS only when a genuine cross-owner gate exists.
