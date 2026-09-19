---
summary: "AK5773: YAML-safe skill projection, native Pi discovery proof, and release-guidance composition limits."
read_when:
  - "Reproducing the generated release-skill loading defect or its bounded repair."
  - "Distinguishing release guidance discovery from installation, behavioral evaluation, or publication."
type: "evidence"
---

# Release-skill discovery repair — AK5773

## Scope and decision

Operator approved repairing/evaluating the existing engineering-core release skill
rather than introducing a duplicate release framework. Exact task: AK5773.
Baseline: `9225dd66a83b5a9c23e14d2f834dbabdd2ce71d8`.
Method: installed `agent-skill-engineer` 2.0.4, integrity-defect repair; no formal
optimization, model-comparison, or publication claim.

Compared two structures before mutation:

- repair the shared generator and compose the release discipline with the target
  lane and repo-local contract;
- create a separate universal release-operator skill.

Selected the first. The reproduced failure is malformed generated frontmatter,
not demonstrated lack of another workflow owner. The existing discipline covers
release prerequisites and artifact validation; repository workflows own execution.
A new operator skill remains unjustified by this loader evidence alone.

No source doctrine, profile membership, package version, consumer policy, global
skill installation, host settings, workflows, tags, or registry state was changed.
The 42 projected descriptions are reserialized; their decoded text, names and
bodies remain unchanged. Build outputs are local generated proof, not releases.

## Baseline and frozen regression intent

The generator interpolated descriptions beginning `[ec-discipline]` or `[ec-lane]`
as bare YAML scalars. Existing tests checked substrings rather than parsing.

Before the generator change:

- the strict skill-authoring audit returned `invalid-frontmatter`;
- installed Pi 0.84.4 `loadSkillsFromDir` returned zero release skills and a YAML
  parse warning;
- the strengthened 11-test projection suite failed with four failures and five
  errors before the repair.

Pre-repair regression inputs covered the real bracket/colon/comment case, quotes
and backslashes, injected newlines/frontmatter delimiters, tabs/carriage returns,
Unicode line/paragraph separators, Boolean-like text, aliases and mappings.
The fixed checks require one physical description line and exact string roundtrip.

## Repair and proof

`skill_front_matter` now uses `json.dumps(description)`: JSON strings are valid
YAML scalars and ASCII escapes prevent physical Unicode line separators. No YAML
runtime dependency was added. Generated files were regenerated, not hand-edited.

Observed outcomes:

| Check | Result |
|---|---|
| Projection suite | 11 tests pass |
| Complete repository unittest suite | 354 tests pass |
| Projection currentness / determinism | 42 skills, 25 profiles pass |
| Native Pi release-only discovery | One exact release skill; zero diagnostics |
| Native Pi explicit release + Python selection | Two exact skills; zero diagnostics; release entry present in formatted prompt |
| Native Pi entire skill directory | 43 skills including the separate engineering-core skill; 15 pre-existing dotted-name warnings |
| Repo self-check, lineage, addendum checks, skill sync, bounded adoption scan | Pass |
| Build and release-local verifier | Pass; wheel and sdist inspected, neither published |
| Independent reviewer | Source fix acceptable; no correctness/security blocker |
| Final whitespace check | Pass after removing one trailing blank line |

Independent review: `dispatch-1789809735385`. It independently compared all 42
projections with HEAD, verified unchanged bodies/names/decoded descriptions and
byte-identical `skills/profiles.json`, exercised native Pi parsing including all
eight edge fixtures, and ran ten read-only tests. It deliberately skipped the
existing write-producing determinism test; the controller ran all eleven.

Reproducible repo commands (from this repo root):

```bash
UV_NO_CONFIG=true uv sync --locked
UV_NO_CONFIG=true uv run --no-sync python -m unittest discover -s tests -v
UV_NO_CONFIG=true uv run --no-sync python -m engineering_core.self_check --repo-root .
UV_NO_CONFIG=true uv run --no-sync python scripts/check-release-lineage.py --mode ci
UV_NO_CONFIG=true uv run --no-sync python scripts/check-justfile-addenda.py
UV_NO_CONFIG=true uv run --no-sync python scripts/sync-skill-assets.py --check
UV_NO_CONFIG=true uv run --no-sync engineering-core scan-adoption \
  --scope . --include-scope-root --format json --prefer-repo --max-repositories 10
UV_NO_CONFIG=true uv build
UV_NO_CONFIG=true uv run --no-sync python scripts/release-local.py verify
git diff --check
```

The native observation imported the installed host's `dist/core/skills.js`, called
`loadSkillsFromDir` with each explicit skill root, then called `loadSkills` with
`includeDefaults:false` and the two explicit `skillPaths`, and checked
`formatSkillsForPrompt`. This was a direct library-level host observation: no Pi
session or model request was launched. Reproduction must resolve the installed
host module rather than assuming a machine-local path or a different version.

Fingerprints:

- baseline generator SHA-256: `9c767ee755b6b87a615c47f51512ed1007dcea156c57b423446a87644ffa0fb8`
- repaired generator: `7a3499ae910a79e3ebb03e1ea74870dd4fb4d5c694e90adaeca2fc9cadc76300`
- projection tests: `cfa86ec04a219125571c3fbc4d75550adfe93a8c74f838c3951f5adb5814cfd1`
- release skill: `ff6a9d782ea608489939e98fc428be1cdebc799fd727f774d968994c7e4ad2ba`

## Retained failures and limits

The post-repair strict skill-authoring audit still fails strict mode with zero
errors and five warnings: trigger phrasing, missing specifically named boundary,
workflow and verification sections, and missing eval suite. Its non-strict report
labels the skill valid. These are not silently waived or claimed as a strict pass;
source discipline headings and meaning were not rewritten to satisfy heuristics.
There is no A/A, A/B, fresh-model routing, comparative task-quality, cross-client,
permanent installation, publishing field proof, or production-ready claim.

The plain `uv sync --locked` attempt failed because ambient global exclude-newer
configuration disagreed with the lock. `uv --no-config sync --locked` succeeded.
An initial verifier pass subsequently rewrote `uv.lock` through nested `uv`
commands that did not inherit the outer CLI flag. Only that attributable options
block was removed, restoring exact tracked lock bytes. A second verifier run
with inherited `UV_NO_CONFIG=true` passed and left the lock unchanged. This is
captured as AK5775, not folded into the skill generator fix.

AK5774 tracks the 15 dotted-name portability warnings. Renaming them requires a
compatible profile/member migration, not a silent edit in this repair.

`docs/skill-profiles.md` now explains opt-in explicit loading and repo-pin-aware
release composition. Loading current checkout projections does not upgrade any
consumer's accepted engineering-core pin. DSPx's release workflow and its active
session inventory remain unchanged.
