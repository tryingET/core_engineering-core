---
summary: "Current repository-local engineering-core self-adoption posture and authority boundary."
read_when:
  - "Before planning, advising, or validating engineering work in this repository."
type: "reference"
---

# Local engineering guidance

## Upstream

- Source: `core/engineering-core`
- Release pin: `v0.12.1` (`5be0f0a294014f2f7aee1ca5adcb6f3c76553e11`)
- Policy: `policy/engineering-lane.json`

## Selected guidance

- Lane: `py`
- Disciplines: `validation`, `testing`, `security-privacy`, `documentation`, `dependency-governance`

## Declared capabilities

- `planning`, `advisor`
- `closed_loop` is not declared.

These declarations authorize deterministic static observation only. They do not prove command execution, model use, CI compliance, release readiness, or verified runtime evidence. Repository and AK owner surfaces retain those facts.

## Validation posture

Use the repository's existing owner-declared validation commands. This adoption adds no hard CI gate and executes no consumer-declared command.
