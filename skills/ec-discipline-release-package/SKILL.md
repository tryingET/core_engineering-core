---
name: ec-discipline-release-package
description: "[ec-discipline] Cross-language release and package discipline for versions, changelogs, artifact provenance, publishing, compatibility, and rollback. Load when: A repo publishes packages, binaries, containers, templates, docs bundles, extension packages, model assets, or service release artifacts.; Work changes versioning, changelogs, artifact provenance, publishing, signing/checksums, compatibility, migration releases, deprecation, or rollback."
---

---
summary: "Cross-language release and package discipline for versions, changelogs, artifact provenance, publishing, compatibility, and rollback."
read_when:
  - "A repo publishes packages, binaries, containers, templates, docs bundles, extension packages, model assets, or service release artifacts."
  - "Work changes versioning, changelogs, artifact provenance, publishing, signing/checksums, compatibility, migration releases, deprecation, or rollback."
type: "guide"
---

# Discipline — Release and Package

## Purpose

Release/package guidance owns cross-language invariants for versioning, changelogs, artifact provenance, publishing, compatibility, migration releases, deprecation, and rollback. Lanes choose ecosystem-specific commands: npm, uv/PyPI, Cargo, GoReleaser, Mix releases, CMake packaging, container tooling, or repo-local scripts.

A release is not just a git tag. It is a claim that a named artifact can be installed, run, audited, and rolled back under a stated compatibility contract.

## Load when

Load this discipline when work touches:

- package publishing, binary/container/model/template/docs artifact generation, or release automation
- semantic versioning, changelogs, release notes, tags, provenance, checksums, signing, SBOMs, or trusted publishing
- public APIs, CLI flags, config files, schemas, database migrations, generated clients, extension manifests, or plugin contracts
- deprecation, migration releases, compatibility windows, rollback, or hotfix posture

Do not load it for private code edits that do not change distributed artifacts or compatibility expectations.

## Versioning invariants

Use semantic versioning where the artifact has consumers that need compatibility signals:

- MAJOR: incompatible API/CLI/config/schema/artifact behavior changes
- MINOR: backward-compatible features, new optional fields, additive APIs
- PATCH: backward-compatible fixes, docs/metadata corrections, small internal changes

If the ecosystem has a different accepted versioning model, document it repo-locally. Calendar versions, internal build numbers, or model versions are acceptable only when their compatibility meaning is explicit.

Version the thing consumers depend on: library API, CLI behavior, service contract, schema, container image, model asset, template output, extension manifest, generated client, persisted data format, or domain vocabulary/state contract.

## Changelog and release notes

A useful release note states:

- what changed for users/operators/integrators
- compatibility impact and required migration steps
- security/privacy relevance if any
- known issues and rollback notes when material
- artifact identifiers: version, tag, image digest, package URL, checksum, model id, or docs bundle id as applicable

Do not fill changelogs with commit noise while hiding migration or compatibility facts.

Derive release notes from the version's changelog entry instead of writing them twice, and rewrite repository-relative links to point at the release tag: release pages and package registries do not resolve them. A README that a registry renders needs absolute links and image URLs for the same reason.

## Artifact provenance

Each release artifact should be traceable to source:

- git revision/tag and clean/dirty state
- build command and environment or CI run
- dependency lockfile/toolchain versions where relevant
- generated files and schemas regenerated from committed inputs
- checksums for downloadable archives/binaries/model assets where useful
- container image digest rather than mutable tag alone
- package registry provenance/trusted publishing when the ecosystem supports it

Treat untraceable artifacts as unreleasable unless the repo explicitly accepts that risk.

## Signing, checksums, and attestations

Use signing/checksums/attestations when artifacts cross a trust boundary, are manually downloaded, run as binaries, install extensions/plugins, or enter production automation.

Minimum practical posture:

- checksums for release archives/binaries/model assets not solely distributed through a trusted registry
- registry provenance/trusted publishing where available and already supported by the ecosystem
- signatures or attestations for high-trust binaries, containers, installers, or enterprise distribution
- documented verification path for consumers if verification is expected

Do not add ceremonial signing that no consumer can verify and no maintainer can operate.

## Publishing rules

Before publishing:

- build from a clean source state or a CI run with explicit provenance
- run the repo's release validation tier, not only unit tests
- verify packaged contents: no secrets, no local caches, no oversized accidental artifacts, no missing README/license/schema/assets
- verify install/import/run smoke from the built artifact, not only from the source tree
- confirm registry namespace, ownership, 2FA/trusted publishing, and token handling
- confirm version uniqueness and tag/release consistency
- build each release once and publish those exact files to every channel (registry, release page, mirrors); record per-file digests and confirm they match across channels
- clear the build output directory first, so a stale artifact from an earlier version is never the one smoke-tested or published

