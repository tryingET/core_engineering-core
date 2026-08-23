---
summary: "Evidence for revising Decision 128 around the pre-v1 break, v1 stability boundary, executable journeys, empirical validity, and owner autonomy."
read_when:
  - "Reviewing the Decision 128 revision chain or current ADR readiness."
  - "Checking which findings are observed versus proposed."
type: "evidence_note"
decision_id: 128
task_id: 4907
---

# Evidence Note — engineering-core v1.0 convergence revision chain

## Status

This is the Tier 1 evidence note for decision `128`. It records bounded observations and review
findings; it is not an ADR, implementation proof, G0–G5 PASS, or release authority.

## Artifact baseline

```text
historical RFC commit = 27c3e2ba1aba0f28598ae61e1f8d454dcad170f1
historical RFC SHA-256 = 10b6ba7f9dbc7eea03aaf48785fc790c514197f1b69fe7947483d2230c0b5661
R2 RFC/SHA-256 = docs/rfc/2026-08-23-v1-convergence-contract-r2.md / 93f6060d6fab2af7b0b39b4dd0d998592ce0c9a7610f7b42b701f396986c24a5
R3 RFC/SHA-256 = docs/rfc/2026-08-23-v1-convergence-contract-r3.md / eb7279ca3d844baefa1f1377a63f124b36379c57c975412a6fca1cf455635ed7
R4 RFC/SHA-256 = docs/rfc/2026-08-23-v1-convergence-contract-r4.md / dfaf60c826ca1eec475a848b7b8ff7a81344f6c13251b7c81179e6f53096b5d1
R5 RFC/SHA-256 = docs/rfc/2026-08-23-v1-convergence-contract-r5.md / d8a17d69b12d9235de75e123acb28362876f0062d504ac45d991cec15736b5e4
```

Each digest is immutable. R2–R4 produced `revise_rfc`; R5 has a fresh plan. Any R5-byte change requires another attempt.

## Observed evidence

### 1. The historical RFC mixed a clean v1 decision with pre-v1 compatibility obligations

The historical artifact required:

- upgrades from recorded v0 pins in G1;
- v0.7.0, v0.8.0, and v0.10.0 released inputs in G2 without support classification; and
- compatible behavior or migration/downgrade for an “older supported consumer” in G4.

The current support policy, by contrast, supports only latest stable/current main for fixes. The
operator has now explicitly removed any v0-to-v1 compatibility requirement.

### 2. Package semver cannot reset protocol identity

The pre-v1 product already exposes identifiers including `engineering-plan-v1`,
`engineering-capability-scan-v1`, and multiple `engineering-*-v1` evidence/work schemas in source,
catalog, README, and documentation. The support policy states that meaning remains compatible
within a versioned protocol identifier.

Therefore a package `1.0.0` clean break may change package surfaces, but a retained protocol ID must
keep its meaning or be replaced by a new identifier. Release number and protocol epoch are distinct.

### 3. Rendered operator behavior is a current proof gap

`src/engineering_core/templates/engineering.local.template.md` currently presents v0.9.0 retrieval
and includes a machine-local self-development checkout path. That is truthful for current
self-development but demonstrates why a source-only reference check cannot prove candidate-installed
rendering. The revised contract requires candidate-bound source/root parity plus execution from an exact installed wheel and exact extracted sdist before G0-B/G5.

This evidence does not claim the future validator or corrected candidate exists.

### 4. The first RFC's numeric proof rules lacked decision evidence

The historical G3 fixed effect, interval, Brier, ECE, harm-stop, cluster, and per-cell values without
a cited pilot distribution, power result, target-population justification, or forecast provenance.
It also weighted four participant baselines rather than three owner groups, giving TeachingCo two
baseline cells. Historical G2 resource limits likewise lacked a recorded supported-platform baseline.

The product posture intentionally leaves exact thresholds to a predeclared owning decision surface.
R2 introduced prospective protocol ownership. Its review then required R3 to add sole-treatment arms, owner-normalized weights, multiplicity, and pessimistic harm-missingness.

### 5. Predetermined live governance outcomes create incentive pressure

Historical G4 required the live candidate set to contain a promotion, separate rejection/retirement,
material revision, and rollback while saying outcomes were not coerced. Formal owner authority was
preserved, but v1 remained contingent on producing that result distribution.

R2–R4 separate:

- live owner cycles judged only against frozen evidence criteria; and
- deterministic fixtures/replays proving every lifecycle transition and invalid path.

Rollback remains a mandatory reversibility drill. No live owner must manufacture a substantive result.

### 6. AK lifecycle evidence is currently incomplete

Before this revision cycle, `ak decision passport 128 -F json` reported:

```text
state = review_pending
review_outcome = null
legal_review_closure = null
adr_ref = null
missing current_track, problem_brief, evidence_note, review_memo, review_synthesis
```

The old repository synthesis was conditional decision support and was never attached as legal AK
closure. Each revised RFC therefore needs a fresh plan, memo, and controlling synthesis rather than retroactive promotion.

## Multi-review convergence

Independent read-only review roles covered semver/release contracts, protocol evolution/security,
operator resilience, prospective causal inference, and institutional mechanism design. They agreed
that removing pre-v1 compatibility materially simplifies G1/G2/G4, but does not remove the need for:

- stable v1/v1.x semantics;
- explicit protocol epochs and adapter boundaries;
- public transition/rollback/rendering oracles;
- justified G3 design; or
- non-coercive G4 and lawful AK closure.

Lane execution is supporting evidence only. The canonical outcome comes from the fresh review memo
and controlling synthesis attached to decision `128`.

R2 lanes unanimously returned `revise_rfc`. R3 closed those findings but exposed authority/operator gaps. R4 closed those; four lanes returned `ready_for_adr`, while protocol review required immutable source-transition admission for G0-A3. R5 binds the exact base tree, reviewed outputs, frozen inputs, task/allowlists, and permitted diff before candidate preparation, then requires G0-B verification. All five R5 lanes returned `ready_for_adr`; the R5 memo and controlling synthesis preserve that disposition while leaving decision acceptance and ADR recording to AK/operator authority.

## Evidence limits

- No v1 compatibility manifest, adapter, public transition command, empirical protocol, lifecycle
  conformance suite, candidate, or release currently exists.
- Participant and empirical owners have not accepted downstream tasks through this note.
- Current source observations establish review targets, not future PASS claims.
- Decision acceptance remains an operator/AK action after legal review closure.
