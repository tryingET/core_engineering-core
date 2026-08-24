---
summary: "G1 dependable-adoption proof protocol and deterministic manifest/envelope harness for engineering-core v1.0 convergence."
read_when:
  - "Executing, reviewing, or validating Gate G1 adoption-journey proof under decision 128."
  - "Authoring or binding a G1 journey manifest, result envelope, or negative-control record."
type: "implementation-plan"
---

# G1 dependable-adoption proof protocol

Controlling contract: `docs/rfc/2026-08-23-v1-convergence-contract-r5.md` (Gate G1),
accepted as `docs/adr/2026-08-23-v1-convergence-contract.md`.
Harness: `scripts/v1/dependable_adoption.py` (internal qualification tooling; not a
public package surface). Tests: `tests/test_v1_dependable_adoption.py`.

## Authority boundaries

- This protocol is **candidate-independent** at G0-A2: every template emitted by the
  harness leaves candidate identity, expected candidate-bound bytes, and per-baseline
  runbook digests `unassigned`. They bind only at G0-B against the exact candidate.
- The harness validates manifests and envelopes. It never invokes participant commands,
  never resolves remotes, and never mutates any repository. Journey execution belongs to
  each baseline owner inside its own disposable replica under its own AK task.
- Engineering-core is producer/validator only; it cannot be a positive adopter.

## Ten frozen journey categories

Each positive baseline executes all ten through candidate-shipped commands or
rendered-manifest path/digest runbooks; the harness only freezes and checks the record:

| # | Category (frozen key) | Boundary proven by the frozen assertions |
|---|---|---|
| 1 | `resolve_install_remote` | immutable remote resolution; zero local `git+file`/workspace-checkout fallback |
| 2 | `retrieve_explain_guidance` | guidance, dependencies, omissions, pilots, local deviations, stability class, pre-v1 break shown without hidden workspace context |
| 3 | `plan_transition_mode` | `clean_adopt`/`clean_transition`/shipped `migration` selection; plan/diff, preserved local truth, backup, recovery, removal effects |
| 4 | `apply_owner_plan` | plan-digest-bound apply; drift rejection; atomic completion or documented recovery; no accepted partial state |
| 5 | `diagnose_v1_adoption` | diagnosis/scanning without executing undeclared commands, URLs, models, observations, patches |
| 6 | `prove_active_resolution` | per declared scope: one active v1 resolution, zero active pre-v1/mixed runtime, preserved owner truth; idempotence for clean-slate |
| 7 | `failure_boundaries` | malformed pin fails before DNS/network/helpers/import/build/mutation; unavailable well-formed pin contacts only the approved credentialless fixture remote; malformed policy fails before consumer command; interruption at every durable mutation boundary or proven transactional atomicity |
| 8 | `rollback_recovery` | public rollback from post-apply checkpoint restores exact starting posture; Git/filesystem comparison as independent oracle |
| 9 | `removal_with_owner_edits` | frozen owner edits on mixed-ownership cases; plan-bound removal or structured refusal; validation without engineering-core; zero classified pins/selections/surfaces left; no no-op success |
| 10 | `final_posture_disposal` | restore predeclared proof-workspace posture; validate; inventory residual state; dispose/quarantine replica |

## Journey manifest (per baseline)

A journey manifest binds, before the first run: baseline identity (owner group, physical
repository identity, full pinned revision, role), the ten category entries each carrying
frozen assertion names/expected classes, starting/ending checkpoints, candidate argv or
runbook digest (`unassigned` until G0-B), environment/network/timeout policy, effects
declaration (Git/index/untracked/ignored, process, cache, credential, config, temp),
declared validation commands, mixed-ownership map when owner-writable files are touched,
and recovery plan. The harness `validate` mode fails closed on:

- unknown or missing category; missing/empty required field;
- any candidate-identity field assigned at protocol stage;
- any local-checkout or `git+file` fallback declared anywhere;
- any negative-control entry declaring mutation, execution, or non-identical pre/post
  receipts;
- manifest template-digest mismatch;
- population shape violation: fewer than four positive baselines or a missing negative
  control; duplicate physical repository identities.

## Result envelopes (machine-decidable)

`envelope` mode accepts one completed journey record and emits/validates an envelope with
schema `engineering-core.v1.g1.journey-envelope/1`: status
(`pass|fail|blocked|incomplete`), per-assertion `expected/observed/required` triples,
declared before/after effects and undeclared-residual findings, digests (journey manifest;
candidate `unassigned` until G0-B), owner/task binding, and independent-review record.
Narrative fields cannot set or rescue a status: `pass` requires every required assertion
observed==expected, zero undeclared residuals, and an independent (non-producer) reviewer.
`incomplete`/`blocked` require explicit missingness reasons. Failures, interruptions, and
refusals stay first-class records.

## Exact pass threshold (frozen)

G1 passes only when validated envelopes show: **10 × N of 10 × N** journeys passed for the
accepted manifest denominator `N` (≥4 positive baselines across ≥3 independent owner
groups); **100%** of negative-control commands returning the frozen missing/absent schema
result with byte-identical pre/post receipts; **100%** of the frozen failure-boundary
probes failing at their distinct boundary before prohibited effects; every declared
validation green; remote-source portability for every positive baseline; and zero
authority-loss events, silent deviation losses, undeclared residuals, or synthetic-secret
disclosures. Timings and commentary remain descriptive only.

## Determinism and custody

Template and validation outputs are canonical JSON (sorted keys, compact separators) with
no wall-clock content; two runs are byte-identical. Timestamped receipts live outside the
deterministic payload. Evidence transfers follow the RFC default-deny rule; raw snapshots
stay owner-local.

## Rollback

This additive protocol/harness can be withdrawn without touching the accepted RFC or any
owner record. A protocol change restarts affected journey evidence under the frozen impact
matrix.
