---
summary: "Release history for engineering-core."
read_when:
  - "Preparing, verifying, or auditing an engineering-core release."
type: "release-history"
---

# Changelog

## [Unreleased]

## [0.9.0] - 2026-08-17

### Added

- Added canonical catalog and pilot-overlay validation, generated-projection checks, a repository self-check, and a Python 3.10–3.13 CI matrix with built-wheel smoke testing.
- Added dry-run-first `engineering-core init` and `engineering-core migrate` workflows with idempotent application, requirement closure, structured deviation preservation, and conservative legacy cleanup.
- Added stable fleet-scan diagnostics, versioned baselines, configurable ratchet gates, a synthetic scan benchmark, and a checked packaged agent skill.
- Added opt-in Ultracite and evidence-safety TypeScript pilot addenda, pilot profiles, and an evidence template without changing the stable TypeScript default.
- Added release-lineage validation, automatic tagged GitHub Releases from validated `main` versions, and merged-branch cleanup automation.

### Changed

- Reconciled the full `v0.8.0` release lineage with the catalog/adoption stack instead of replacing the newer release history with the stale `0.3.x` branch line.
- Raised the declared Python floor to 3.10, matching the syntax and type features used by the package.
- Kept the richer v0.8 doctor, capability, evidence-reconciliation, and owner-use contracts while integrating the new adoption and fleet-ratchet surfaces.

### Fixed

- Prevented package versions from moving below an existing stable tag or releasing from a history that does not contain the latest stable release.
- Replaced per-PR pseudo-release bumps in a stacked change with one coherent `0.9.0` release.
- Added deterministic cleanup for merged `agent/*` and `recovery/*` branches even when the repository auto-delete setting is disabled.

## [0.8.0] - 2026-07-12

### Added

- Added deterministic `prepare-work`, `finalize-work`, and `verify-work` commands for explicit owner task context, plans, optional external advice, owner dispositions/receipts, and matched/stale/mismatched repository verification.
- Added owner-use context, bounded-work-plan, task-bound advice-request, work-packet, evidence-bundle, and work-verification contracts with full Git revisions, focused no-follow file snapshots, transitive digest bindings, and explicit non-authority effects.
- Added deterministic owner-use dogfood and real canary evidence over current Agent Kernel, DSPx, and pi-extensions work.

### Changed

- Reused the canonical advisor response validator in closed-loop processing instead of maintaining a weaker duplicate validator.
- Hardened advisor and general safe JSON loading against symlinks, special files, duplicate members, and non-finite JSON values.
- Added the v0.7 catalog snapshot to historical reconciliation support while preserving v0.6/v0.7 doctor, scan, and reconciliation boundaries.

## [0.7.0] - 2026-07-11

### Added

- Added explicit `reconcile-evidence` joins over owner-supplied repository mappings, receipts, plans, bounded advice artifacts, and Git revision ancestry.
- Added deterministic matched/stale/mismatched projections that preserve owner-reported states without promoting CI, release, AK, compliance, or rollout authority.
- Added bounded no-follow regular-file JSON ingestion and reproducible evidence-reconciliation dogfood.

### Changed

- Hardened existing closed-loop record loading against symlinks, symlinked parents, FIFO/special files, oversized inputs, read races, and invalid UTF-8 JSON.
- Kept `engineering-doctor-v1` and `engineering-capability-scan-v1` receipt-free and backward compatible.

## [0.6.0] - 2026-07-11

### Added

- Added package-native `engineering-core-capabilities-v1` parsing and independent declaration, static-observation, and evidence dimensions.
- Added deterministic, non-executing `doctor` and explicit-population `scan-capabilities` JSON commands.
- Added typed catalog protocol access, bounded no-follow repository-file ingestion, dedicated tests, and deterministic capability dogfood.

### Changed

- Integrated capability dogfood and package-module inspection into local release verification.
- Preserved existing planning, advice, closed-loop, and `scan-adoption` contracts without consumer execution or mutation.

## [0.5.0] - 2026-07-11

### Added

