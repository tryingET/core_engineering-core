# AGENTS.md — agent-adoption-steward

## Intent
Standing-agent repository for **agent-adoption-steward**, the advisory cross-company engineering-core adoption steward (all EC consumers). Repository ownership governs its persona, prompts, manifest, and releases; it does not appoint the agent to an organizational role or grant company authority.

The agent's executable identity is `agent.json` (manifest convention v1) plus `docs/person/system-prompt.md`; keep the rest of this repo consistent with them.

## Guardrails
- No secrets in git (use CI variables + local secret-manager references).
- Main-first workflow: commit directly to `main` for normal work. Use a review branch/PR only for releases, when the operator explicitly requests a gate, or when a repo-local accepted policy documents a narrower exception.
- Treat `docs/_core/**` as immutable (vendored snapshot from `governance-kernel`; no submodules).
- Author explicit task scope in AK and treat `governance/task-scopes/AK-*.snapshot.json` as frozen exports, not hand-authored authority.

## Delegation, WIP, outcome, and effect gates
- This repository does not appoint organizational roles or grant company delegation. Discover delegation through accepted AK/governance state; if it is missing, expired, or ambiguous, stop and escalate.
- Admit active work only through a scoped owner-native task and finite-WIP decision. Starting work must name what is displaced, deferred, or stopped when capacity is full.
- Passing validation is not an outcome, release, external-effect authorization, or lifecycle decision.
- External effects and terminal `continue`, `stop`, `redirect`, or `complete` decisions require explicit human or accountable-owner authority.
- A CTO/technical-steward packet is a freshness-bounded projection from owner-native state, never a shadow backlog or authority surface.

## AK-native route guardrails
- Read the relevant AK task, direction, decision, and delegation state before inventing work.
- Generic input such as `proceed` continues an active execution task; it does not authorize lifecycle closeout, source-owner mutation, publication, or knowledge promotion.
- Treat closeout/readiness rows as gate inputs, not lifecycle authorization.
- Handoff instead of editing by convenience when facts belong to Prompt Vault, ROCS, Pi/runtime, KES, steward/publication, template propagation, Oracle/DSPx, or another owner.
- Do not revive SG/TG/OP markdown planning where AK-native direction is declared.

## Agent Kernel projection flow

```bash
ak task scope export <TASK-ID> > governance/task-scopes/AK-<TASK-ID>.snapshot.json
./scripts/check-task-scope-snapshots.sh
```

Use `AK_CMD="${AK_CMD:-ak}"` only to select an explicit compatible executable. Never substitute another state store when AK is required.

## Deterministic tooling policy (ROCS-first)
- Prefer `./scripts/rocs.sh <args...>` before ad-hoc scripting.
- Use inline Python only when no deterministic repo command exists.

## Stack contract
- If this agent ships language-specific software, declare its accepted engineering-core lane in `policy/engineering-lane.json` and local deltas in `docs/engineering.local.md`.
- If no language lane is selected, consult engineering-core through its catalog/list commands without pretending that a repo-local lane contract exists.

## Reusable procedures
Reusable cognitive and operating procedures belong to Prompt Vault governance. Discover them through the Prompt Vault query/retrieve surfaces, check dispatch posture before execution, and keep runtime decisions/evidence in AK rather than copying procedure bodies into this repository.

## Knowledge Crystallization Flow

```text
Session → diary/ (raw) → docs/learnings/ (crystallized) → TIPs (propagated)
```

1. During a session, capture raw facts in `diary/<date>--type-scope-summary.md`.
2. Extract durable patterns into `docs/learnings/`.
3. Route generalized reusable procedures to Prompt Vault and semantic changes to their ontology owner.
4. Keep owner-local product learnings in this repository.

## Recursion policy (explicit)
Allowed:
- L1 -> L2

Forbidden:
- L1 -> L0
- L2 -> L1
- any cycle

## Read order
1. `docs/_core/README.md`
2. `docs/person/`
3. `governance/README.md`
4. `docs/decisions/`
5. `docs/learnings/`
6. `diary/`
7. `docs/system4d/`
