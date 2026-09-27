---
summary: "Release history for engineering-core."
read_when:
  - "Preparing, verifying, or auditing an engineering-core release."
type: "release-history"
---

# Changelog

## [0.12.2] - 2026-09-27

### Added

- `engineering-core pin --ref <tag> --ref-commit <sha>` moves a repository's release pin and nothing else: `ref`, `release_pin`, `repository`, every engineering-core `--from` source in the policy and local doc, and the release-pin line. Key order, formatting and hand-written text are kept, a raw-SHA `ref` keeps its shape, workspace-local sources become the portable GitHub source, and no adoption journal is written. `migrate --ref` couldn't do this on any fleet repo: it refused the hand-written `docs/engineering.local.md`, and with `--force` replaced it with the managed template (AK6101).

## [0.12.1] - 2026-09-27

### Fixed

- `init`/`migrate --ref` silently kept an existing pin: `_policy_document` preferred the old `ref`, and `release_pin` and pinned commands were never updated (`migrate --ref v0.12.0` on a v0.7.0 repo changed nothing but key order). An explicit `--ref` now moves `ref`, `release_pin`, `repository` and every pinned command to the portable GitHub source when given the new `--ref-commit <sha>`, and refuses with a conflict (naming the `git ls-remote` command that yields the commit) when the commit is missing. Without `--ref`, the existing pin is kept as before (AK6055).

## [0.12.0] - 2026-09-26

### Breaking

- The 15 dotted profile aliases kept for 0.11.x (`ec-ts.justfile` and similar) are removed; use the hyphenated names (`ec-ts-justfile`) (AK6002).

### Added

- `scan-adoption` flags a committed `uv.lock` that recorded a lock-affecting setting (`exclude-newer`, `exclude-newer-package`) that `pyproject.toml` doesn't declare: `uv_lock_records_undeclared_setting:<setting>`. Such a lock came from a user-level `uv.toml`, drifts on other machines, and fails `--locked` in clean environments. Only the lock header is read, so large locks don't exhaust the scan budget.

### Changed

- `dependency-governance` discipline and the py/ts/pi-ts lanes: release-age quarantine exemptions for your own packages, keyed to verified ownership (git and path pins are never quarantined; PyPI exemptions by exact, verified name; npm by owned scope; Bun by exact name only); rename distributions that collide with someone else's registry name.
- CI pins the runner image to `ubuntu-24.04` (instead of `ubuntu-latest`, which moves to Ubuntu 26 on 2026-10-19) and moves actions to current Node 24 majors (checkout v7, setup-python v7, setup-go v7, cache v6).
- Adoption templates and `docs/adoption.md` examples pin the v0.11.0 release.

### Fixed

- `docs/support-policy.md`, `docs/repository-automation.md` and the product posture still described the Python 3.10 floor after v0.11.0 raised it to 3.13.

## [0.11.0] - 2026-09-26

### Breaking

- Python 3.13+ is required (was 3.10+). CI tests 3.13 and 3.14.
- The 15 lane-addendum skills use Agent Skills spec names: dots become hyphens (`ec-lane-ts.justfile` -> `ec-lane-ts-justfile`). The matching dotted profile names remain as `deprecated_aliases` for 0.11.x (AK5774).
- ts and pi-ts lanes: TypeScript 7 only. Typecheck with `tsc --noEmit` from exactly pinned `typescript@7`; `@typescript/native-preview` (`tsgo`) and the dual-compiler `typecheck:fallback` are removed, and dev tools needing the classic compiler API are replaced rather than kept on TypeScript 6 (AK5916).

### Fixed

