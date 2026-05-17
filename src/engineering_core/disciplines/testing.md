# Discipline — Testing

## Purpose

Choose test forms by risk, not fashion. Lanes provide tools; this discipline defines when each test type earns its cost.

## Test taxonomy

- **Unit tests** — pure functions, small modules, state transitions.
- **Integration tests** — component + dependency boundary, DB/files/API adapters.
- **Contract/schema tests** — API payloads, generated files, migrations, config formats.
- **Property/fuzz tests** — parsers, normalizers, permissions, serializers, routing, invariants.
- **Golden/snapshot tests** — generated artifacts and stable render output.
- **Browser/E2E tests** — user-critical flows in real browser/runtime context.
- **Accessibility tests** — automated plus keyboard/assistive review for critical paths.
- **Performance/load tests** — latency, throughput, memory, frame budget, startup cost.
- **Migration/compatibility tests** — old data/config/artifacts remain readable or fail safely.
- **BDD/Gherkin** — only when executable shared scenarios materially improve cross-role agreement.

## Decision rules

- Test pure domain logic below UI/service layers.
- Test adapters at their boundary with realistic failure cases.
- Use property tests when examples under-sample a large input space.
- Use E2E only for flows whose correctness depends on browser/runtime integration.
- Use snapshots for intentional stable output; review snapshot changes as behavior changes.
- Add regression tests for bugs that were plausible, not one-off environmental accidents.

## Test data

- Make fixtures minimal, named, and owned.
- Avoid production secrets or real user data.
- Prefer generated data when invariants matter.
- Version compatibility fixtures when migrations exist.

## Failure modes

- test pyramid dogma that ignores product risk
- brittle E2E tests replacing cheaper boundary tests
- snapshots nobody reviews
- mocks that assert implementation instead of behavior
- property tests without clear invariant
- BDD as ceremony rather than shared executable language
