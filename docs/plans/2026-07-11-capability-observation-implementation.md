---
summary: "Implementation plan for engineering-core doctor and explicit-population capability scanning."
read_when:
  - "Implementing or verifying the capability observation RFC."
type: "implementation-plan"
---

# Implementation plan — Capability observation and doctor

Controlling design: `docs/rfc/2026-07-11-capability-observation-and-doctor.md`.

## Scope

Deliver a bounded complete first implementation of:

- `engineering-core-capabilities-v1` parsing;
- deterministic capability evaluation;
- `engineering-core doctor --repo`;
- `engineering-core scan-capabilities --repo/--repo-file`;
- reusable public package APIs;
- deterministic dogfood and negative probes;
- docs, tests, version, changelog, catalog protocols, and release verification updates.

Do not implement external model invocation, active command execution, automatic repair, consumer mutation, canonical society inventory ownership, dashboard writes, or AK evidence promotion.

## Work sequence

### 1. Decision and review membrane

- Review the RFC adversarially.
- Revise blocking ambiguity before source changes.
- Record the architecture decision in AK with RFC/review artifacts where the repo workflow supports it.

### 2. Capability contract

Create `src/engineering_core/capabilities.py`:

- immutable typed declaration structures;
- exact version/name/status/schema validation;
- compatibility with policies lacking the block;
- pure evaluation against catalog protocol identifiers;
- independent declaration/observation/evidence dimensions.

Extend `EngineeringPolicy` without changing existing fields or callers.

### 3. Doctor

Create `src/engineering_core/doctor.py`:

- deterministic checks and stable sorting;
- twice-compiled plan/request digest checks;
- explicit pin posture;
- no execution/no mutation proof fields;
- `healthy | degraded | blocked` aggregation;
- caught, typed failures rather than tracebacks.

### 4. Capability scan

Create `src/engineering_core/capability_scan.py`:

- repeated explicit repository paths;
- bounded newline-delimited repository file parsing;
- canonical path normalization and deduplication;
- missing/unreadable path diagnostics;
- stable population digest;
- per-capability proof-tier counts;
- deterministic output independent of input ordering.

### 5. CLI extraction

Create a narrow parser/dispatcher module, likely `capability_cli.py`, so `cli.py` stays below the repository code budget. Add:

```text
engineering-core doctor --repo PATH [--repo-root PATH] [--prefer-repo] [--pretty]
engineering-core scan-capabilities (--repo PATH ... | --repo-file FILE ...) [--repo-root PATH] [--prefer-repo] [--pretty]
```

Both commands emit JSON only in v1. Repeated `--repo` and `--repo-file` forms may be combined. Argparse rejects an invocation with neither form; a structured exit-1 report is emitted when inputs are syntactically valid but zero repositories resolve.

### 6. Unit tests and dogfood

Add `tests/test_capabilities.py`, `tests/test_doctor.py`, and `tests/test_capability_scan.py` for exact parser fields, proof-state transitions, pin postures, report shapes, deterministic aggregation, exit behavior, and malformed inputs.

Add `scripts/dogfood-capabilities.py` using temporary repositories and public APIs. Cover:

- absent declaration;
- valid planning/advisor/closed-loop declarations;
- unsupported contract version;
- unknown capability and wrong schema;
- stable plan and request digests;
- explicit duplicate paths;
- missing repository;
- repo-file comments/blanks;
- repo-file control characters, symlinks, special files where supported, excessive bytes, and excessive items;
- relative repo-file entries resolved against the repo-file parent;
- package/catalog version mismatch and released pin mismatch;
- structured blocked/partial/zero-population outcomes and exit codes;
- declared consumer command sentinel remains unexecuted;
- zero policy, consumer, patch, receipt, or AK mutations;
- byte-identical repeated output.

### 7. Package and release surfaces

- Add typed protocol metadata to `Catalog` rather than reading unchecked raw fields.
- Bump the package and both catalogs for the additive product/schema change.
- Update `CHANGELOG.md`, README, adoption/closed-loop docs, and versioned release notes.
- Add `scripts/dogfood-capabilities.py` to source inclusion and release artifact inspection.
- Keep every code file at or below the default 500 LOC budget by extracting CLI parsing/dispatch.

### 8. Verification and release readiness

Run:

```bash
python -m py_compile src/engineering_core/*.py scripts/*.py
python -m unittest discover -s tests
python scripts/check-justfile-addenda.py
python scripts/dogfood-closed-loop.py
python scripts/dogfood-capabilities.py
uv run engineering-core doctor --repo . --prefer-repo --pretty
uv run engineering-core scan-capabilities --repo . --prefer-repo --pretty
node ~/ai-society/core/agent-scripts/scripts/docs-list.mjs --docs . --strict
uv run engineering-core catalog --pretty --prefer-repo
uv build
```

Also run negative CLI probes and compare repeated output hashes.

## Acceptance criteria

- Architecture review has no unresolved blocker.
- Stable semantics are importable package APIs, not script-only behavior.
- Existing `scan-adoption`, plan, advise, and closed-loop commands remain compatible.
- Policy without capability declarations remains valid.
- Doctor never executes repository commands or invokes external models.
- Capability scan denominator comes only from explicit inputs.
- No static result is labeled unqualified `adopted` or `verified`.
- Outputs are schema-versioned, deterministic, bounded, and authority-qualified.
- All repository validation and dogfood pass.
- Every touched code file remains within the 500 LOC default budget.

## Rollback

Revert the additive command/modules and capability parsing fields. Existing policy and scanner behavior remains unchanged; no consumer migration is required until repositories deliberately add the optional contract.
