---
summary: "RFC for native engineering-core doctor and factual capability-observation commands."
read_when:
  - "Changing engineering-core capability declarations, doctor behavior, or cross-repo capability reporting."
type: "rfc"
---

# RFC — Capability observation and doctor

## Status

Proposed for implementation under operator direction on 2026-07-11. This RFC defines a read-only observation contract; it does not authorize consumer-repo mutation or society-wide rollout by itself.

## Problem

Engineering-core v0.5 provides deterministic planning, bounded advisor requests, validated advice, dispositions, receipts, calibration, pattern synthesis, and doctrine proposals. The product cannot yet answer three operational questions truthfully:

1. Is the local CLI and a target repository ready to use these capabilities?
2. Has a repository declared and statically demonstrated a capability?
3. Across an explicit repository population, how many repositories are absent, declared, observable, blocked, or evidenced?

Ad-hoc shell/Python snippets can answer fragments, but they are not versioned product contracts. The existing `scan-adoption` command measures the older docs/policy/lane surface, not v0.5 capability maturity.

## Decision drivers

- Stable, reusable semantics belong in the packaged CLI, not copied scripts.
- Scripts remain appropriate for release orchestration and deterministic dogfood.
- Doctor and scanners must never execute repository-declared commands.
- Declaration, static observation, owner disposition, execution observation, and verified evidence are distinct facts.
- Repository populations must be explicit inputs; engineering-core must not invent canonical society scope.
- Existing `scan-adoption` output remains compatible.
- Outputs must be deterministic, schema-versioned, bounded, and owner-safe.

## Proposed architecture

```text
policy/engineering-lane.json
        |
        v
capability parser ---- catalog/protocol metadata
        |                         |
        +----------+--------------+
                   v
          capability evaluator
          /                  \
 doctor --repo           scan-capabilities
 fixed local checks      explicit --repo/--repo-file population
          \                  /
           +------ typed reports ------+
                  JSON, deterministic
```

### Product surfaces

Native package modules and CLI commands own stable behavior:

- `engineering_core.capabilities`: versioned policy contract and pure evaluation.
- `engineering_core.doctor`: deterministic, non-executing local readiness checks.
- `engineering_core.capability_scan`: explicit-population aggregation and proof-tier counts.
- `engineering-core doctor --repo ...`.
- `engineering-core scan-capabilities --repo ... | --repo-file ...`.

Scripts own reproducible orchestration only:

- `scripts/dogfood-capabilities.py` exercises public APIs and CLI behavior.
- Release verification invokes the dogfood script.
- Scripts do not define schemas, maturity states, or scanner semantics.

### Why no new filesystem-wide inventory command in v1

A canonical AI Society repository population belongs to AK/company inventory owners, not engineering-core. Filesystem discovery can include archives, backups, worktrees, and candidates, and broad recursive walks can exhaust budgets before later scopes. The v1 scan therefore consumes explicit repository paths, either repeated `--repo` flags or an owner-produced newline-delimited `--repo-file`. A later `engineering-repository-inventory-v1` may be added when its source owner and metadata contract are decided.

## Policy contract

Optional nested block under `engineering_core`:

```json
{
  "engineering_core": {
    "ref": "v0.5.0",
    "capability_contract": {
      "version": "engineering-core-capabilities-v1",
      "capabilities": {
        "planning": {
          "status": "declared",
          "schema": "engineering-plan-v1"
        },
        "advisor": {
          "status": "declared",
          "request_schema": "engineering-advice-request-v1",
          "response_schema": "engineering-advice-response-v1"
        },
        "closed_loop": {
          "status": "declared",
          "receipt_schema": "engineering-evidence-receipt-v1",
          "disposition_schema": "engineering-recommendation-disposition-v1"
        }
      }
    }
  }
}
```

V1 intentionally contains no shell strings, argv, URLs, environment variables, or executable hooks. Unknown contract versions, capability names, fields, statuses, and schema identifiers are reported as invalid or unsupported.

Existing policy files without this block remain valid and mean `capability declaration absent`.

## Observation model

Each capability reports independent dimensions:

- `declaration_status`: `absent | valid | invalid | unsupported`.
- `observation_status`: `not-declared | observable | blocked | not-observed`.
- `evidence_status`: `not-supplied` in v1.

The evidence values `declared`, `execution-observed`, `evidence-verified`, `stale`, `mismatched`, and `unknown` are reserved for a later receipt-input extension and **must not be emitted by v1**. Capability declaration and receipt declaration are never represented by the same field.

Normative transitions:

