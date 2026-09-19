---
summary: "Cross-language testing discipline for choosing test forms by risk and cost."
read_when:
  - "Selecting unit, integration, property, contract, browser, E2E, snapshot, visual, or manual tests."
  - "Reviewing whether a test suite matches the behavior and risk being changed."
type: "guide"
---

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
- In agent or prompt loops, use repo-declared loop validation phases (`loop-verify-fast`, impact planning/running, and `loop-landing-check` where present) to select tests by changed behavior and risk; do not treat loop orchestration itself as test authority.

## Test data

- Make fixtures minimal, named, and owned.
- Avoid production secrets or real user data.
- Prefer generated data when invariants matter.
- Version compatibility fixtures when migrations exist.

## Isolation

- Tests never read or change the operator's live state: running services and their sockets, desktop sessions, home-directory configuration, credentials, lock files.
- Default every test to fail closed on that state, for example with an autouse fixture that removes service endpoints from the environment and points configuration roots at empty temporary paths. A test that needs one of them provides a fabricated one.
- A suite that has only run on its author's machine has not shown it is isolated. Run it on a clean runner early, and treat what fails there as isolation bugs, not flakes.
- When a test injects doubles into a spawned process, use a mechanism the host environment cannot shadow and assert that the doubles took effect: a silently missing double runs the real effect.

## Failure modes

- test pyramid dogma that ignores product risk
- brittle E2E tests replacing cheaper boundary tests
- snapshots nobody reviews
- mocks that assert implementation instead of behavior
- property tests without clear invariant
- BDD as ceremony rather than shared executable language
- tests that pass only because the developer's machine provides a service, socket or configuration they silently use
