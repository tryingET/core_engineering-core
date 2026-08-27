---
summary: "D-0001: instantiate agent-adoption-steward as the first softwareco standing agent with a null skill profile."
read_when:
  - "Changing the agent manifest, toolset, or skill selection"
type: "adr"
status: "accepted"
---

# D-0001: standing-agent instantiation and manifest choices

Date: 2026-08-27 · Status: accepted (AK 5100)

## Context / problem

AK 5100 asked for the first softwareco standing agent from the healthco L2
agent template family, declared through the new agent manifest convention v1.
The convention's example manifest used `skills.profile: "ec-py"`.

## Decision

- Instantiate from `softwareco/copier/tpl-agent-repo` (same template family
  as the healthco agent repos) at `owned/agents/agent-adoption-steward`.
- `agent.json` per convention v1 with `skills.profile: null` and
  `skills.extra: ["softwareco-owned-repo-router", "ai-society-runtime-recipes"]`:
  this role stewards adoption posture rather than executing an EC language
  lane, so an EC code-skill profile would misdescribe its work.
- `tools: ["read", "bash"]`, `thinking: "medium"`: advisory, read-only
  posture; all mutation stays with owners.
- Territory `softwareco/owned/*`; the engineering-core checkout is
  reference-only.

## Alternatives

- `ec-py` profile — rejected: imports implementation skills this advisory
  role does not use.
- Broader toolset (edit/write) — rejected: the steward proposes, owners
  dispose.

## Consequences

- The agent cannot self-apply adoption changes even if prompted; every
  proposal must name owner-executed commands.
- Skills stay runtime-resolved by name; profile members can be added later
  via engineering-core `~/ai-society/core/engineering-core/skills/profiles.json` if the role grows.

## Validation / rollout

- Manifest validates against convention v1; registry resolution is
  fail-closed on unknown skill names or a missing system-prompt file.
- Proof-of-use: first instantiation recorded through AK evidence on task
  5100.
