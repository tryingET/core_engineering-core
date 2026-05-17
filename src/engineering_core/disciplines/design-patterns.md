---
summary: "Cross-language design-pattern lexicon and selection discipline for recurring code, service, data, concurrency, and architecture shapes."
read_when:
  - "Work chooses or reviews a named implementation/design pattern such as factory, actor, repository, saga, strategy, adapter, or state machine."
  - "A repo needs pattern vocabulary hints without turning pattern names into architecture cargo cult."
type: "reference"
---

# Discipline — Design Patterns

## Purpose

Design patterns are a vocabulary for recurring solution shapes. They are not architecture law, not proof of quality, and not a substitute for domain modeling, tests, or operational evidence.

This discipline gives cross-language pattern hints so agents and engineers can recognize common shapes, ask the right tradeoff questions, and avoid inventing misleading local names. Language lanes decide how a pattern is realized in TypeScript, Python, Go, Rust, C++, Elixir, or another ecosystem.

## Load when

Load this discipline when:

- code introduces a named pattern or should probably use a known pattern name
- review debates factory/actor/repository/service/saga/state-machine/etc. shapes
- a pattern appears repeatedly across repos and needs consistent vocabulary
- architecture docs need a compact pattern pointer without duplicating a pattern textbook

Do not load it just to decorate simple code with pattern names.

## Rule

A pattern is justified only by the force it handles:

- creation complexity
- structural boundary or compatibility
- behavioral variation
- lifecycle/state coordination
- concurrency/async coordination
- persistence/data authority
- integration/release/operational boundary

If there is no force, the pattern is ceremony.

## Pattern lexicon

Use this as a hint list, not a mandate. Prefer the smallest pattern that names the real force.

### Creational patterns

1. **Abstract Factory** — create families of related objects without binding callers to concrete types.
2. **Builder** — construct complex objects stepwise while preserving validation/readability.
3. **Factory Method** — let a subtype or local policy choose the concrete product.
4. **Prototype** — create by cloning/configuring an existing exemplar.
5. **Singleton** — one shared instance; use rarely because global state hides dependencies and test seams.

### Structural patterns

6. **Adapter** — translate one interface into another.
7. **Bridge** — separate abstraction from implementation so both can vary.
8. **Composite** — treat individual and tree/group objects uniformly.
9. **Decorator** — wrap behavior without changing the underlying object/interface.
10. **Facade** — provide a simpler interface over a subsystem.
11. **Flyweight** — share immutable/heavy intrinsic state across many small objects.
12. **Proxy** — stand in for another object to control access, laziness, remoteness, or protection.

### Behavioral patterns

13. **Chain of Responsibility** — pass a request through ordered handlers until one handles it.
14. **Command** — represent an action as data for queueing, undo, logging, or dispatch.
15. **Interpreter** — evaluate a small language or expression grammar.
16. **Iterator** — traverse without exposing collection representation.
17. **Mediator** — centralize coordination among peers to reduce direct coupling.
18. **Memento** — capture/restore state without exposing internals.
19. **Observer** — notify dependents when state changes.
20. **State** — move state-specific behavior into explicit state objects/types.
21. **Strategy** — swap algorithms/policies behind a stable interface.
22. **Template Method** — fixed algorithm skeleton with overridable steps.
23. **Visitor** — add operations over a stable object structure without modifying each type.

### Concurrency, reactive, and resilience patterns

24. **Actor** — isolate state inside message-processing entities.
25. **Active Object** — decouple method invocation from execution through queued requests.
26. **Reactor** — demultiplex events and dispatch handlers synchronously around an event loop.
27. **Proactor** — start async operations and handle completion events later.
28. **Monitor Object** — encapsulate synchronized access to shared state.
29. **Thread Pool** — reuse bounded workers for many tasks.
30. **Producer-Consumer** — decouple production and consumption with a queue/buffer.
31. **Scheduler** — centralize ordering/timing of work.
32. **Future/Promise** — represent a value available later.
33. **Publish-Subscribe** — decouple publishers from subscribers through a topic/bus.
34. **Event Loop** — serialize asynchronous callback/task processing through one loop.
35. **Circuit Breaker** — fail fast around unhealthy dependencies until recovery conditions hold.

