---
summary: "Versioned engineering-core skill-profile interface, key stability, aliases, and fleet-reference validation."
read_when:
  - "Publishing, consuming, renaming, or removing an engineering-core skill profile."
  - "Validating agent manifests against engineering-core profiles."
type: "reference"
---

# Skill-profile fleet interface

`skills/profiles.json` is a published interface for agent manifests and dispatch tooling:

```json
{
  "schema": "engineering-core.skill-profiles/1",
  "profiles": { "ec-py": ["ec-lane-py"] },
  "deprecated_aliases": { "ec-python": "ec-py" }
}
```

The example alias illustrates the contract; it is not currently published. Consumers must reject an unknown schema, malformed profile data, aliases whose target is not canonical, and profile names found in neither `profiles` nor `deprecated_aliases`. A deprecated alias resolves to its canonical profile but should emit a repository-and-profile diagnostic so its owner can migrate.

## Stability rule

Profile keys are stable API identifiers. Membership may change as guidance evolves, but a key must not be renamed or removed in place. A rename is additive:

1. publish the new canonical key;
2. retain the old key in `deprecated_aliases`, pointing directly to the canonical key, for at least one engineering-core release;
3. migrate configured fleet manifests during that window;
4. remove the alias only after the fleet-reference check proves no configured manifest uses it.

`ec-defaults`, `ec-full`, and every published `ec-<lane-or-addendum>` key are covered by this rule. `tests/fixtures/skill-profile-v1-keys.json` is the additive compatibility baseline.

## Fleet check

The projection check can validate each immediate child repository's `agent.json` without writing to the fleet:

```bash
python3 scripts/build_skill_projection.py --check --fleet-root /path/to/agents
# or
ENGINEERING_CORE_FLEET_ROOT=/path/to/agents python3 scripts/build_skill_projection.py --check
```

An explicitly configured root that is missing, contains no manifests, has an unreadable manifest, lacks a non-empty `skills.profile`, or references an unknown profile fails closed. Diagnostics include both the agent repository and referenced profile. Alias references remain valid during the deprecation window and emit a migration diagnostic.

There is no unversioned bare-map compatibility projection. Consumers should migrate once to the schema object and then dispatch on `schema`; silently treating top-level metadata as profile keys would defeat fail-closed resolution.
