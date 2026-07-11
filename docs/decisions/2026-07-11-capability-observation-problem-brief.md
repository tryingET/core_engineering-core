---
summary: "Problem brief for reusable doctor and factual capability observation."
read_when:
  - "Reviewing why v0.5 capability adoption cannot yet be measured truthfully."
type: "problem-brief"
---

# Problem brief — Capability observation

Engineering-core v0.5 can compile plans, construct bounded advice requests, validate advice, and process owner evidence records, but it has no doctor and no contract for observing those capabilities across repositories. Existing `scan-adoption` measures docs/policy/lane structure only. Ad-hoc filesystem scripts are not reusable product contracts and cannot distinguish owner declaration from static compatibility or verified execution.

A six-scope filesystem orientation found 44 structurally adopted repositories among 84 explicit git paths, but no inspected local engineering policy/doc referenced v0.5 capability schemas. That result is orientation, not canonical society closure: the repository population was filesystem-derived, and the scanner cannot represent the new maturity dimensions.

The required change is an additive, read-only packaged CLI contract that consumes explicit owner-provided repository paths, validates optional capability declarations, reports static observability without executing commands, and leaves evidence/rollout authority with repo owners and AK where accepted.
