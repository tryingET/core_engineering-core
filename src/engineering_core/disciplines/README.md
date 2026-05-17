---
summary: "Index and load model for engineering-core cross-language discipline docs."
read_when:
  - "Choosing which engineering-core discipline docs to load for a repo or task."
  - "Explaining how disciplines differ from language lanes."
type: "reference"
---

# Engineering Core Disciplines

Disciplines are cross-language engineering contracts. A language lane answers **how this ecosystem implements work**. A discipline answers **what must remain true regardless of ecosystem**.

Use disciplines when a concern crosses TypeScript, Python, Go, Rust, C++, Elixir, generated docs, CLIs, native UIs, browser apps, and services.

## Load model

```text
repo-local work
-> choose language lane(s)
-> choose applicable discipline(s)
-> record repo-local deviations in docs/engineering.local.md
```

Do not load every discipline by default. Load the smallest set that owns the concern.

## Available disciplines

- `design-system` — tokens, components, motion, asset governance, visual consistency.
- `accessibility` — operability and assistive-technology semantics across UI surfaces.
- `validation` — tiered checks, command surfaces, and evidence expectations.
- `testing` — test taxonomy and when each test type earns its cost.
- `local-first-data` — local state, persistence, migrations, sync, and authority.
- `observability` — logs, traces, metrics, local/runtime visibility, and telemetry boundaries.
- `security-privacy` — secrets, permissions, data minimization, dependency risk, privacy posture.
- `documentation` — docs authority, front matter, decisions, architecture, and generated projections.
- `specification-and-dsls` — implicit DSL audits, formalization thresholds, schemas, generators, and executable policy.
- `engineering-reasoning` — lightweight router for deductive, abductive, inductive, adversarial, and Prompt Vault-supported reasoning modes.
- `build-graph-acceleration` — evidence-gated adoption of Buck2, Bazel, Pants, Nx/Turborepo, remote cache, and remote execution.
- `dependency-governance` — adding, pinning, reviewing, and retiring dependencies.
- `service-api` — service/API boundaries, contracts, auth, jobs, health/readiness, migrations, deployment, and rollback.
- `ai-ml` — model assets, inference boundaries, evals, dataset/prompt/model provenance, privacy, safety claims, and reproducibility.
- `performance` — profiling, budgets, benchmark hygiene, regression gates, frontend/backend/GPU measurements, and evidence.
- `release-package` — semantic versions, changelogs, artifact provenance, publishing, compatibility, migrations, deprecation, and rollback.
- `data-governance` — data authority, schemas, lineage, lifecycle, quality, retention, privacy, migrations, and projections.
- `domain-modeling` — domain vocabulary, invariants, workflows, state transitions, aggregate boundaries, and anti-corruption layers.
- `design-patterns` — shared pattern vocabulary for factory, actor, adapter, repository, saga, state machine, and related recurring solution shapes.

## Operating rule

A discipline should state invariants and decision rules. It should not duplicate every lane's tool recipe. Lanes map the invariant into ecosystem-native commands.

Lifecycle rules for adding, splitting, merging, or relocating disciplines live in `docs/discipline-lifecycle.md`. Authority boundaries live in `docs/authority-map.md`.