| Capability | Declaration input | Declaration status | Static observation | Observation status | Evidence status |
|---|---|---|---|---|---|
| any | contract absent, or capability omitted from a valid contract | `absent` | none | `not-declared` | `not-supplied` |
| any | unknown contract version | `unsupported` | none | `blocked` | `not-supplied` |
| any | malformed/unknown capability fields or schema ids | `invalid` | none | `blocked` | `not-supplied` |
| planning | exact valid declaration | `valid` | compile the plan twice | `observable` only when both plans have `status=complete` and identical `plan_sha256`; otherwise `blocked` | `not-supplied` |
| advisor | exact valid declaration | `valid` | compile plan and build request twice | `observable` only when both request digests match and the plan is complete; otherwise `blocked` | `not-supplied` |
| closed_loop | exact valid declaration | `valid` | schema compatibility only | `not-observed`; v1 accepts no receipts | `not-supplied` |

`engineering-plan-v1.status=complete` means the deterministic compiler found no unknowns, error diagnostics, or bounded-read omission diagnostics under its existing contract. It does not mean repository commands ran or operational adoption occurred.

An empty `capabilities` object is valid for forward migration but yields a `degraded` doctor result. A `healthy` result requires at least one declared capability. Aggregation precedence is `blocked` over `not-observed` over `not-declared` over `observable`. Static compatibility never upgrades evidence status. No result is called unqualified `adopted` or `verified`.

## Doctor contract

`engineering-doctor-v1` performs fixed checks only:

1. target is a readable directory;
2. catalog loads and protocol identifiers exist;
3. policy is absent, valid, invalid, or unsupported;
4. released pin versus workspace-local/unpinned posture is explicit;
5. plan compiles deterministically;
6. advisor request builds deterministically under fixed budgets;
7. declared capability schemas match the package catalog;
8. no consumer commands or patches were executed.

Overall status:

- `healthy`: a capability contract exists, every declared planning/advisor capability is observable, no declared capability is blocked, and no warning/error finding exists;
- `degraded`: deterministic inspection succeeded but the contract is absent, the pin is absent/unpinned/mismatched, a declared closed-loop capability is `not-observed`, or warning findings exist;
- `blocked`: target/catalog/package compatibility failed, policy/contract is invalid or unsupported, or a declared planning/advisor capability is blocked.

Pin posture is deterministic:

- `released-match`: `engineering_core.ref` exactly equals `v<catalog.version>`;
- `workspace-local-unpinned`: literal `workspace-local-unpinned`;
- `released-mismatch`: a semver tag `vX.Y.Z` different from the catalog version;
- `absent`: no ref;
- `other`: any other non-empty ref.

Only `released-match` is warning-free. The latter four produce warnings, except package `__version__` versus selected catalog version mismatch, which is a blocking error. `--prefer-repo` changes catalog provenance but not this rule.

Doctor is diagnostic. It does not install, repair, invoke a model, execute validation commands, mutate policy, apply patches, create receipts, or claim CI/release/AK/compliance authority.

## Capability scan contract

`engineering-capability-scan-v1` consumes an explicit, deduplicated repository population. Repeated `--repo` and `--repo-file` inputs may be combined; at least one unique repository must resolve. One bad repository produces a failure record and does not abort other repositories. If zero repositories resolve, the command emits a structured scan with zero records and exits 1.

Normative doctor report shape:

```json
{
  "schema": "engineering-doctor-v1",
  "authority": "static diagnostic only; no command execution or authority promotion",
  "repository": "/absolute/path",
  "package_version": "0.6.0",
  "catalog": {"version": "0.6.0", "source": "packaged|repo"},
  "pin_posture": "released-match|workspace-local-unpinned|released-mismatch|absent|other",
  "status": "healthy|degraded|blocked",
  "checks": [{"id": "...", "status": "pass|warn|fail|not-observed", "summary": "...", "evidence": []}],
  "capabilities": {"planning": {}, "advisor": {}, "closed_loop": {}},
  "consumer_commands_executed": false,
  "external_models_invoked": false,
  "mutations_performed": []
}
```

Normative scan shape:

```json
{
  "schema": "engineering-capability-scan-v1",
  "authority": "explicit-population static observations; not rollout closure",
  "population": {"count": 1, "sha256": "...", "repositories": ["/absolute/path"]},
  "completeness": "complete|partial",
  "summary": {"doctor_status_counts": {}, "capabilities": {}},
  "records": [],
  "failures": []
}
```

