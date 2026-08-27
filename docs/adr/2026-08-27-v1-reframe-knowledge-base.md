---
summary: "Reframe engineering-core v1.0 as a curated engineering knowledge base delivered via pi skills and the agent fleet; G3 retired with an honest null."
read_when:
  - "Deciding what engineering-core ships as v1.0, or how its value is delivered and measured."
  - "Consuming the G1-G5 gate lineage after the 2026-08 strategic re-evaluation."
type: "adr"
status: "accepted"
---

# ADR: engineering-core v1.0 — curated knowledge base, delivered

Date: 2026-08-27 · Status: accepted (operator, "yes to all" + strategic
re-evaluation) · Supersedes the release framing implied by the v1 convergence
contract's G3 requirement.

## Context

The v1 program gated release on G1–G5, with G3 (empirical evidence that
guidance improves outcomes) as the value proof. The accumulated evidence:

- G3 campaign (127 pairs, generic tasks): arms identical (0.917/0.917,
  1.0/1.0) — **guidance does not amplify model skill**.
- v3 pilot (contract-conformance tasks): separation 6/10; sol 20%→100% with
  guidance — **guidance is knowledge transfer**: conventions models cannot
  guess.
- v3b (post advise-surface fix): glm's failures recovered when the grammar
  was documented — **delivery form is the mechanism**; small high-signal
  content in context is where value realizes.
- G1 (40/40), G2, G4: the curation, safety, and review machinery all pass —
  and cost roughly an order of magnitude more effort than the delivery layer.
- The successor campaign (N=72, pre-registered) was operator-stopped at 30/72
  before its interim look: no verdict, and resource redirection to this
  reframe. Its partial data (evidence arm ahead on sol, glm mildly reversed)
  is lineage, not a finding.

## Decision

1. **engineering-core 1.0 ships as a curated engineering knowledge base**
   (lanes, disciplines, templates, adoption records) whose primary delivery
   surface is the **pi skill projection** (skills/ec-*, profiles.json) and,
   through it, the **softwareco agent fleet** (standing agents with persona
   system prompts, least-privilege tools, and EC skill profiles).
2. **G3 is retired.** The skill-amplification question it asked was never the
   product claim; the knowledge-transfer claim is demonstrated (v3/v3b,
   diagnostic-grade) and is continuously measured by **production telemetry**
   (AK receipts, adoption scans, agent learnings) rather than synthetic
   campaigns. The G3 record stands as: campaign operator-stopped incomplete
   (null signal, instrument-limited); successor stopped pre-interim
   (non-verdict); question reframed and routed to production telemetry.
3. **Gate lineage:** G0/G1/G2/G4 records remain valid trust evidence for the
   machinery (adoption safety, rollback, review governance). G5's "NOT READY"
   verdict is superseded by this reframe: the release blocker it named (G3
   incomplete) no longer gates, because the claim it gated is withdrawn.
4. **The advise response validator** shrinks to its trust-relevant core
   (patch inertness, citation binding); the response grammar ships as
   documentation (5082), not as a conformance barrier. The CLI adoption
   surface (init/migrate/doctor/scan/rollback/remove) remains the operator
   tooling surface.

## Consequences

- Release = content + curation + projection: the 1.0.0 candidate line may be
  re-frozen from main (candidate-5 lineage) under a scoped release task when
  the operator calls for it; no empirical gate precedes it.
- Value is proven in use: agent-fleet receipts and adoption telemetry replace
  campaigns; KES learnings close the loop back into curation.
- The G4-A/G4-B governance (content review with differentiated dispositions)
  remains the curation quality bar for content changes.

## Non-goals

No claim that EC guidance improves model skill. No re-running of synthetic
lift campaigns. No change to AK/owner authority boundaries.
