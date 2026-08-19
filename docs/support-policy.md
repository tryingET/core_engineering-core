---
summary: "Supported platforms, compatibility surfaces, release channels, and support boundaries for engineering-core."
read_when:
  - "Deciding whether an environment, version, command, schema, or integration is supported."
type: "reference"
---

# Support and compatibility policy

## Product stage

`engineering-core` is a pre-1.0, source- and GitHub-Release-distributed CLI plus versioned engineering content. It is suitable for controlled adoption where consumers pin a tag or commit and review upgrades. It is not currently published to a Python package registry and does not provide a hosted service.

## Validated environment

The required CI matrix validates Python 3.10, 3.11, 3.12, and 3.13 on Ubuntu. Linux is therefore the production-validated platform today. macOS and Windows behavior is best-effort until those operating systems are represented in required CI; consumers on those platforms should pin a version and run their own acceptance checks.

`uv` and Git are required for the documented source-based development and tagged-install workflows. The built wheel is platform-independent Python, but repository checkout behavior may still depend on filesystem and symlink semantics.

## Supported release line

The latest stable GitHub Release and current `main` are supported for fixes. Older pre-1.0 releases are historical compatibility points rather than maintained long-term-support branches.

Consumers should pin an immutable commit for reproducibility while retaining the corresponding semantic tag for human-readable intent. Upgrade reviews should read the changelog, release notes, migration notes, and catalog-history changes.

## Compatibility surfaces

Consumer-facing surfaces include:

- the `engineering-core` command and documented subcommand names;
- documented exit-code meaning;
- versioned JSON schema identifiers such as `engineering-plan-v1`;
- catalog IDs, kinds, dependencies, and selection semantics;
- packaged lane, discipline, template, and profile identifiers;
- release artifact names and catalog-history snapshots.

Python modules are internal implementation details unless a module or symbol is explicitly documented as a public API.

Within a versioned JSON protocol, field meaning should remain backward compatible. An incompatible protocol change should introduce a new schema identifier, coexist long enough for migration where practical, and include fixtures and migration notes. Catalog ID removal or semantic repurposing is a breaking content change even when Python code is unchanged.

## Support boundaries

The project provides deterministic static tooling and documentation. It does not:

- execute consumer validation commands by default;
- operate or monitor consumer services;
- invoke a model provider unless an owner supplies an external adapter;
- decide organizational compliance;
- grant exceptions or promote generated evidence to authority;
- guarantee correctness of third-party tools named in lane guidance;
- provide a response-time or uptime service-level agreement.

Use GitHub issues for reproducible bugs and content proposals. Use the private process in `SECURITY.md` for vulnerabilities. Questions that depend on a specific repository's architecture or policy belong in that repository's local engineering documentation.
