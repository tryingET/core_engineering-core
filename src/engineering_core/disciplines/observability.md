# Discipline — Observability

## Purpose

Make runtime behavior inspectable without leaking secrets or pretending local logs equal production truth.

## Signals

- **Logs** — discrete events with level, context, and error details.
- **Metrics** — counts, gauges, histograms, SLO indicators.
- **Traces** — causality across calls, jobs, devices, workers, and user flows.
- **Profiles** — CPU, memory, allocations, frame time, GPU/IO where relevant.
- **Health/readiness** — dependency and startup state for humans and automation.
- **Evidence artifacts** — command outputs, reports, receipts, screenshots, benchmark data.

## Invariants

- Every long-running service has health/readiness posture.
- Critical errors carry enough context to act.
- Telemetry never leaks secrets, tokens, raw PII, or sensitive payloads by default.
- Local observability is useful without requiring a cloud account.
- Production/field claims use runtime evidence, not only local tests.

## Decision rules

- Use structured logs when machines must query them.
- Use metrics when trend/threshold matters.
- Use traces when causality crosses process/module/network/device boundaries.
- Use profiles when performance work is the task.
- Add correlation/request/session IDs before debugging distributed behavior.

## Failure modes

- logs as string soup
- metrics without units or cardinality control
- traces that record sensitive payloads
- health endpoint always returns OK
- benchmarks without hardware/runtime context
- observability introduced only after incident