The population digest is SHA-256 over canonical compact JSON of the sorted unique absolute path strings. Records and findings are sorted by canonical path and check id. Absolute paths are intentionally included because this is an owner-local diagnostic artifact; publication requires owner-side redaction or projection.

`--repo-file` accepts UTF-8 newline-delimited paths, ignores blank lines and lines whose first non-space character is `#`, and resolves relative entries against the repo-file parent. Direct `--repo` paths resolve against the current working directory. Canonical aliases deduplicate after resolution. Repo files must be no-follow regular files, at most 1 MiB, with no NUL/control characters. Inputs are bounded to 1,000 resolved repositories by default and a hard ceiling of 10,000; exhaustion is a structured failure. Symlink/FIFO/device repo files fail closed.

Report fields are required exactly in v1; extra fields are not emitted. Nested schemas are normative:

- A check contains exactly `id`, `status`, `summary`, and `evidence`. `id` is bounded text; `status` is `pass | warn | fail | not-observed`; `summary` is bounded text; `evidence` is a sorted array of bounded text strings.
- A capability result contains exactly `declaration_status`, `observation_status`, `evidence_status`, `schemas`, and `findings`.
- `schemas` is exact by capability: planning has `{"plan": "..."}`; advisor has `{"request": "...", "response": "..."}`; closed loop has `{"receipt": "...", "disposition": "..."}`. Values always contain the expected identifiers from the selected typed catalog, including when declaration is absent, invalid, or unsupported. Supplied invalid identifiers appear only in bounded finding evidence strings, never in `schemas`.
- A finding contains exactly `code`, `severity`, `message`, and `evidence`; severity is `info | warning | error`; evidence is a sorted array of bounded text strings.
- A scan failure contains exactly `path`, `code`, and `message`, all bounded text.
- `records` contains exact `engineering-doctor-v1` objects sorted by repository.
- `summary` contains exactly `doctor_status_counts` and `capabilities`. Doctor counts always contain integer keys `healthy`, `degraded`, and `blocked`. Each capability summary contains exact `declaration_status_counts`, `observation_status_counts`, and `evidence_status_counts`, with every enum key present and a non-negative integer value.
- `population` contains exactly `count`, `sha256`, and `repositories`; repositories are sorted unique absolute path strings.

Every text/evidence/path string is at most 4,096 UTF-8 bytes. A check or capability has at most 100 findings/evidence entries. A doctor has exactly the fixed checks defined by v1 and at most 100 total findings. A scan has at most the configured repository limit plus at most 1,000 failure records; exceeding a bound fails closed rather than truncating silently.

## CLI and exit contract

- `--repo` and `--repo-file` may be combined.
- Argparse syntax errors and missing population arguments use normal stderr and exit 2.
- Successful `doctor` reports `healthy` or `degraded` on stdout and exits 0.
- `doctor` emits a structured `blocked` report on stdout and exits 1.
- `scan-capabilities` emits its structured report on stdout. It exits 0 when at least one repository was inspected, even when `completeness=partial`; automation must inspect completeness. It exits 1 when no repository was inspected or a population input itself is malformed/over-budget.
- Per-repository invalid policy or blocked doctor status remains a record, not a process abort.
- Unexpected internal exceptions remain failures and must not be converted to healthy/degraded reports.

## Safety and authority

- No discovered or declared command is executed.
- No external model is invoked.
- No policy, receipt, disposition, dashboard, AK state, or consumer repository is mutated.
- Advisor output does not affect doctor truth.
- Evidence claims require owner-produced, digest-bound receipts; static observation never substitutes for them.
- Society-wide factual closure requires an owner-approved population, complete scan, repo-local declarations, and AK/owner evidence where canonical tracking is required.

## Compatibility

- `scan-adoption` remains unchanged and continues to report its existing structural taxonomy.
- Existing policies parse without a capability block.
- New commands and schemas are additive.
- Package-visible changes require a version bump and release notes.

## Alternatives rejected

1. **Put society scans in `scripts/`** — rejected because schemas and maturity semantics would drift outside the package.
2. **Execute declared commands in doctor** — rejected as unsafe policy-to-shell coupling.
3. **Infer capability adoption from file names or command strings** — rejected as false evidence.
4. **Make engineering-core own canonical society inventory** — rejected as source-owner drift.
5. **Replace `scan-adoption` immediately** — rejected because it would break existing dashboards and semantics.

## Rollback

The change is additive. Rollback removes the new CLI parsers/modules and optional policy interpretation; existing policies and `scan-adoption` remain valid. Consumer capability blocks become ignored unknown data under the old parser rather than executable behavior.
