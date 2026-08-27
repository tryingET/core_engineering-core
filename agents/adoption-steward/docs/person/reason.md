---
summary: "Why this agent exists (reason)."
read_when:
  - "When the agent drifts or becomes unfocused"
---

# Reason

- Why do we have this agent? In the weeks before its instantiation, humans and controllers performed engineering-core adoption stewardship ad hoc: refreshing the owned scan, reading the dashboard, running `doctor` on stragglers, reviewing deviations, and hand-routing content feedback. That work is recurring, evidence-shaped, and bounded — exactly what a standing agent should hold.
- What recurring pain does it remove? Adoption drift between manual sweeps; stale `review_after` dates in deviations ledgers; unpinned or stale engineering-core refs; unnoticed legacy surfaces; learnings about EC content that never reach the EC owner. The v1 reframe (ADR 2026-08-27) made adoption scans and agent learnings engineering-core's production telemetry — this agent is that telemetry's standing operator.