### Enterprise, service, and data patterns

36. **Repository** — collection-like access to aggregates/data while hiding persistence details.
37. **Unit of Work** — track and commit a coherent set of changes transactionally.
38. **Data Mapper** — map between domain objects and persistence records without coupling them.
39. **Active Record** — combine persistence operations with a data object; useful for simple CRUD, risky for rich domains.
40. **Identity Map** — ensure one in-memory object per persisted identity in a unit of work.
41. **Lazy Load** — defer loading until needed; watch hidden IO and latency.
42. **Service Layer** — expose application operations/use cases over domain logic.
43. **Domain Model** — encode behavior and invariants in domain objects/types, not only scripts/records.
44. **Transaction Script** — implement a use case procedurally; fine for simple workflows, brittle for rich domains.
45. **CQRS** — separate command/write model from query/read model.
46. **Event Sourcing** — persist state as an event log and derive current state by replay/projection.
47. **Saga** — coordinate long-running distributed workflow with compensating actions.
48. **Outbox** — atomically persist state change and outgoing message for reliable publish.
49. **Inbox** — record received messages for dedupe/idempotent processing.
50. **Anti-Corruption Layer** — translate foreign models so they do not contaminate internal semantics.
51. **Strangler Fig** — incrementally replace a legacy surface by routing slices to a new implementation.

### Functional, policy, and extension patterns

52. **Dependency Injection** — pass dependencies explicitly to improve substitution, testing, and wiring clarity.
53. **Null Object** — replace null checks with a do-nothing implementation when absence has neutral behavior.
54. **Specification** — name and compose business predicates/rules.
55. **Result/Either** — represent success/failure as data instead of exception-only flow.
56. **Option/Maybe** — represent presence/absence explicitly.
57. **Lens** — focus immutable reads/updates into nested structures.
58. **Pipeline** — compose ordered transformations or processing stages.
59. **Middleware** — wrap request/operation processing with ordered cross-cutting behavior.
60. **Plugin** — load optional behavior behind a stable extension contract.
61. **Registry** — map names/keys to implementations; useful for extension points, risky as hidden global state.
62. **State Machine** — model states, transitions, guards, and effects explicitly.
63. **Policy Object** — isolate a decision rule so it can be named, tested, versioned, and swapped.

## Placement rule

Pattern guidance belongs closest to the invariant it protects:

- domain patterns: `domain-modeling`
- service/integration patterns: `service-api`
- data/persistence patterns: `data-governance` and `local-first-data`
- concurrency/runtime patterns: `performance`, `observability`, and the language lane
- UI/component patterns: `design-system`, `accessibility`, and frontend addenda
- package/release migration patterns: `release-package`

Use this discipline as the vocabulary index. Use the owning discipline for the actual invariant and validation expectations.

## Selection questions

Before adding a named pattern, answer:

1. What force does it handle?
2. What simpler code would fail, and how?
3. What invariant does the pattern protect?
4. What dependency, lifecycle, concurrency, or persistence cost does it add?
5. How will tests prove the pattern boundary rather than only the happy path?
6. Is this pattern local to one repo, or recurring enough to document in engineering-core?

## Failure modes

- Pattern names used as prestige instead of explanation.
- Factory/registry/DI hides a dependency graph that should be explicit.
- Actor/event/pub-sub hides ordering, backpressure, idempotency, or failure semantics.
- Repository abstracts away queries that are actually domain or performance decisions.
- Singleton creates untestable global state.
- Saga/outbox/event sourcing adopted without operational observability and replay policy.
- Pattern catalogs duplicate ROCS/domain vocabulary instead of linking to semantic owners.