- Added deterministic advisory planning/explanation, bounded provider-neutral advice validation, and strict catalog/policy/repository-fact parsing.
- Added owner-bound dispositions and receipts, calibration, multi-input pattern synthesis, and unapplied doctrine proposals.
- Added a reproducible end-to-end closed-loop dogfood harness with fail-closed negative probes.
- Added bounded recursive scanner completeness, omission, failure, and usage reporting.

### Changed

- Strengthened local release verification, catalog consistency, and wheel/sdist inspection.
- Preserved explicit consumer, CI/release/AK/compliance, and doctrine-owner authority boundaries.

### Fixed

- Rejected JSON-form secret-bearing records, unsafe or hallucinated paths, unknown IDs, malformed inputs, and provenance mismatches.

## [0.3.4] - 2026-05-25

### Added

- Added `repo-loop-validation-v1` as a reusable repo-owned loop validation command contract for agent, slash-command, visible-loop, nexus-loop, and future prompt-loop scenarios.
- Added the `repo-loop-validation` template to the CLI/catalog and package template resources.
- Added optional `engineering_core.loop_validation` scanner visibility with loop validation status counts, missing command details, and markdown report rendering.
- Added engineering-local and validation-tier-map template sections for optional loop validation mappings.

### Changed

- Clarified in validation/testing disciplines, adoption docs, authority map, README, and vision that loop commands produce evidence and do not replace AK, CI/release, repo landing, or governance authority.

## [0.3.3] - 2026-05-19

### Added

- Added `engineering-core scan-adoption` for generic multi-scope engineering-core adoption coverage scans across repos and package/member surfaces.
- Added reusable adoption scan/render modules and tests for structural status, legacy detection, invalid policies, package surfaces, and catalog-aware lane/discipline validation.
- Added `docs/vision.md` for the cross-company adoption scanner/guidance substrate target state.

### Changed

- Documented that engineering-core owns scanner semantics while lane/company roots own generated rollout dashboards and JSON snapshots.
- Updated repo-local AGENTS guidance to include adoption scanner ownership, change discipline, and validation.

## [0.3.2] - 2026-05-18

### Added

- Added repo-local `AGENTS.md` guardrails for lane/discipline/catalog/template changes.

### Changed

- Enriched the machine-readable catalog with kind/category, file name, and short description metadata for lanes, disciplines, and templates.
- Documented version-bump, generated `dist/` artifact policy, and no-legacy-alias rename posture in repo-facing guidance.

## [0.3.1] - 2026-05-17

### Changed

- Clarified release history: `v0.3.0` is the first released artifact containing the completed 10,000 ft authority/adoption/lifecycle foundation, 5,000 ft CLI/catalog/template product surface, and 2,000 ft cross-language discipline layer.

## [0.3.0] - 2026-05-17

### Added

- Added cross-language disciplines for service/API boundaries, AI/ML, performance, release/package, data governance, domain modeling, and design patterns.
- Added catalog/profile coverage and CLI visibility for the new disciplines.
- Added tests that verify new discipline availability, catalog/package catalog sync, architecture wikilinks, and the 63-entry design-pattern vocabulary.

### Changed

- Updated lane docs with concise load pointers for the new disciplines without duplicating discipline content.
- Clarified ROCS/controlled-vocabulary source-owner boundaries with DRY wikilinks to the AK architecture and Layer-12 vocabulary docs.
- Added front matter to the Rust build-graph addendum so docs strict checks pass.

## [0.2.0] - 2026-05-17

### Breaking Changes

- Renamed the shared engineering guidance package, Python import package, CLI, lane file prefix, repo-local override file, and policy metadata to the engineering-core naming family. See [v0.2.0 migration map](docs/releases/migrations/v0.2.0.md).

### Added

- Added cross-language discipline docs for validation, testing, security/privacy, local-first data, accessibility, design systems, documentation, observability, and dependency governance.
- Added adoption artifacts: `docs/adoption.md`, `catalog.json`, and `templates/engineering.local.template.md`.
- Added CLI commands for discipline listing, discipline display, and discipline path lookup.
- Added CLI tests covering lane and discipline command surfaces.

### Changed

- Bumped version to `0.2.0` for the pre-1.0 breaking rename.
- Updated lane docs, symlinks, and Justfile addendum checks to the engineering-core naming family.

### Fixed

- Removed legacy command/package entry points instead of preserving compatibility aliases.
