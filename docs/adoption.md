---
summary: "How repositories adopt engineering-core lanes, addenda, disciplines, and repo-local overrides."
read_when:
  - "A repo is adding or refreshing docs/engineering.local.md."
  - "An agent needs to choose engineering-core lanes, addenda, or disciplines for a concrete repo."
type: "guide"
---

# engineering-core adoption

Use engineering-core as a versioned upstream source for shared engineering guidance, not as a compatibility shim for legacy names.

Related governance docs:

- `docs/authority-map.md` — where shared guidance, repo-local deviations, templates, validation policy, and runtime truth belong.
- `docs/discipline-lifecycle.md` — when to add, split, merge, or relocate discipline guidance.

## Adoption surface

A repo that adopts engineering-core should carry:

1. `policy/engineering-lane.json` when a machine-readable lane declaration is useful.
2. `docs/engineering.local.md` for human-readable local overrides.
3. A local validation command surface (`just`, package scripts, or equivalent) that records what must pass before handoff.

## Read order

1. Repo-local `docs/engineering.local.md`.
2. Declared lane(s), for example `engineering-core show ts --prefer-repo` from this repo.
3. Conditional addenda only when relevant, for example `ts-frontend` for browser UI work.
4. Cross-language disciplines only when they own the current concern.

## Selection rule

Choose the smallest truthful upstream set:

- one or more language lanes for implementation ecosystems;
- conditional lane addenda for narrower surfaces;
- cross-language disciplines for invariants such as validation, testing, accessibility, documentation, or security/privacy.

Do not load every lane or every discipline by default.

## Safe initialization

`engineering-core init` plans repository adoption without writing by default. It combines an optional catalog profile, explicit `--lane` and `--discipline` values, or conservative repository inference, then closes catalog requirements such as `ts-frontend -> ts`.

```bash
engineering-core init --repo . --profile service-api
engineering-core init --repo . --lane ts --discipline validation --format json
engineering-core init --repo . --lane ts --discipline validation --apply
```

The command emits a unified diff, preserves existing machine-readable fields and structured deviations, and is idempotent after application. It refuses to replace an existing hand-written `docs/engineering.local.md` unless `--force` is supplied after reviewing the proposed diff.

Generated policies reserve `engineering_core.deviations` for evidence-bearing local exceptions. A useful entry records at least an ID, reason, owner, evidence paths or links, and a review date:

```json
{
  "id": "validation.no-browser-e2e",
  "reason": "This package has no browser or external-process boundary.",
  "owner": "platform-tooling",
  "evidence": ["docs/architecture/package-boundaries.md"],
  "review_after": "2027-02-17"
}
```

## Legacy migration

`engineering-core migrate` plans a transition from `docs/tech-stack.local.md` and `policy/stack-lane.json`. It does not delete legacy files unless both `--remove-legacy` and `--apply` are present, and it will not apply a plan that contains conflicts.

```bash
engineering-core migrate --repo .
engineering-core migrate --repo . --remove-legacy --apply
```

## Ownership rule

Adoption should preserve the authority map:

- engineering-core owns shared lanes and disciplines;
- repo docs own local deviations and selected subsets;
- governance-kernel owns canonical validation policy;
- templates own generated defaults;
- Agent Kernel owns runtime task/evidence/decision truth.

Do not move repo-specific commands into shared disciplines, and do not fork shared doctrine into generated templates.

## Hard rename rule

The rename to `engineering-core` is intentionally breaking. Do not recreate old CLI aliases, package aliases, file names, or policy names. Consumers should update references directly.

## Adoption scanning

Use `engineering-core scan-adoption` for reusable adoption mechanics across repo, lane, company, or workspace scopes, including `~/ai-society/core` itself. The scanner reports structural adoption, legacy surfaces, invalid policy JSON, catalog/list command presence, selected lanes/disciplines, heuristic semantic discipline flags, and optional `repo-loop-validation-v1` coverage when declared in `policy/engineering-lane.json`.

Examples:

