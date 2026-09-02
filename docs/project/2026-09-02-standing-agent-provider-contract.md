---
summary: "Candidate engineering-core provider contract and exact least-privilege adoption-steward profile."
read_when:
  - "Publishing or consuming engineering-core resources for a standing-agent release."
type: "contract-candidate"
status: "owner_acceptance_pending"
---

# Standing-agent provider contract

## Decision candidate

Engineering-core owns only the `engineering-core/ec-*` namespace. It is one provider, not the profile system. It publishes complete, immutable skill-tree and profile revisions with provider-qualified references. Importing or materializing a publication does not transfer content ownership and does not appoint an agent, approve a release, authorize a run, observe a runtime, or settle effects.

The machine-readable contract is `contracts/standing-agent/provider-contract-v1.json`. The exact first-pilot profile is `contracts/standing-agent/ec-adoption-steward.v1.json`, bound to observed source commit `51fc387556d0873bee61fea18164d707554b6af9` and five complete current skill trees. Its payload identity is `sha256:69fccd9bd1b304f01d1ae629a08818d0386791f853d79b895c7ce4e5367c4875`.

## Current versus target

Current `skills/profiles.json` provides mutable named lists including `ec-defaults` and `ec-full`; it has no accepted immutable publication contract and no `ec-adoption-steward` profile. The target adds an immutable publication envelope without changing current default resolution. The pilot profile is the exact five-tree `ec-defaults` baseline under the new name `ec-adoption-steward`. Any target-lane additions are task-scoped, exact, provider-qualified, and outside the immutable profile.

`ec-full` remains available to current consumers but is explicitly prohibited for the first high-assurance pilot. This contract does not edit the live agent manifest or switch a fleet default.

## Identity and completeness

A skill-tree reference is the complete Git tree, not only `SKILL.md`. Its entrypoint blob is recorded for audit, but the tree identity controls scripts, references, assets, and invocation policy. Aliases may aid discovery but are never exact identity. Historical availability is distinct from launch eligibility.

## Alias, compatibility, deprecation

Aliases are owner-maintained pointers and must resolve to one immutable publication plus a recorded effective interval. Moving an alias never changes the old publication. Deprecation preserves exact historical retrieval while making new launch eligibility false unless an explicit permit binds that revision. Schema-1/current-profile consumers continue unchanged.

## Security and authority boundaries

The profile may narrow knowledge and procedure inputs. It cannot widen tools, credentials, target repositories, effects, validity, or delegation. Model-controlled fields are requests only. Provider import into Prompt Vault remains a snapshot with the engineering-core owner and source revision attached.

## Acceptance scenarios

1. The validator recomputes the publication payload digest and checks all five complete trees.
2. A consumer rejects a bare `ec-discipline-testing` reference in strict resolution.
3. A task may add one exact target-lane tree only when the permit names it; the base publication remains unchanged.
4. A historical deprecated publication can be retrieved but is not launch eligible by that fact.
5. Import into Prompt Vault preserves owner and source and grants no appointment or run authority.

## Migration and rollback

Acceptance may add `ec-adoption-steward` as an additive profile publication and later expose a compatibility alias in `skills/profiles.json`; it must not rewrite `ec-defaults` or `ec-full`. Rollback removes the additive publication/alias and keeps all current profiles and consumers. No consumer migration is applied by this PR.

## Reversal triggers

Reopen if complete-tree identity cannot preserve invocation policy, if a required skill is outside engineering-core ownership, or if provider import is shown to transfer semantic ownership. Do not reopen merely because a consumer prefers a physical path or bare name.

## Acceptance required

This candidate becomes an owner-accepted contract only through the engineering-core repository's documented owner process and exact PR/commit reference. Merge alone must not be interpreted as agent appointment or execution authorization.
