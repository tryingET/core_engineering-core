---
summary: "Template for comparable TypeScript quality-tool pilot evidence and promotion decisions."
read_when:
  - "Planning or reviewing an Ultracite, Oxlint, Biome, or evidence-safety pilot."
type: "template"
---

# TypeScript Quality Pilot

## Identity

- Repository/package:
- Cohort: greenfield | brownfield
- Owner:
- Reviewers:
- Date:
- Hypothesis:
- Candidate realization/rule subset:
- Upstream refs and exact versions:

## Baseline

- Current package manager/runtime:
- Current formatter/linter/typechecker:
- Exact commands and file scope:
- Generated/vendor/build-output ignores:
- Cold runtime:
- Warm runtime:
- Existing diagnostic counts by rule/severity:
- Existing suppressions/exceptions:

## Candidate result

- Installation/configuration diff:
- Dependencies added/removed:
- Lockfile impact:
- Cold runtime:
- Warm runtime:
- Auto-fix diff size:
- Remaining diagnostics by rule/severity:
- True defects found:
- False positives or ambiguous findings:
- Required suppressions/deviations:
- Editor behavior:
- Agent behavior:
- CI/non-interactive behavior:
- Doctor/configuration diagnosis:
- Reviewer and migration effort:

## Evidence quality

- Same file scope and cache state used: yes | no
- Repeated runs recorded: yes | no
- Tests and typecheck passed after changes: yes | no
- Unrelated changes excluded: yes | no
- Raw outputs/benchmarks stored at:

## Decision

- Outcome: promote | optional | narrow | reject | continue pilot
- Rationale:
- Accepted tradeoffs:
- Required follow-up:
- Rollback command/steps:
- Decision owner:
- Review after:

## Promotion checklist

- [ ] Greenfield and brownfield evidence exists.
- [ ] Diagnostics were reviewed by rule, not only counted.
- [ ] False positives and deviations are documented.
- [ ] Runtime comparisons use equivalent inputs.
- [ ] Dependency and supply-chain impact is reviewed.
- [ ] CI and rollback are deterministic.
- [ ] The proposed scope is explicit: repo-local, optional profile, or stable lane default.
