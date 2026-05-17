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

## Operating rule

A discipline should state invariants and decision rules. It should not duplicate every lane's tool recipe. Lanes map the invariant into ecosystem-native commands.

Lifecycle rules for adding, splitting, merging, or relocating disciplines live in `docs/discipline-lifecycle.md`. Authority boundaries live in `docs/authority-map.md`.
