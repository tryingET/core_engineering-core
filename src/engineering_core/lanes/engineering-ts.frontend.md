---
summary: "TypeScript frontend application addendum for browser apps and interactive user-facing UI."
read_when:
  - "A TypeScript repo owns browser app, SPA, camera/media UI, local-first frontend data, or design-heavy frontend behavior."
  - "Work changes frontend state, routing/forms, media/device lifecycle, Rive/motion, browser tests, or accessibility."
type: "guide"
---

# TypeScript Lane — Frontend Application Addendum

Read this addendum when a TypeScript repo is a browser app, SPA, interactive UI, camera/media UI, local-first user-data app, design-heavy frontend, or frontend package that owns product interaction.

Do not read it for backend-only services, CLIs, small libraries, static scripts, or package-only repos unless they own user-facing browser behavior.

## State taxonomy

| State kind | Default | Use when | Do not use when |
|---|---|---|---|
| trivial local UI | plain TypeScript/component-local state | toggles, field drafts, hover/focus, display-only values | state has lifecycle, retries, permissions, or async coordination |
| product workflow | XState | setup, camera/model readiness, sessions, multi-step flows, guarded transitions | simple independent values |
| server/cache | TanStack Query or equivalent | remote APIs, cache invalidation, retry/refetch, optimistic updates | app has no remote read/write API |
| durable user data | explicit persistence module/package | history, preferences, calibration, offline data, migrations | ephemeral session values |
| animation state | Rive state machines or CSS/SVG | motion communicates product behavior | static decoration |

## XState rule

Use XState for frontend flows with explicit lifecycle, event coordination, guarded transitions, async invocation, retries, cancellation, parallel regions, permission state, device readiness, or model loading.

Good XState targets:

- onboarding/setup flows
- camera/microphone/device permission states
- WASM/model/media loading readiness
- workout/session lifecycles
- exercise phase machines
- TTS/backend/device availability
- upload/sync/import/export flows

Bad XState targets:

- simple open/closed toggle
- one text input
- isolated hover/focus state
- static display values

Validation expectation:

- state charts or machine definitions are testable separately from rendering
- impossible states are eliminated or named explicitly
- failure/retry/cancel paths are modeled, not left as booleans

## Rive rule

Use Rive for interactive/animated components when motion carries product meaning.

Good Rive targets:

- guided exercise demos
- calibration affordances
- coaching feedback characters or visual guides
- unlock/progression/reward moments
- animated explanations of changing state

Bad Rive targets:

- static icons
- decoration with no behavioral meaning
- effects CSS/SVG can express more simply

Required integration notes:

- keep assets in explicit asset paths, for example `src/assets/rive/`
- document Rive state-machine inputs/events
- type the code boundary that drives animation inputs
- provide reduced-motion fallback
- provide non-visual meaning for assistive technology users

## Local-first frontend user data

Use localStorage only for tiny/simple values with low migration cost.

Use IndexedDB, OPFS, SQLite-WASM, or a repo-approved local persistence layer when data is structured, queryable, durable, large, or migration-sensitive.

Durable frontend data requires:

- schema/version
- migration path
- export/reset behavior
- corruption behavior
- privacy classification
- sync/backup decision if remote behavior exists

## Browser testing

- Pure logic: Bun Test or Vitest.
- Browser behavior: Playwright.
- Accessibility: axe/playwright checks plus keyboard review for critical flows.
- Visual regression: only when UI stability matters enough to review diffs.
- Device/media flows: fake adapters for unit tests; real browser/device smoke where practical.

## Media, ML, and device lifecycle

For camera, microphone, sensors, WASM, ML models, GPU/WebGL, and local devices:

- model permission and readiness explicitly
- separate loading, ready, degraded, denied, failed, and unavailable states
- use Workers when CPU/model work causes UI jank
- cache/version large assets deliberately
- provide fallback or degraded mode when device/model/backend is absent
- never imply health/medical accuracy beyond the validated product claim

## Routing and forms

Do not add router/form libraries by default.

Add a router when navigation, deep links, nested routes, or history semantics become product-relevant.

Add a form library when validation, dynamic fields, async submission, or error recovery exceed plain controlled inputs.

## Applicable disciplines

Load these discipline docs when the concern applies:

- `disciplines/design-system.md` for tokens, components, motion, assets, and visual consistency.
- `disciplines/accessibility.md` for keyboard, focus, semantics, reduced motion, and assistive-technology behavior.
- `disciplines/local-first-data.md` when frontend user data is durable, structured, migrated, synced, exported, or privacy-sensitive.
- `disciplines/security-privacy.md` for camera/media permissions, health-adjacent user data, telemetry, secrets, and dependency risk.
- `disciplines/testing.md` and `disciplines/validation.md` for browser, accessibility, E2E, visual, and device/media validation choices.
- `disciplines/observability.md` when frontend runtime performance, field errors, traces, or user-flow evidence matter.

Frontend code should use semantic tokens and documented component contracts before component proliferation.
