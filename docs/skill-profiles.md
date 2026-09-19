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

## Release guidance: compose, do not duplicate

`ec-discipline-release-package` owns cross-language release guidance. Pair it with
only the recipient's relevant lane (`ec-lane-py`, `ec-lane-pi-ts`, or another
selected lane) and its repo-local release contract. The Python lane does not
mandate Release Please; the pi-ts lane recommends it. `just` remains a local
command interface, not an alternative to version/changelog coordination.

Before choosing or running a release path:

1. Read the target's instructions, `docs/engineering.local.md` and compact
   `policy/engineering-lane.json` selection, including its immutable release pin.
2. Retrieve guidance from that accepted revision. An absent discipline selection
   is an adoption proposal, not permission to edit policy. If the pin predates
   skill projections, read its canonical lane/discipline documents instead of
   silently loading today's checkout.
3. Inspect the target's version surfaces, dependency bounds, lockfile, release
   workflows and existing publisher. Keep source version, built artifact,
   GitHub release, registry publication and deployed version distinct.
4. Follow the recipient's validation and authorization contract. A request to
   inspect or prepare a release does not authorize publication. Check consumers'
   compatibility ranges and test the exact built artifacts, outside the source
   tree, before an explicitly approved publish operation.
5. After an uncertain publication, reconcile the exact package/version and
   artifact digest before retrying. An existing version or successful workflow
   is not proof that the intended bytes were published.

These steps compose existing guidance; they do not create a universal release
executor, override a consumer pin, or install/activate a skill in a host.

## Explicit Pi discovery and claim limits

A `skills/` directory in this repository does not automatically make its contents
available in another repository's Pi session. `ec-py` contains the Python lane
and default disciplines, not every optional discipline. `ec-full` is not the
remedy for a single missing release skill: it loads unrelated guidance.

For an explicitly accepted engineering-core checkout containing valid projections,
Pi accepts repeated `--skill` paths. For example, after resolving the recipient's
accepted revision to `EC_ROOT`, a deliberately isolated selection is:

```bash
pi --no-skills \
  --skill "$EC_ROOT/skills/ec-discipline-release-package" \
  --skill "$EC_ROOT/skills/ec-lane-py"
```

This command launches a session and suppresses ambient skill discovery; it is not
a read-only inspection command. It does not publish or make a persistent settings
change by itself. Use the chosen host's documented explicit-selection surface;
do not install global links or alter consumer settings as an incidental repair.

`scripts/build_skill_projection.py` generates the `ec-*` files. Descriptions are
JSON-quoted, YAML-compatible single-line scalars so brackets, colons, quotes,
newlines and Unicode separators cannot escape into frontmatter structure. Repair
the generator and regenerate; never hand-edit a projected skill.

Validation separates three claims:

- projection checks and scalar regression tests prove generated-byte consistency;
- native host loader observation proves discovery for that host/version and exact
  selected files, not persistent installation or model selection/use;
- fresh-context routing, behavior and authorized field trials are separate proof.
  Static audits or a formatted prompt do not establish successful releases.

The release skill is discipline guidance, not a field-qualified publishing agent.
Any later operator skill needs a demonstrated procedural gap, non-overlapping
triggers and recipient-owned evaluation. Existing dotted lane-addendum skill
names may warn in Pi and fail stricter hosts; preserve published profile keys and
handle any naming migration separately rather than silently renaming them.
