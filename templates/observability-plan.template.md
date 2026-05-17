---
summary: "Template for repo observability signals, health checks, SLO seeds, and runtime evidence."
read_when:
  - "A repo adds services, workers, runtime telemetry, benchmarks, or health/readiness surfaces."
type: "template"
---

# Observability Plan

Repo: `<repo/path>`
Runtime surface: `<service/CLI/worker/frontend/native tool>`

## Signals

| Signal | Implementation | Purpose | Sensitive data risk | Validation |
|---|---|---|---|---|
| logs | `<library/path>` | `<why>` | `<risk/redaction>` | `<command/check>` |
| metrics | `<library/exporter>` | `<why>` | `<risk>` | `<command/check>` |
| traces | `<library/exporter>` | `<why>` | `<risk>` | `<command/check>` |
| profiles/benchmarks | `<tool>` | `<why>` | `<risk>` | `<command/check>` |
| health/readiness | `<endpoint/command>` | `<why>` | `<risk>` | `<command/check>` |

## Runtime evidence

- Local smoke command: `<command>`
- CI/runtime check: `<command/job>`
- Artifact paths: `<paths>`
- Accepted warnings: `<none or rationale>`

## SLO seeds, if accepted

- Availability: `<target>`
- Latency: `<target and path>`
- Error budget action: `<policy>`
- Queue/backlog health: `<policy>`

## Redaction and privacy

- Secrets redacted: `<yes/no>`
- User data redacted/minimized: `<yes/no>`
- Telemetry opt-in/retention: `<policy>`
