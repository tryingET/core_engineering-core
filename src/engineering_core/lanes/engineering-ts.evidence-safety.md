---
summary: "Opt-in TypeScript evidence-safety contract and staged anti-slop-inspired rule pilot."
read_when:
  - "A high-assurance TypeScript repo is reducing unsafe evidence loss or assertion laundering."
  - "A repo is piloting selected anti-slop-inspired Oxlint rules with measured diagnostics."
type: "guide"
status: "pilot"
---

# TypeScript lane — evidence-safety addendum

This addendum is opt-in and evidence-gated. It captures a portable invariant inspired by anti-slop-style rules without declaring every upstream opinion universally applicable.

Use it with `ts`, `validation`, `testing`, `security-privacy`, `dependency-governance`, and `specification-and-dsls`.

## Core invariant

> Preserve known type evidence, parse uncertainty at system boundaries, and localize every unavoidable escape with a checked, reviewable invariant.

The goal is not to maximize rule count. The goal is to prevent flows that discard evidence and later manufacture it back through assertions, broad contracts, reflection, or ad hoc narrowing.

## Strong initial pilot candidates

Start with rules whose failure mode is specific and whose remediation normally improves the contract:

- chained type assertions;
- widening a known value and later asserting it back;
- explicit broad target types that discard known literal/key evidence;
- dictionary value contracts based on `any`, `unknown`, `object`, or `{}` when a real value contract is available;
- non-const type assertions without a nearby `SAFETY:` explanation of the checked invariant.

A `SAFETY:` comment is evidence, not a waiver. It should identify the parser, constructor, ownership rule, exhaustive condition, or other fact that makes the assertion valid.

## Conditional candidates

Pilot these only when the repository architecture supports the opinion and measure the exceptions:

- banning module mocks in favor of real dependency seams;
- rejecting ad hoc runtime `typeof` checks outside dedicated boundary guards;
- restricting `unknown` parameters, returns, or aliases;
- restricting `Reflect.get` and `Reflect.apply`;
- requiring narrower dictionary and object-parameter contracts.

These can be valuable in a high-assurance service or library and counterproductive at genuine untyped boundaries. Do not launder types or add meaningless wrappers merely to satisfy a rule.

## Keep repo-local until repeated evidence exists

Naming preferences and other low-risk style opinions should remain repo-local unless multiple repositories demonstrate a recurring defect they prevent. A rule such as banning `shape` in symbol names is not a cross-repository safety invariant by itself.

## Vendoring and provenance

When the rule implementation is vendored:

- record the upstream repository and exact tag or commit;
- record the local destination and owner;
- keep local modifications explicit;
- exclude the vendored implementation from application linting when appropriate;
- retain focused rule tests;
- compare upstream changes before replacing a local copy.

Do not silently treat a mutable upstream branch as the runtime authority for every repository.

## Rollout

1. Run read-only diagnostics and capture a baseline.
2. Classify findings by rule, code ownership, true defect, false positive, and remediation effort.
3. Enable only the high-signal subset for changed files or one owned slice.
4. Require tests and type checking after every remediation.
5. Ratchet new findings before attempting whole-repository cleanup.
6. Record necessary deviations with reason, owner, evidence, and review date.
7. Promote a rule only after representative repositories show low ambiguity and durable defect prevention.

## Failure modes to reject

- weakening types or inserting double assertions to make the linter pass;
- moving uncertainty into aliases without parsing it;
- replacing real tests with comments;
- banning valid boundary code without an explicit guarded exception;
- enabling every upstream rule at error severity before measuring the repository;
- claiming safety improvement from diagnostic count alone.