- Every lane's copyable config and gate commands are now executed at release. The audit found silent false passes in every lane (AK5908, AK5917):
  - ts: Biome `useLiteralKeys` fought `noPropertyAccessFromIndexSignature`; `baseUrl` broke TypeScript 7; `bun.toml` is ignored by Bun (now `bunfig.toml`); `[test] root` skipped `test/`; the Dockerfile copied `bun.lockb`, used `addgroup`, and bundled for the browser target (stubbing `node:fs`). Biome config migrated to 2.x.
  - py: `[tool.uv.scripts]` isn't a uv feature and made uv drop all project `[tool.uv]` settings; new `config` gate fails on uv config warnings; the quarantine is project-declared.
  - rust: gates without `--workspace` skipped workspace members; no toolchain pin; `cargo fmt` rewrote instead of failing.
  - go: format and module gates never failed; `go run ./cmd/...` broke with more than one command.
  - cpp: the reference Justfile's `$$` meant `check`/`ci` never passed; ctest passed with zero tests; stale compile databases hid new files from clang-tidy.
  - elixir: `mix ci` aborted in the dev env; the Docker base tag didn't exist; the release ran with latin1 encoding.
  - common-lisp: `asdf:test-system` exited 0 on failing tests; SBCL's deferred warnings slipped past the load gate.
- uv.lock no longer depends on the machine that wrote it: engineering-core declares `exclude-newer = "7 days"` itself, and release verify proves the lock checks clean with and without a user uv config (AK5775).
- G4-B verifier: revised lineage must name each decided cycle exactly once; failures from `governed_evolution.py` are structured (`invalid_cycle`, `suite_case_failed`) instead of tracebacks (AK5780, AK5781).
- Skill projection prunes orphaned skill directories, and `--check` fails on them.

### Added

- `scripts/lane-conformance.py`: per-lane executable conformance (Quality gates, pinned config blocks, Tool install cache, must-fail probes, real Docker builds), run with `--all` by release verify; `.github/actions/lane-toolchains` installs the pinned base toolchains in CI.
- Rationale and refutations: `docs/project/2026-09-23-lane-config-conformance-greats.md`.

## [0.10.0] - 2026-08-22

### Added

- Added the reversible advisory `agent-interaction` recommendation profile with no preset lanes and the existing disciplines `validation`, `testing`, `security-privacy`, `observability`, `local-first-data`, `specification-and-dsls`, and `documentation`, in that order.
- Added exact CLI list/recommendation coverage for the lane-neutral profile.
- Added the `common-lisp` language lane with first-class language-extension guidance for macros/CLOS/MOP, REPL and hot-redefinition safety, SBCL/ASDF baselines, reproducible Quicklisp/Qlot dependencies, `asdf:test-system` validation, portability boundaries, and a conditional standardized Justfile addendum.
- Added catalog-backed CLI retrieval, documentation, and exact list/show/path/catalog parity coverage for the Common Lisp lane.

### Evidence boundary

- Agent Kernel task 4667 remains the execution membrane for the `agent-interaction` profile only. Bounded cross-owner G3 read-only canary evidence has an independent PASS before that candidate catalog inclusion; it does not authorize or prove the separately operator-directed Common Lisp lane.
- The Common Lisp lane is shared advisory guidance. Its inclusion does not claim consumer adoption, runtime effectiveness, a completed/tagged release, publication, ontology, or mandatory policy.
- Restored the aggregate-gate proof-ownership guidance in the `validation` discipline.
- Restored the v0.8.0 validation evidence record, the narrow-v0.8 owner-use authority ADR, and the v0.8.1 local-release record that the v0.9.0 history reconciliation dropped together with the feature line above.
- Refreshed adoption templates and `docs/adoption.md` worked examples to the latest prior immutable release available during v0.10.0 preparation (`v0.9.0`). Repository self-adoption advances separately after a release is published, so released examples are not rewritten in place.
- Release verification smoke-tests the `common-lisp` lane via `engineering-core show common-lisp`.
- Advanced the package version from `0.9.0` to `0.10.0`; the abandoned in-place `0.8.1`/`0.8.2` version sequence was never released and is intentionally skipped.

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

### Fixed

- Moved owner-use release dogfood scratch from hardcoded `/tmp` to the environment-selected managed temporary directory.

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
