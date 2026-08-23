---
summary: "Bounded R4 review-set plan for Decision 128 after R3 closed broad issues but exposed five final contract defects."
read_when:
  - "Reviewing revision 4 of the v1 convergence RFC."
  - "Checking final substantive closure before ADR progression."
type: "review_set_plan"
task_id: 4907
decision_id: 128
artifact_kind: "review_set_plan"
rfc_ref: "docs/rfc/2026-08-23-v1-convergence-contract-r4.md"
rfc_sha256: "dfaf60c826ca1eec475a848b7b8ff7a81344f6c13251b7c81179e6f53096b5d1"
---

# Review Set Plan — engineering-core v1.0 convergence revision 4

## Status

```text
review_kind = re-review after revise_rfc
reviewed_artifact = docs/rfc/2026-08-23-v1-convergence-contract-r4.md
reviewed_SHA256 = dfaf60c826ca1eec475a848b7b8ff7a81344f6c13251b7c81179e6f53096b5d1
outer_host = pi_sdk
AK_active_track = current_track
review_closure_mode = multi_lane_requires_synthesis
intended_effect = closure_candidate
```

R4 is a bounded correction after R3. It authorizes no implementation, owner work, decision acceptance,
ADR, candidate, or release. Any RFC-byte change invalidates this plan's review result.

## Inputs

- exact R4 artifact above;
- problem/evidence notes and product posture/support policy;
- immutable R2 and R3 plans, memos, and syntheses;
- AK task `4907`, decision `128`, direction `AK.V5.SF01`;
- governance-kernel decision lifecycle and review-synthesis v6 contract.

## R3 findings R4 must close

1. Add a lawful post-G0-A2/G4-A convergence-implementation and candidate-preparation admission path,
   including exact tasks, dependency fan-in, permitted effects, failure boundaries, and no release power.
2. Require execution of every candidate-bound rendering assertion from the exact installed wheel and
   exact extracted sdist, not archive/member parity.
3. Restore fail-before-effect minima for malformed pins, unavailable well-formed pins, and malformed
   policy; test interruption at every durable mutation boundary or prove transaction atomicity.
4. Require non-empty mixed-ownership coverage whenever owner-writable files are touched, spanning
   every applicable structured/textual pattern or independently reviewed non-applicability.
5. Scope the one-active-v1/no-mixed-runtime invariant per manifest-declared adoption/resolution scope.

## Review lanes

All lanes confirm the exact digest and inspect for regressions as well as their primary seam.

1. **Semver/authority graph:** validate G0-A1→A2→A3→B task release, manifest timing, public stability,
   population layering, alternatives, candidate/release separation.
2. **Protocol/federation:** recheck complete offers, security floors, adapter loss, parser guarantees,
   downgrade rules, threat coverage, and ensure G0-A3 creates no protocol bypass.
3. **Operator/rendering:** validate exact artifact execution, candidate-digest runbooks, malformed-input
   boundaries, every-boundary recovery, ownership-map coverage, removal/exit, and scoped resolution.
4. **Empirical validity:** ensure G0-A3 and R4 edits do not weaken sole treatment, owner weighting,
   common models, multiplicity, forecast provenance, harm missingness, or protocol freeze.
5. **Governance/legality:** validate exact-task authority, G4 non-coercion, population decisions,
   immutable revision lineage, current AK/task/direction state, and steps remaining for legal closure.

## Outcome rule

The designated synthesizer emits exactly one:

- `ready_for_adr` when all R3 findings close and no new review-level blocker exists;
- `revise_rfc` for any remaining byte-level defect; or
- `reject_current_direction` if Model A should stop.

No vote or average controls. A supported authority, security, operator-safety, empirical-validity, or
compatibility contradiction controls. Missing downstream implementation is not an RFC blocker when
an explicit task/gate fails closed on its absence.

## Canonical outputs

- `docs/project/2026-08-23-v1-convergence-review-memo-r4.md`
- `docs/project/2026-08-23-v1-convergence-review-synthesis-r4.md`

The plan is attached before synthesis. Both output refs are fresh/single-use. Only the synthesis may
control ADR legality under `multi_lane_requires_synthesis`.

## Completion conditions

- five immutable lane results cover all R3 findings;
- the memo separates substantive quality from AK legality;
- the synthesis names one outcome and exact legal next move;
- final commit/RFC digest is carried in AK attachment evidence; and
- the passport exposes one controlling closure without session inference.
