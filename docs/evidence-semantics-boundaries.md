---
summary: "Responsibility boundaries between engineering-core, agent-kernel, ontology-kernel, rocs-cli, and owner authority."
read_when:
  - "Designing evidence persistence, shared terminology, ontology references, or agent-runtime integration."
  - "Deciding whether a state or term belongs in an engineering-core schema or the shared ontology."
type: "reference"
---

# Evidence, semantics, and runtime authority

Engineering-core participates in a larger local-first toolchain, but it must remain usable as a standalone public package. Integration should connect distinct authorities rather than make several repositories claim the same truth.

## Responsibility map

| Concern | Primary owner | Contract boundary |
|---|---|---|
| Shared engineering lanes, disciplines, content lifecycle, and engineering-specific JSON protocols | `core/engineering-core` | Defines and validates its own portable schemas. It does not execute consumer commands or promote evidence into organizational authority. |
| Runtime tasks, evidence records, governance receipts, decisions, artifacts, and lineage in AI Society | `agent-kernel` and the active AK database | Persists runtime truth and content-addressed references. Storage proves custody and recorded lifecycle facts; it does not make a claim semantically correct. |
| Canonical cross-system concepts, labels, aliases, relations, and lifecycle of shared terms | `core/ontology-kernel` | Owns stable semantic definitions. A term should move here only after it is genuinely shared and its meaning needs one owner. |
| Ontology source admission, reference resolution, validation, packing, and conformance receipts | `core/rocs-cli` | Operationally validates and resolves ontology material. Source/schema/reference conformance is not semantic correctness, adoption, activation, or currentness. |
| Adoption, exceptions, approval, and interpretation for a concrete repository or organization | the owning human or policy surface | Tool output and persisted evidence inform the decision but do not replace it. |

## Evidence persistence through agent-kernel

Engineering-core already emits bounded receipts, dispositions, plans, work bundles, reconciliation results, and deterministic digests. In an AI Society deployment, agent-kernel is the appropriate durable store for the resulting runtime evidence and lineage.

The integration should preserve these layers:

1. engineering-core defines and validates the engineering-specific artifact;
2. an owner or authorized executor performs the work outside engineering-core;
3. agent-kernel records the execution evidence, governance receipt, artifact identifier, or content digest;
4. engineering-core may later reconcile an explicitly supplied artifact without upgrading the owner state;
5. the owning policy surface decides adoption, exception, promotion, or retirement.

A receipt and supporting evidence answer different questions:

- a receipt records **what governed transition or operation occurred**;
- evidence records **what observation, validation, or audit fact supported it**.

Agent-kernel already keeps this distinction for its runtime contracts. Engineering-core should preserve it rather than treating an evidence blob as proof that a transition occurred or treating a transition receipt as proof that its justification was sufficient.

### Minimum portable reference

When engineering-core documentation or a proposal refers to evidence stored outside the repository, record enough information to locate and verify it without copying the full payload:

- producer and schema identifier;
- stable evidence, receipt, run, or artifact identifier;
- subject repository and revision when applicable;
- content digest;
- capture time and bounded scope;
- authority ceiling or explicit nonclaim;
- optional ontology concept IDs used for classification.

Do not commit private evidence payloads merely to make shared guidance self-contained. Public consumers without agent-kernel may use digest-bound local artifacts that satisfy the same engineering-core schema; agent-kernel is an integration target, not a mandatory runtime dependency.

## Shared terminology through ontology-kernel

`ontology-kernel`, not `rocs-cli`, is the correct home for a cross-system glossary. `rocs-cli` should resolve, validate, pack, and expose the ontology definitions, while the semantic owner remains ontology-kernel.

Do not move every engineering-core enum into the shared ontology. States such as `declared`, `schema-valid`, `execution-observed`, and `evidence-verified` currently have precise meaning inside `engineering-evidence-receipt-v1`; preserving that schema-local meaning is safer than assigning a vague global definition.

Promote a term to ontology-kernel when all of these hold:

1. at least two independent systems or versioned schemas use the term;
2. inconsistent interpretation creates a real routing, policy, evidence, or user risk;
3. a concise definition, examples, anti-examples, and relations can be stated without depending on one implementation;
4. existing uses can reference a stable ontology ID without silently changing their local protocol meaning;
5. an owner and migration/deprecation path are known.

Likely candidates for a bounded ontology proposal are the cross-system nouns and relations around evidence, receipt, claim, authority, observation, verification, and disposition. Their protocol-specific state machines should remain in the owning schemas.

The ontology change belongs under `ontology/src/reference/` in `core/ontology-kernel`, follows `ontology-markdown-v1`, and is validated or retrieved through `rocs-cli`. Consumers should bind the ontology reference or snapshot digest they used. A successful ROCS conformance receipt proves exact source/schema/reference admission only; it must not be presented as evidence that the proposed meaning is correct or adopted.

## End-to-end shape

```text
engineering-core doctrine or recommendation
  -> owner-authorized execution
    -> engineering-core receipt/disposition artifact
      -> agent-kernel evidence/receipt/artifact persistence
        -> optional ontology-kernel concept IDs
          -> rocs-cli resolution and source-conformance proof
            -> owner decision about adoption, exception, promotion, or retirement
```

No arrow upgrades authority automatically.

## Pi and hierarchical AGENTS.md

Hierarchical `AGENTS.md` loading is a harness-level instruction mechanism used by Pi and repository-local workflows. This integration contract does not replace, flatten, generate, or centralize that hierarchy. Engineering-core documentation and skills remain subordinate to the instructions selected by the harness and owning repository.

Evidence persistence and ontology semantics therefore belong in the explicit contracts above, not in repeated `AGENTS.md` prose.

## Failure modes to reject

- requiring the private agent-kernel runtime to use the public engineering-core package;
- storing evidence in agent-kernel and then claiming the stored assertion is independently verified;
- defining canonical vocabulary in rocs-cli because it implements the validator;
- treating ROCS source conformance as semantic correctness, adoption, or currentness;
- replacing schema-specific state definitions with underspecified global terms;
- copying sensitive evidence into doctrine or agent-instruction files;
- allowing a generated artifact to promote itself into owner or policy authority.
