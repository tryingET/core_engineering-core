---
summary: "Release history for engineering-core."
read_when:
  - "Preparing, verifying, or auditing an engineering-core release."
type: "release-history"
---

# Changelog

## [Unreleased]

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