Keep ecosystem-specific commands in lanes or repo-local release docs.

## Release automation

When CI publishes, the release decision is one explicit act (a pushed version tag or an approved run) and everything after it is mechanical:

- check that the tag names the packaged version before building
- give each job only the permission it needs: building reads the source, registry upload uses short-lived trusted-publishing identity in a protected environment restricted to release tags, creating the release writes repository contents; keep no long-lived registry tokens where trusted publishing exists
- pin third-party CI actions to full commit digests, not movable tags
- where the release host makes releases immutable (files and tag locked once published), create the release together with its files, checksums and notes in one step; publishing first and attaching files later fails, and the release can then only be corrected in its notes
- order the channels so a failure leaves a state you can explain, and say in the release process which channel is authoritative when the second one fails

## Release authority

A release artifact should have one authoritative release surface: tag, registry version, image digest, package metadata, or documented local release record. Avoid split-brain releases where README, changelog, package metadata, container tag, and generated docs disagree.

Keep one version string everywhere consumers can read it: package metadata, the version the runtime reports, the newest changelog heading and the tag. Enforce it with a test and a release-time check rather than by review.

Generated artifacts must be either included intentionally or regenerated deterministically by consumers. Do not make consumers guess whether checked-in generated files are source, projection, or proof output.

## Compatibility and migration releases

Compatibility includes more than library functions:

- CLI flags, output formats, config keys, env vars, file layouts, generated schemas, event payloads, database migrations, container ports, extension manifests, model/prompt behavior, and operator workflows
- generated clients and downstream templates
- persisted data written by prior versions
- queued jobs/events emitted by prior versions

For migrations, prefer staged releases:

1. Add forward-compatible support.
2. Migrate/backfill while old readers still work.
3. Switch writers/traffic.
4. Remove old behavior only after deprecation window and evidence.

Document rollback hazards when data or external side effects cannot be undone.

## Deprecation

A deprecation needs:

- what is deprecated and replacement path
- first version/date carrying warning
- planned removal version/date or condition
- affected consumers and detection method
- validation that warnings are visible but not noisy enough to be ignored

Do not silently remove behavior that consumers could reasonably depend on.

## Release validation

Release validation should match artifact risk:

- package contents check: manifest/files/license/readme/assets/schemas
- build/rebuild from clean checkout
- install/import/run smoke from built artifact
- compatibility tests for public API/CLI/schema/config behavior
- migration dry run or fixture upgrade/downgrade where data is involved
- security/privacy/dependency review for changed dependencies, generated artifacts, or new distribution channels
- performance/eval evidence for release notes that make performance or AI/ML quality claims
- the release validation on a clean runner before tagging; a suite that has only run on a maintainer's machine has not shown it is independent of that machine (see `testing`)
- install from the registry after publishing; consumer-side quarantine settings (a minimum package age) can hide a fresh release, so relax them for that one package during verification instead of disabling them

Use `validation`, `testing`, `dependency-governance`, `security-privacy`, `service-api`, `data-governance`, `domain-modeling`, `performance`, and `ai-ml` as applicable.

## Rollback and hotfix posture

A rollback plan names:

- artifact to roll back to
- config/schema/data/job/event compatibility constraints
- whether downgrade is safe after migrations or writes by the new version
- feature flag/traffic control/manual mitigation path
- owner who can publish or deploy a hotfix

For package releases, remember that unpublishing may be impossible or harmful. Prefer patch releases, yanks/deprecation notices, and clear advisory notes according to ecosystem norms.

## Failure modes

- Version number changes but no artifact provenance or install smoke exists.
- A changelog hides breaking config/schema/CLI behavior under "refactor".
- Release artifacts include local caches, secrets, generated junk, or omit required assets.
- A package is tested only from source, not as installed/published.
- A migration release has no rollback story for already-written data.
- Mutable container tags or model names are treated as stable artifact identity.
- Package metadata, changelog, generated docs, and tag describe different releases.
- Signing exists but verification is undocumented or impossible for consumers.
- Files are attached to an already-published release on a host that makes releases immutable, leaving a release without its artifacts.
- The registry and the release page carry different builds of the same version.
- Release notes or a registry-rendered README keep repository-relative links that break outside the repository.
- A stale artifact from an earlier build is the one that gets smoke-tested or published.
