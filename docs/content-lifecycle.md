---
summary: "Evidence-backed proposal, pilot, promotion, review, deprecation, and retirement rules for shared engineering content."
read_when:
  - "Proposing or reviewing a lane, discipline, addendum, template, profile, catalog, or doctrine change."
  - "Deciding what evidence, falsification condition, review trigger, or retirement signal a shared rule needs."
type: "reference"
---

# Engineering content lifecycle

Shared engineering content creates second-order effects across repositories and agents. Treat each substantial rule as a revisable decision contract, not as timeless prose or an automatically promoted model recommendation.

This lifecycle applies to lanes, disciplines, conditional addenda, templates, profiles, catalog metadata, and doctrine proposals. More specific documents may add placement or packaging rules.

## Lifecycle stages

These stages are governance language, not new machine states in the catalog schema:

1. **Proposal** — an unapplied candidate with a named problem, scope, alternatives, and owner decision still pending.
2. **Pilot** — bounded guidance used in explicitly selected repositories or workflows to gather evidence.
3. **Stable** — versioned shared guidance whose applicability, evidence, counterexamples, and compatibility implications are understood well enough for ordinary adoption.
4. **Deprecated** — retained for compatibility while a replacement or migration path is active.
5. **Retired** — no longer selected or recommended; historical references remain interpretable when practical.

No CI run, agent recommendation, ontology definition, evidence-store record, or generated proposal promotes a stage automatically. Promotion and retirement remain owner decisions.

## Minimum decision record

A substantial proposal should make these fields reviewable even when they remain in Markdown rather than a new schema:

- **problem:** the repeated risk, inconsistency, or decision cost;
- **audience and scope:** affected repo shapes, lanes, disciplines, and explicit non-goals;
- **invariant or decision rule:** what should remain true without binding every consumer to one tool;
- **load triggers:** when an agent or maintainer should retrieve the guidance;
- **evidence references:** observations, incidents, measurements, receipts, or artifacts and their provenance;
- **strongest alternative:** the best competing rule or decision to remain repo-local;
- **counterevidence and exceptions:** known situations where the proposal performs worse or does not apply;
- **falsification conditions:** observable results that would weaken, revise, split, or reject the rule;
- **adoption and compatibility:** migration, catalog/schema impact, rollback, and consumer cost;
- **review trigger:** date, ecosystem event, incident threshold, or evidence volume that causes re-evaluation;
- **retirement signal:** conditions under which the guidance should be deprecated, merged, or removed;
- **semantic references:** stable ontology IDs when a term already has a shared canonical meaning.

AI-generated analysis may help assemble this record, but model confidence, repetition, or rhetorical quality is not evidence.

## Evidence quality and storage

Prefer evidence that is bounded, attributable, reproducible where possible, and connected to the exact claim being made. Distinguish:

- direct observation from inference;
- execution evidence from transition receipts;
- one-repository experience from recurring cross-repository evidence;
- absence of a reported failure from evidence of safety or effectiveness;
- conformance to a source/schema contract from semantic correctness or adoption.

In the AI Society environment, agent-kernel may persist live evidence rows, governance receipts, decisions, artifact references, and lineage. Shared engineering content should normally reference those records by stable ID and digest rather than copy private payloads into this repository.

A useful external evidence reference includes the producer/schema, stable evidence or receipt ID, subject and revision, digest, capture time, scope, and authority ceiling. Public contributors without agent-kernel may provide equivalent digest-bound local artifacts. AK integration is optional; evidence quality and authority rules are not.

See `docs/evidence-semantics-boundaries.md` for the storage and authority split.

## Promotion gates

### Proposal to pilot

Start a pilot only when:

- the problem and bounded audience are clear;
- the proposal is reversible and does not silently become a default;
- the strongest alternative and obvious counterexamples are recorded;
- success, harm, and falsification observations can be collected;
- an owner and review trigger are named.

A pilot should have an expiry or explicit review event. An expired pilot remains a proposal, not an implicit stable rule.

### Pilot to stable

Promote only when:

- evidence comes from more than one repository, lane, or meaningfully independent context unless the risk justifies a narrower emergency rule;
- the evidence supports the invariant rather than merely one implementation recipe;
- known counterevidence and exceptions are represented in applicability or non-goals;
- load triggers are selective enough to avoid unnecessary agent context;
- compatibility, migration, and rollback effects are understood;
- the rule has a review trigger and retirement signal;
- any cross-system term reference points to an accepted ontology definition rather than a local guess.

For an emergency security or data-loss rule, bounded precautionary guidance may precede broad evidence. Label the uncertainty, keep scope narrow, and schedule review after operational evidence exists.

## Falsification and revalidation

A rule is not falsifiable merely because reviewers can disagree with it. Name observable conditions, for example:

- the expected failure class does not decrease across representative adopters;
- false positives or maintenance cost exceed a stated threshold;
- consumers repeatedly need the same exception;
- a new platform/runtime invalidates a required assumption;
- an alternative produces equal or better outcomes with lower complexity;
- evidence cannot be reproduced or is later shown to be misclassified;
- the load trigger retrieves the guidance for mostly irrelevant repositories.

Revalidation may confirm, narrow, split, downgrade to a pilot, deprecate, or retire guidance. Preserve the decision and evidence lineage; do not rewrite old evidence to look current.

## Deprecation and retirement

Deprecate, merge, or retire guidance when:

- its trigger is indistinguishable from another rule;
- it has no active consumers and no credible near-term need;
- repeated exceptions show that its scope is wrong;
- counterevidence outweighs the supporting evidence;
- the underlying platform, threat, or workflow no longer exists;
- a replacement provides a clearer invariant or lower adoption cost;
- the rule has become implementation history rather than current guidance.

Retirement is a compatibility event when consumers reference a public ID, schema, command, or packaged file. Preserve a replacement/migration path and release-note entry where needed. A stored AK record or historical ontology reference remains evidence of what was decided or observed; it does not keep retired guidance current.

## Shared semantics

Keep protocol-specific states and reason codes in their owning versioned schemas. Promote terminology to ontology-kernel only after it is used across independent systems and one canonical meaning reduces real ambiguity. Use rocs-cli to validate and resolve accepted ontology material; do not treat ROCS conformance as proof that the content should be promoted.

## Review checklist

Before accepting a substantial shared-content change, verify:

- placement and authority are correct;
- evidence and counterevidence are distinguishable and attributable;
- private payloads are referenced rather than copied;
- falsification and review conditions are observable;
- pilot scope or stable promotion criteria are explicit;
- compatibility and rollback effects are understood;
- retirement can occur without erasing historical evidence;
- ontology references are accepted IDs rather than invented labels;
- no tool output promotes itself into owner authority.