```bash
engineering-core scan-adoption --scope /path/to/lane-root --include-packages --format json
engineering-core scan-adoption --scope ~/ai-society/core --repo-discovery recursive --include-scope-root --include-packages
engineering-core scan-adoption --scope ~/ai-society/core --scope ~/ai-society/softwareco/infra --repo-discovery recursive --include-scope-root --include-packages --format json
```

Keep generated rollout state in the scope owner, not in engineering-core. For example, a lane root may write `governance/engineering-core-adoption-scan.json` and `docs/project/engineering-core-adoption-dashboard.md`, but engineering-core owns the scanner semantics and generic report shape. Start with warning/ratchet use before hard CI gates so scope owners can distinguish true adoption debt from intentional local posture.

Loop validation visibility is optional. `absent` does not make a repo structurally partial; `partial`, `invalid`, or `unknown-version` only means the repo declared a loop validation contract that needs review.

Scanner traversal is explicitly bounded. Defaults are 1,000 repositories, depth 12, 100,000 visited files, and 10 MiB of policy/doc reads; override them with `--max-repositories`, `--max-depth`, `--max-files`, and `--max-read-bytes`. JSON and Markdown report `completeness`, budget `limits`/`usage`, `omissions`, and per-path `failures`. A `partial` result is truthful usable evidence, not complete coverage. Paths and policy-derived text are escaped before Markdown table rendering. Discovery and policy reads are advisory only: the scanner never executes commands found in consumer repositories.

Both scanning and `recommend --repo` use the same typed policy parser. Malformed policy is reported as `invalid-policy` by scanning and rejected by recommendation rather than being interpreted differently.

## Capability observation

The older structural scanner and the v0.6 capability observer answer different questions:

- `scan-adoption` observes local docs, policy, lane/discipline declarations, command mappings, and optional loop-validation structure.
- `doctor` observes whether one repository can be inspected deterministically and whether declared planning/advisor schemas are statically compatible.
- `scan-capabilities` aggregates doctor results over repeated explicit `--repo` paths and/or bounded owner-produced `--repo-file` lists.

A repository may optionally add exact `engineering-core-capabilities-v1` metadata under `engineering_core.capability_contract`. The contract contains protocol identifiers and declaration status only—never shell commands, argv, URLs, credentials, or executable hooks. Missing declarations remain valid and report `absent/not-declared/not-supplied`.

Static observation is not execution evidence. Doctor and capability scan v1 remain receipt-free and cannot emit `execution-observed` or `evidence-verified`. Keep canonical repository populations, rollout dashboards, exceptions, tasks, and runtime evidence with their owner surfaces.

Use `reconcile-evidence` only when an owner explicitly supplies stable repository-id/path mappings and receipt paths. Its matched result means the supplied receipt, bounded artifact, plan bindings, and revision ancestry reconcile; it does not authenticate the owner or promote evidence into AK, CI, release, compliance, or rollout authority.

```bash
engineering-core doctor --repo /path/to/repo --pretty
engineering-core scan-capabilities --repo /path/to/repo --repo-file owner-repositories.txt --pretty
```

Architecture and exact schemas: `docs/rfc/2026-07-11-capability-observation-and-doctor.md`.

## Owner-use packets

After static adoption, an owner may connect a real task to planning and externally supplied advice without changing capability-observation semantics:

```bash
engineering-core prepare-work --repo . --repo-id <stable-owner-id> --context context.json --pretty > packet.json
engineering-core finalize-work --packet packet.json --advice advice.json --disposition disposition.json --pretty > bundle.json
engineering-core verify-work --repo . --repo-id <stable-owner-id> --bundle bundle.json --pretty
```

These commands use only explicit owner inputs. They do not discover AK tasks, invoke models, execute declared commands, apply patches, or promote receipts. Keep canonical task/evidence state with AK or the declared owner; store generated packets and bundles only when the owner finds them useful. See `docs/owner-use-workflow.md`.

## Version pinning

For local workspace adoption, record the source honestly as `workspace-local-unpinned`. For released adoption, pin to a git tag or package version and record the retrieval command in repo-local policy.
