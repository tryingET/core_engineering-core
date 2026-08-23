---
summary: "Current-track R3 review memo for Decision 128: most R2 blockers closed, but authority-graph and operator-oracle defects require R4."
read_when:
  - "Inspecting the historical R3 review attempt for Decision 128."
  - "Checking why revision 4 was required before ADR readiness."
type: "review_memo"
task_id: 4907
decision_id: 128
artifact_kind: "review_memo"
reviewed_artifact_ref: "docs/rfc/2026-08-23-v1-convergence-contract-r3.md"
reviewed_sha256: "eb7279ca3d844baefa1f1377a63f124b36379c57c975412a6fca1cf455635ed7"
track_id: "current_track"
review_outcome: "revise_rfc"
---

# Review Memo — engineering-core v1.0 convergence revision 3

## Review chain status

```text
review_kind = re-review after revise_rfc
reviewed_artifact = docs/rfc/2026-08-23-v1-convergence-contract-r3.md
reviewed_SHA256 = eb7279ca3d844baefa1f1377a63f124b36379c57c975412a6fca1cf455635ed7
review_outcome = revise_rfc
legal_next_move = produce_r4_and_fresh_review_set
ADR_legal_from_this_attempt = false
implementation_authorized = false
```

All lanes confirmed the digest and made no mutation.

## Lane dispositions

| Lane | Continuation evidence | Outcome | Controlling result |
|---|---|---|---|
| Semver/public constitution | `dispatch-1787524357077` | `revise_rfc` | All prior blockers closed; new G0 authority deadlock blocks candidate creation. |
| Protocol/adversarial federation | `dispatch-1787524357079` | `ready_for_adr` | All negotiation, adapter, parser, downgrade, threat, and transfer findings closed. |
| Operator/rendered product | `dispatch-1787524357081` | `revise_rfc` | Installed-artifact execution, malformed-input minima, and non-vacuous mixed-ownership coverage remain open. |
| Prospective empirical validity | `dispatch-1787524357083` | `ready_for_adr` | Every prior G3 blocker closed; only protocol-level refinements remain. |
| Federated governance/legality | `dispatch-1787524357085` | `ready_for_adr`; ADR legal now: no | R2 findings closed and G4 remains non-coercive; Git/AK artifacts are not yet attached. |

## R2 findings closed by R3

R3 correctly repaired:

- G4-A→G0-B manifest timing and assertion-backed v1/v1.x baselines;
- qualification-population layering and manifest-derived G1 denominator;
- fair strongest-alternative treatment;
- complete-offer negotiation, security floor, replay defense, adapter loss/status/lineage;
- parser acceptance guarantees versus qualification budgets and valid-v1 downgrade protection;
- candidate-bound public procedures, plan binding, owner exit, clean-transition and every-boundary recovery direction;
- sole-treatment empirical arms, owner-normalized weights, common model set, multiplicity, forecast provenance, and pessimistic harm missingness; and
- named transfer/custody references and non-coercive G4.

## Remaining RFC blockers

1. **Authority deadlock:** G0-A1 releases only protocol/harness authoring and G0-A2 only G4-A pilots, while G0-B presupposes convergence implementation and candidate preparation. Add an explicit task-release checkpoint with dependencies, permitted effects, and stop boundary.
2. **Installed rendering proxy:** “wheel/sdist parity” could remain archive comparison. Require installation of the exact wheel into an empty environment and execution from an exact extracted sdist through documented workflows.
3. **Malformed-input regression:** restore constitutional minimum boundaries for malformed pin, unavailable pin, and malformed policy; qualification protocols may tighten but not weaken them.
4. **Mixed-ownership vacuity:** require a non-empty coverage map whenever owner-writable files exist, including applicable structured/textual patterns or independently reviewed `not_applicable` entries.
5. **Resolution scope:** define the one-active-v1 invariant per manifest-declared adoption/resolution scope so legitimate monorepo package scopes are not centralized.

## Outcome

Model A remains viable; rejection is unsupported. The findings are contract defects, not missing future implementation, so this digest cannot control ADR readiness.

```text
review_outcome = revise_rfc
next_legal_move = create docs/rfc/2026-08-23-v1-convergence-contract-r4.md
```
