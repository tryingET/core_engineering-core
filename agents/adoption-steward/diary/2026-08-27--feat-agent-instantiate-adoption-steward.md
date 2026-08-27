# 2026-08-27 — Instantiate agent-adoption-steward (AK 5100)

## What I Did

- Bootstrapped `owned/agents/agent-adoption-steward` from
  `softwareco/copier/tpl-agent-repo` via `new-repo-from-copier.sh`.
- Authored manifest `agent.json` (convention v1, null skill profile),
  persona `<repo>/docs/person/system-prompt.md`, person docs, four activity
  prompts (adoption-audit, migration-proposal, deviation-review,
  ec-feedback), do-not-touch policy, README, and D-0001.
- Adopted engineering-core disciplines for this repo itself via
  `engineering-core init` (validation, security-privacy, documentation; no
  language lane).

## What Surprised Me

- The softwareco template ships richer AGENTS guardrails (delegation,
  WIP, outcome/effect gates) than its healthco sibling — strong
  inheritance for a fleet agent.
- The EC v1 reframe ADR is dated the same day (2026-08-27) and names the
  agent fleet as engineering-core's delivery surface; this repo became its
  first concrete member within hours.

## Patterns

- Advisory agents: the manifest toolset (`read` + `bash`) is the authority
  boundary; docs only restate it.
- Adoption stewardship decomposes cleanly into four recurring prompts:
  audit / proposal / deviation review / feedback — the ad hoc human loop,
  templated.

## Crystallization Candidates

- → `docs/learnings/`: "advisory-agent least-privilege manifest pattern"
  once a second fleet agent exists to diff against.
- → EC feedback: none yet from this instantiation.
