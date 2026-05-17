---
summary: "Cross-language domain modeling discipline for vocabulary, invariants, boundaries, workflows, and anti-corruption layers."
read_when:
  - "Work changes business/domain concepts, state transitions, permissions, workflow rules, aggregates, policies, or cross-boundary vocabulary."
  - "A repo is accumulating anemic transport/database models, duplicated business rules, or ambiguous domain language."
type: "guide"
---

# Discipline — Domain Modeling

## Purpose

Domain modeling owns cross-language invariants for business vocabulary, entities, value objects, aggregates, workflows, state transitions, policies, and anti-corruption boundaries. Language lanes choose types, modules, classes, structs, behaviours, protocols, schemas, and persistence libraries.

This discipline is not a command to perform heavyweight DDD everywhere. It is a guard against letting transport shapes, database rows, UI forms, or vendor payloads become the domain by accident.

## Load when

Load this discipline when work touches:

- domain vocabulary, business rules, permissions, lifecycle states, workflows, or policy decisions
- entities, value objects, aggregates, invariants, commands, events, or state machines
- duplicated business logic across service, UI, job, and database layers
- mapping between external/vendor concepts and internal product concepts
- schema/API changes whose meaning depends on domain semantics, not just field shape
- product areas where ambiguous words cause wrong code, wrong tests, or wrong decisions

Do not load it for small CRUD/admin utilities where fields are genuinely passive and no behavior/invariant is hidden.

## Core rule

The domain model is the code/docs contract that protects meaning. It is not automatically:

- the database schema
- the API request/response type
- the UI form state
- the ORM model
- the vendor payload
- the analytics event

Any of those may resemble the domain. None should silently own it unless the repo explicitly accepts that simplification.

## Vocabulary and concept invariants

- Use one name for one concept; do not reuse one word for multiple lifecycle states or authority classes.
- Define terms at the boundary where ambiguity causes behavior changes.
- Make illegal states unrepresentable where the language/tooling reasonably supports it.
- Represent domain absence precisely: unknown, not applicable, not yet collected, redacted, deleted, and failed are different states.
- Keep display labels/translations separate from stable domain values.
- Treat renamed concepts as migrations when persisted data, APIs, docs, events, or tests depend on the old name.

## Controlled vocabulary and ROCS boundary

Domain-modeling guidance may identify candidate vocabulary, local enum names, state names, and bounded-context terms. It does not make those terms canonical society semantics by itself.

DRY authority rule:

- Repo-local domain terms live in the owning repo until they need shared semantics.
- Shared controlled vocabulary and ontology changes belong in ROCS / ontology owner surfaces, not in engineering-core prose.
- AK / `society.v2.db` may store runtime facts that reference controlled terms, but does not become ontology authority by convenience.
- Engineering-core should link to the semantic owner instead of copying canonical vocabularies.

Architecture references for this boundary:

- [[~/ai-society/softwareco/owned/agent-kernel/docs/project/ai-society-convergence-architecture.md|AI Society Convergence Architecture]]
- [[~/ai-society/softwareco/owned/agent-kernel/docs/project/2026-04-25-layer-12-operator-vocabulary-boundary.md|Layer-12 Operator Vocabulary Boundary]]

Use `specification-and-dsls` to decide when a local vocabulary should become a schema, generator, linter, or executable policy. Use ROCS-owned workflows when a term must become shared ontology rather than repo-local language.

## Design patterns boundary

Use `design-patterns` for the shared pattern vocabulary, including classic names such as factory, adapter, observer, actor, repository, saga, and state machine. Pattern guidance still belongs closest to the invariant it protects:

- domain patterns such as entity, value object, aggregate, policy, domain event, state machine, and anti-corruption layer belong here
- service/integration patterns such as idempotent endpoint, outbox, saga/process manager, webhook receiver, and adapter facade belong in `service-api`
- data patterns such as canonical store, projection, cache, event/audit log, migration, and backfill belong in `data-governance`
- UI/component patterns belong in `design-system`, `accessibility`, or the relevant frontend addendum
- language idioms and framework-specific realization belong in lanes, not disciplines

