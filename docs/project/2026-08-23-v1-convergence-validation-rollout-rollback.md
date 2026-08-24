---
summary: "Validation, rollout, and rollback projections for the accepted engineering-core v1.0 convergence contract; binds each convergence stage to executable checks and stop behavior."
read_when:
  - "Validating any v1.0 convergence task before completion or claiming a gate result."
  - "Deciding release-window, post-release verification, rollback, or stop behavior for v1.0."
type: "plan"
---

# Validation, rollout, and rollback — engineering-core v1.0 convergence

## Authority

- Decision: AK `128`, accepted; ADR `docs/adr/2026-08-23-v1-convergence-contract.md`.
- Contract of record: `docs/rfc/2026-08-23-v1-convergence-contract-r5.md`
  (SHA-256 `d8a17d69b12d9235de75e123acb28362876f0062d504ac45d991cec15736b5e4`).
- Execution binding: `docs/project/2026-08-23-v1-convergence-implementation-plan.md`.

## Validation contract

### Repository validation (every convergence task, before completion)

From the repository root:

```bash
UV_NO_CONFIG=1 uv sync --locked
UV_NO_CONFIG=1 uv run python -m unittest discover -s tests -v
UV_NO_CONFIG=1 uv run python -m engineering_core.self_check --repo-root .
UV_NO_CONFIG=1 uv run python scripts/check-release-lineage.py --mode ci
UV_NO_CONFIG=1 uv run python scripts/check-justfile-addenda.py
UV_NO_CONFIG=1 uv run python scripts/sync-skill-assets.py --check
UV_NO_CONFIG=1 uv run engineering-core scan-adoption --scope . --include-scope-root \
  --format json --prefer-repo --max-repositories 10
UV_NO_CONFIG=1 uv build
```

`UV_NO_CONFIG=1` isolates validation from the workstation's global uv `exclude-newer`
configuration; plain `uv sync --locked` failing under that external configuration is a
disclosed non-blocking environment observation, not repository drift.

Tasks touching release-affecting surfaces additionally run
`uv run python scripts/release-local.py verify` (deterministic dogfood harnesses, complete
unit suite, CLI checks, artifact inspection).

### Per-gate validation (authoring tasks 4871–4875)

Each authoring task must land, before completion:

- its frozen protocol/plan document under `docs/plans/`;
- its deterministic script and tests under `scripts/v1/` and `tests/`, with negative
  fixtures proving fail-closed behavior (missing/unknown input, drift, nonzero exit);
- two-run byte-identical determinism evidence for deterministic payloads;
- template/oracle digests recorded candidate-independent where the RFC requires G0-A2
  freezing before G0-B binding; and
- the full repository validation block above.

A task whose tests pass only by weakening an RFC rule (for example, fabricating a
candidate-dependent expected result at authoring time) fails validation.

### Per-gate validation (admission and beyond)

- **G0-A2:** population manifest canonical digest (RFC 8785) plus raw digest/length;
  participant owner acceptances; frozen impact matrix; gate-conformance source inside the
  reviewed tree. Machine-decidable envelope schemas validated by tests.
- **G0-A3:** read-only verifier emits the candidate-admission record; any missing, stale,
  extra, or changed input blocks admission.
- **G0-B / 4876:** exact candidate on a non-`main` branch; manifest materialization against
  the exact candidate; new checkout without `dist/` passing locked sync, release
  verification, exact-wheel install into an empty environment, exact-sdist workflow,
  rendered/conformance assertions, clean index, effect inventory; fail-closed
  `pre-publish` mode invoked by the workflow; remote tag/Release absent.
- **G1–G4:** the RFC's exact pass thresholds (10×N journeys; 100% of the frozen corpus and
  entrypoint matrix; prospective G3 protocol rules; live G4 cycles plus deterministic
  transition suite). Independent review per gate; producer never sole reviewer.
- **G5 / 4877:** two standalone checkouts reproduce byte-identical wheel/sdist/SHA256SUMS;
  candidate-contained `readiness` mode verifies digests and returns `pass`.

### Evidence recording

Each task records validation evidence through AK (`ak task contract` / evidence refs)
before completion, including the result commit SHA. Narrative cannot override a failed
machine-decidable payload.

## Rollout

The contract defines rollout as a strictly post-G5, separately authorized sequence.
Convergence execution itself performs no participant rollout.

Release states (exact, serialized):

1. `candidate` — G0-B commit exists; unsupported as a proof channel until tag+Release.
2. `release-blocked` — main updated or no tag; window stops.
3. `tag-created-release-absent` — lineage point of no return.
4. `published-verification-pending` — tag/Release exist; dependent verification running.
5. `published-and-verified` — only after the post-release task downloads into an empty
   directory, admits only approved wheel/sdist/checksums, and byte-compares them.

Rules: only the approved exact-SHA fast-forward is allowed; candidate head, triggering CI
head, current remote main, release build SHA, and peeled tag target must be equal at
mutation; `pre-publish` runs immediately before tag/upload; mismatch blocks; a public tag
is never retargeted or reused; downstream rollout remains owner-authorized.

## Rollback

- **Rejection/failed proof:** `v0.10.0` remains current; lineage preserved or defer-closed.
  A failed pre-release candidate stays isolated; fixes create a new candidate plus
  impact-matrix reruns.
- **G1:** restore or quarantine the disposable replica; never pretend Git reverses
  external effects. No fabricated or partial state, helpers, or processes survive.
- **G2:** withhold the aggregate path without touching owner records.
- **G3:** failure leaves evidence advice experimental; the empirical protocol decision and
  negative results remain in lineage; no optional stopping or post-hoc relabeling.
- **G4:** evidence-supported dispositions are preserved; rollback drills restore the exact
  prior stable selection without erasing proposal, evidence, decision, or failure history.
- **Population change:** participant withdrawal requires a fresh accepted
  qualification-population decision; population-dependent evidence restarts.
- **Post-tag failure:** preserve the reached state and lineage, stop rollout, quarantine
  affected copies, and require an explicit corrective/completion/withdrawal decision.

## Stop rules (immediate, any stage)

Stop work immediately on: disclosure; unauthorized transfer, execution, or egress;
permission bypass; path escape; fabrication; substitution; failed deadman; surviving
process; undeclared effect; authority promotion; task drift; or unbound proof. Owner-led
incident response then records blast radius, notification/rotation/deletion,
quarantine/invalidation, restoration, root cause, protocol correction, reruns, and
independent closure. Irrecoverable transferred bytes are never called rolled back.

## Completion discipline

- Gate outcomes are recorded only through the gate's machine-decidable envelope, never
  through narrative or task notes.
- `ak task close-check` must be ready before completing any convergence task.
- No participant repository is mutated without its own exact AK task, local instructions,
  validation contract, and landing decision.
- Direction health (`ak direction check`) is re-verified after decision/task state changes.