Promote a pattern into engineering-core only when it recurs across repos and prevents a real failure. Otherwise record the selected pattern and local tradeoff in `docs/engineering.local.md` or the repo's architecture docs.

## Invariants and policies

A domain invariant is a rule that must remain true regardless of UI, API, job, or storage path. Put invariants where all write paths pass through them, or prove equivalent enforcement elsewhere.

Examples:

- an order cannot be paid twice
- a tenant cannot access another tenant's resource
- a session cannot complete before it starts
- a release cannot be published without artifact provenance
- a model output cannot be treated as validated medical advice

Policies that change by product/business decision should be named and isolated. Do not bury policy in controller glue, SQL snippets, template conditionals, or test fixtures.

## Boundaries and aggregates

Use aggregate/boundary thinking when consistency matters:

- identify which state changes must be atomic
- identify which references can be eventual, cached, or derived
- keep transaction boundaries aligned with invariants when possible
- avoid cross-aggregate synchronous updates unless the invariant truly requires them
- use domain events for meaningful completed facts, not for every internal method call

Do not split a domain into services just because concepts have different names. Split when ownership, scaling, trust, failure, or release boundaries justify it.

## Workflows and state machines

When behavior depends on lifecycle, model the lifecycle explicitly:

- states, transitions, guards, side effects, retries, cancellation, and terminal states
- who/what may perform each transition
- what data becomes required or immutable at each state
- whether transitions are reversible, compensating, or append-only
- how old persisted states migrate when the workflow changes

Boolean flags are acceptable for simple independent facts. They are traps when they encode a hidden state machine.

## Anti-corruption boundaries

External systems and vendors bring foreign models. Protect the internal domain:

- translate vendor/API/database/event payloads into internal concepts at the boundary
- keep vendor status codes and naming from leaking through the whole codebase unless intentionally adopted
- record lossy mappings and impossible/unknown external states
- isolate compatibility shims for legacy schemas and generated clients

An anti-corruption layer is worthwhile when foreign semantics would otherwise contaminate core rules.

## When not to over-model

Do not invent elaborate domain architecture when:

- the repo is a thin adapter with no durable product rules
- the data is genuinely append-only telemetry with simple schema rules
- the workflow is temporary/prototype and not yet stable
- the cost of ceremony exceeds the cost of local clarification

Use the smallest model that prevents real semantic failure: glossary, type alias, enum, state machine, policy object, aggregate, or separate bounded context.

## Cross-references

- `data-governance` owns authority, schema evolution, lineage, lifecycle, quality, and retention.
- `service-api` owns transport/API boundaries, errors, auth, idempotency, and deployment posture.
- `specification-and-dsls` owns formalization thresholds for naming conventions, schemas, generators, and executable policy.
- `testing` owns tests that prove domain invariants and workflow transitions.
- `security-privacy` owns data classification, permissions, and privacy posture.
- `ai-ml` owns model behavior claims where probabilistic output enters a domain decision.

## Validation expectations

For material domain changes, provide:

- changed vocabulary/concepts and affected persisted/API/event/docs surfaces
- invariant tests for rules that must survive all write paths
- workflow/state transition tests when lifecycle changed
- migration/compatibility plan for renamed states, enums, events, or persisted concepts
- anti-corruption mapping tests for external/vendor payloads where semantics are lossy or risky

## Failure modes

- Database tables become the domain model and business rules scatter into controllers/jobs/UI.
- API DTOs become internal truth and external compatibility freezes bad concepts.
- Boolean flags encode an untested state machine.
- Same word means different things in product docs, code, database, and analytics.
- Vendor statuses leak everywhere and become impossible to migrate.
- Domain rules are tested only through happy-path endpoints, not at the invariant boundary.
