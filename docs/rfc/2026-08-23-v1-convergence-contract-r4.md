---
summary: "Revised Model A constitution and evidence-gated qualification contract for engineering-core v1.0."
read_when:
  - "Reviewing or executing any engineering-core v1.0 convergence work."
  - "Selecting owner canaries, empirical protocols, release evidence, or rollback criteria for v1.0."
  - "Assessing whether a claimed v1 pillar is demonstrated rather than merely implemented."
type: "rfc"
system4d:
  container:
    boundary: "engineering-core's public product contract plus explicitly accepted, owner-local AI Society proof tasks."
    edges:
      - "Agent Kernel decision, task, direction, evidence, and artifact references"
      - "owner-repository validation and canary receipts"
      - "DSPx/Oracle empirical protocol and results"
  compass:
    driver: "Earn a trustworthy semver v1.0 baseline without centralizing consumer authority or treating mechanisms as outcomes."
    outcome: "One cumulative, evidence-gated v1.0 contract across dependable adoption, federation, calibration, and governed evolution."
  engine:
    invariants:
      - "All four pillars are required for v1.0; strength in one cannot waive another."
      - "Repository owners retain execution, validation, adoption, rollback, and landing authority."
      - "No document, loop, scanner, model, receipt, or empirical result self-authorizes a release or doctrine change."
  fog:
    risks:
      - "Cross-owner evidence may be confused with central rollout authority."
      - "A broad implementation surface may pass proxies without proving complete operator journeys."
      - "Post-hoc thresholds could turn exploratory results into an unjustified v1 claim."
---

# RFC: engineering-core v1.0 convergence contract — revision 4

## Status and authority

- **RFC state:** revised proposal; not accepted and not an execution or release authorization.
- **Supersedes for review:** the historical RFC plus R2 and R3; every prior review attempt remains immutable history.
- **AK decision:** `128` (`review_pending`; strict convergence with multi-lane synthesis at authoring time).
- **Revision authority:** AK task `4907` plus the operator decision that v1.0 owes no backward compatibility to pre-v1 package releases.
- **Lifecycle inputs:** the problem/evidence notes and `docs/project/2026-08-23-v1-convergence-review-set-plan-r4.md`.
- **Durable product intent:** `docs/project/vision.md`.
- **Maturity contract:** `docs/project/product_posture.md`.
- **Draft baseline:** published `v0.10.0` commit `9038d1ed3d443f44e18624d908d266e5e6dfd934`.

The words **MUST**, **MUST NOT**, **REQUIRED**, and **PASS** describe the proposed v1 gate. They become an accepted execution membrane only through the linked Agent Kernel decision workflow. Review may freeze exact RFC bytes for decision support; it does not accept Model A. An accepted RFC still does not authorize mutation in a participant repository; every owner repository requires its own exact AK task, local instructions, validation contract, and landing decision.

## Decision requested

Adopt **Model A** as a two-layer semver `v1.0` contract:

1. a **public product constitution** defining the stable v1 surface, compatibility floor, authority boundaries, and owner exit; and
2. a **release-qualification program** requiring cumulative proof of four pillars without making every fixture, study, adapter, or release tool a public API.

The four required pillars are:

1. **Dependable Adoption**
2. **Federated Interoperation**
3. **Evidence Calibration**
4. **Review-Governed Evolution**

All four MUST reach the bounded baseline below before v1.0 is declared. Strength in one cannot waive another. Compatible maturation may continue through v1.x. This RFC defines no v2, v3, or v4 contract. A future incompatible public-contract change or materially different product constitution requires a new major-version decision.

## Product constitution and compatibility boundary

### Clean pre-v1 break

`1.0.0` makes **no backward-compatibility promise** to any `0.x` package release. It need not preserve pre-v1 command syntax, output bytes, package layout, policy shape, catalog behavior, implementation, or ability of old executables to read v1 state. No v0 deprecation window, mixed-runtime mode, or downgrade path is required.

Pre-v1 repositories and records may still be used as:

- starting states for an owner-approved clean transition;
- inputs to an explicitly named migration utility that v1 deliberately ships;
- historical or adversarial fixtures expected to return structured `unsupported`, `incomplete`, or migration-required results; or
- immutable evidence of earlier owner decisions.

Those uses do not imply compatibility. Any migration surface deliberately classified as public and stable at G0-A2 becomes part of the v1 contract from that point forward.

### Stable, experimental, internal, and owner-local surfaces

G0-A2 freezes the compatibility-manifest schema, classification rules, and candidate-independent inventory method. G4-A content remains pilot/candidate input, not a frozen v1 surface. After G4-A closes, G0-B emits the final candidate-bound compatibility manifest using these default-deny classifications:

| Class | Required meaning |
|---|---|
| **Public stable** | Every documented CLI command/subcommand and declared option/exit meaning; retained protocol identifier/field meaning; stable catalog/content identifier and selection semantic; packaged retrieval/rendering behavior; documented adoption/transition/diagnosis/rollback/removal behavior; artifact names, supported platform/Python floor, and documented parser/schema acceptance guarantees. Compatible v1.x rules apply. |
| **Experimental/pilot** | Explicitly labeled pilot content or optional preview surface that cannot become a default, stable dependency, or compatibility promise without a reviewed promotion. |
| **Internal qualification** | Gate envelopes, fixture corpora, study allocations, release-effect inventories, conformance implementation details, and review orchestration used only to qualify a release. Inclusion in the repository does not make them public, but exposing them through an otherwise public installed surface does. |
| **Owner adapter** | Owner-local AK, empirical, model/provider, repository, dashboard, or transport integration outside the portable core. It remains optional, replaceable, and owned by its source surface. |

An unlabeled documented consumer-facing surface defaults to **public stable**. Each final manifest entry records its stable ID, class, normative source, introduced version, semantic/output/error promise, deprecation state, and executable compatibility assertion/fixture. Retained pre-v1 protocol IDs additionally bind an immutable declaration/fixture baseline proving that ratification did not narrow meaning. Missing source or assertion fails G0-B.

G0-B stores the final manifest, rendered-product manifest, fixtures, and assertions as the immutable v1.0 compatibility baseline. Every future v1.x release compares its candidate against that baseline and all intervening compatible additions; removal, narrowing, or semantic drift fails the v1.x gate. Classification rules cannot silently exclude a surface to make a candidate pass. A disputed classification requires an accepted architecture revision before candidate evidence.

### v1.x compatibility rules

Within the accepted v1 public surface:

- a patch release may correct behavior without changing documented meaning;
- a minor release may add optional behavior, fields, content, or commands while preserving existing valid use;
- deprecation may warn and name a replacement, but removal or semantic repurposing waits for a future major decision;
- incompatible command, exit, schema, catalog, content-identity, artifact-name, or supported-platform contraction is a major change;
- unknown non-critical extensions may be retained or ignored only as the owning protocol declares; unknown critical extensions fail closed; and
- no parser may treat malformed input as permission to negotiate or fall back to weaker semantics.
- documented parser/schema acceptance guarantees are public behavior: v1.x may raise them but cannot lower them and reject previously valid v1 records. An emergency contraction requires an explicit security decision and incompatible protocol/major-version treatment, not a compatible release label.

Package semver and protocol identifiers are independent namespaces. Existing identifiers such as `*-v1` MUST either retain their already-declared meaning and be ratified into the v1 manifest or be replaced by a new unambiguous identifier. Package `1.0.0` does not reset a protocol identifier.

### Stable core and adapter membrane

Portable core readers consume only canonical v1 envelopes. Conversion occurs once at bounded ingress; egress only renders a declared target and appends to the same lineage. Adapters never spread historical branches through core logic or re-convert an already canonical record. Each side-effect-free conversion binds input and canonical-output digests, adapter executable/configuration digest, trust decision, identity/version, defaults, transformations, losses, and prior conversion chain before invariant validation.

Loss of identity, authority, provenance, privacy classification, critical fields, completeness, or population meaning yields `unsupported`; declared non-critical loss yields `incomplete`; only semantically lossless conversion may yield `complete`. If no safe conversion exists, the result is `unsupported` or `incomplete`, never guessed state.

Proof protocols may mature prospectively through separately accepted owner decisions without becoming semver APIs. A protocol revision restarts affected evidence. Pre-G0-B G4 candidate formation may change future public content under the frozen classification rules; after G0-B, a change to the compatibility baseline, constitutional invariant, owner boundary, or pillar definition requires a new candidate and the governing architecture/major-version path.

## Why a convergence contract is needed

Version `v0.10.0` already contains mechanisms across all four pillars. The unresolved risk is therefore not simply missing feature surface. It is whether those mechanisms work together under complete operator journeys, independent owner boundaries, realistic version skew and hostile inputs, prospective empirical comparison, and reversible doctrine review.

A source implementation, unit test, static adoption flag, matched bundle, or successful visible loop can support one part of that proof. None establishes the cumulative product claim by itself.

## Scope

### In scope

- freezing the minimum public v1 constitution and the default-deny classification used to enumerate exact candidate surfaces;
- proving complete clean adoption, owner-approved transition, recovery, rollback, and removal journeys;
- proving bounded cross-owner production and consumption under skew and partial information;
- prospectively testing evidence-informed advice against a static baseline;
- exercising proposal, pilot, review, promotion, rejection, revision, deprecation, and retirement paths;
- preserving counterevidence, abstentions, negative results, privacy, and owner exit;
- producing a release-readiness assessment through AK and owner evidence.

### Non-goals

- inventing a hosted control plane or society-wide repository denominator;
- bulk adoption or mutation from scanner output;
- making Agent Kernel, DSPx, ROCS, Prompt Vault, Pi, or engineering-core absorb another owner's authority;
- requiring external organizations for v1.0;
- claiming causal effectiveness from schema conformance or owner-authored receipts;
- using model agreement, review rhetoric, or loop count as a release metric;
- defining v2+;
- promising compatibility with a pre-v1 package release or requiring a v0 runtime to consume v1 state;
- merging or pushing a `1.0.0` release-candidate commit to `main`, creating a tag, publishing, or rolling out consumers without a separate exact release task and operator action after G5.

## Qualification population

### Producer and coordination owner

| Role | Repository | Purpose | Counts as an independent positive adopter? |
|---|---|---|---|
| Product producer | `core/engineering-core` | Freeze candidate contracts, provide deterministic harnesses, validate artifacts, and integrate bounded references. | No |

Engineering-core may validate portable records and coordinate the product-level assessment. It MUST NOT execute participant commands by default, own participant dashboards, or convert supplied evidence into participant approval.

### Constitutional population properties and initial candidates

The accepted qualification protocol MUST contain at least three independently governed positive owner groups, at least four baselines, an existing-adopter transition, a historical clean-slate adoption, a heterogeneous/package-boundary case, and one truthful non-adopter negative control. Engineering-core cannot count as a positive adopter. The following repositories are provisional initial candidates, not constitutional identities:

| Group | Provisional candidate | Proof role |
|---|---|---|
| HoldingCo | `holdingco/fcos-control-board` | Existing-adopter transition and governed lifecycle. |
| TeachingCo | `teachingco/mathe` | Small transition, portability, rollback, and removal. |
| TeachingCo | `teachingco/wib@316c45747560392fdab03498849652e8d7e94fcb` | Historical clean-slate adoption, recovery, removal, restoration. |
| SoftwareCo | `softwareco/owned/pi-extensions` | Heterogeneous transition, federation, package boundaries, hostile history. |

These are routing observations, not durable truth, successful proof, or required identities. G0-A2 replaces them through an accepted qualification-population decision and reviewed manifest containing exact revisions, roles, owner task IDs, validation, custody, baseline posture, and authority ceilings. Each participant refreshes Git/AK/policy/validation before acceptance. Pre-v1 pins create no compatibility obligation; each owner selects a frozen clean-transition, explicit-migration, or unsupported path.

### Required negative control

| Provisional candidate | Required role |
|---|---|
| `healthco/agents` | Truthful read-only missing/non-adopter; no adoption mutation. |

A missing participant remains missing/unknown, never adopted, unhealthy, or consenting by inference. A later adoption requires its own owner task; the qualification protocol replaces the negative control prospectively if needed.

### Population manifest and changes

G0-A2 MUST freeze `docs/project/v1-proof-population.json`. Its canonical digest is SHA-256 over UTF-8 JSON Canonicalization Scheme (RFC 8785) bytes; the raw transport-byte SHA-256 and byte length are recorded separately. Every G1–G5 artifact records the canonical digest.

The manifest is canonical only as the immutable population input for one protocol/candidate revision. It does not become current task, owner, validation, custody, or adoption truth. It identifies each positive baseline and negative control by owner, physical repository identity, full Git revision, immutable source, starting posture, permitted role, exact AK task ID, observed task state and observation time, owner-approval reference, validation contract, evidence custody, and authority ceiling. Every run re-resolves live AK and owner state; missing, stale, conflicting, or unknown state blocks execution rather than being repaired from the manifest.

A participant may decline or become unsuitable. Before replacement evidence, a fresh accepted qualification-population decision preserves every constitutional population property, records the reason, exact owner task, preflight/protocol/metrics/reviewer, and new manifest digest. If population-dependent evidence began, affected gates restart. Silent or post-result substitution invalidates G1–G5; changing a constitutional population property reopens this RFC.

## Universal proof rules

Every gate applies these rules:

1. **Stage-correct binding.** G0-A1 binds the exact RFC commit/digest and authority state; G0-A2 binds candidate-independent templates with candidate unassigned; G4-A binds exact pilot/participant revisions; G0-B emits separate candidate-bound instances; G1–G5 bind one candidate and population digest.
2. **Owner-local authority.** Participant effects require participant tasks/instructions. Engineering-core validates projections; it never replaces AK, empirical, content-owner, release-owner, or participant truth.
3. **Declared effects.** Each run records relevant Git/index/untracked/ignored, process, cache, network, service, credential, configuration, temporary, task, and external state before/after. Undeclared state is never absorbed; surviving effects fail or quarantine the run.
4. **Portable source.** Portability proof uses an immutable remote source in an isolated clean environment, never a sibling or home-relative checkout.
5. **Truthful evidence.** Failures, unknowns, missingness, abstentions, rejected proposals, and counterevidence remain first-class. Structural validity, match, owner acceptance, empirical result, governance decision, readiness, and publication remain separate facts.
6. **Reproducibility.** Deterministic payloads run twice from identical ordered inputs and are byte-identical; timestamped receipts remain separate. Empirical outputs bind their declared seeds/configuration and replay limits.
7. **Default-deny transfer and custody.** Before crossing an owner/reviewer/model boundary, the source owner approves the exact outbound bytes/digest/length, recipients/endpoint/region, purpose/classification, access/encryption, logs/cache/session, retention/deletion, route, adapter/model identity, and training use. Sent bytes match approval; raw snapshots remain local; responses are untrusted. External artifacts record owner, classification, custody, readers, retention, producer configuration, capture/review/quarantine state, authority ceiling, and authenticated owner attestation. Secrets/private source are not committed or used for provider training.
8. **No waiver or rewriting.** Any failed required participant or pillar blocks v1.0. Later decisions may revise protocols prospectively; they cannot relabel observed failure or erase lineage.
9. **Independent review.** A producer cannot be its gate's sole reviewer. Authorship, role, owner affiliation, conflicts, inputs, and outcome are recorded before closure.
10. **Drift restarts affected proof.** Candidate changes create new candidates. Undeclared participant, task, protocol, fixture, owner, case, or release-state drift invalidates the run; a frozen impact matrix determines reruns.
11. **Machine-decidable envelopes.** G0-A2 freezes one versioned schema and stage map for `pass|fail|blocked|incomplete`, identity/binding, owner/task, inputs/commands/outputs/assertions, denominator/limits, state/effects, failure/missingness, digests, authority ceiling, and review. Templates cannot pass; an instance passes only with every required assertion true and no required unknown. Narrative cannot override payload.
12. **Constrained materialization.** G0-A2 freezes template digests, stages, fields G0-B may bind, deterministic algorithm, independent oracle, reviewer, and invalidation rules. The read-only G0-B materializer emits separately custodied transition/instance records, never rewrites candidate/templates, executes no proof path, and obtains candidate-dependent expected results from the frozen independent oracle before system output. Any undeclared field/edit invalidates the transition.
13. **Executable conformance.** G0-A2 freezes one portable entrypoint, source digest, argv, mode contracts, and JSON result. The candidate contains those bytes. `candidate`, `readiness`, and mutation-path `pre-publish` modes fail closed on missing/unknown input, drift, nonzero exit, or non-`pass`; conformance supplies no authority.
14. **Public behavior, not harness substitution.** Journeys use candidate-shipped commands or a candidate path/digest enumerated by the rendered-product manifest. Harnesses only isolate, invoke, observe, and run owner validation; they cannot substitute transition, apply, recovery, rollback, removal, or rendering. Git/filesystem state is an oracle, not the operator procedure.
15. **Compatibility differs from robustness.** Every historical fixture declares `clean_transition`, `explicit_migration`, or `unsupported`; release provenance never implies compatibility.
16. **Prospectively governed qualification.** Empirical thresholds/power, platform CPU/memory/time budgets, and fixture denominators require a justified owner-approved protocol before output. Public parser/schema acceptance guarantees remain v1 compatibility facts and cannot be weakened by a qualification budget. Neither class may alter a constitutional invariant.

## Gate G0 — contract, authority, protocol, and candidate freeze

G0 has four ordered checkpoints.

### G0-A1 — accepted-decision membrane

G0-A1 passes only when:

- decision 128 references the final full Git commit and RFC content SHA-256, is accepted as **Model A**, has legal review closure and an ADR, and is linked to active direction `AK.V5.SF01`;
- every required review/synthesis artifact, or its canonical AK attachment envelope, binds that same commit and content digest; an artifact is not required to self-reference the commit that contains it. A path-only reference, `review_pending`, null outcome, missing review track, absent legal closure/ADR, or digest mismatch fails G0-A1;
- `ak direction check` and the decision passport report no unresolved structural issue;
- an AK-native dependency or deferral holds the G0-A1 release task until those conditions pass.

G0-A1 releases only exact engineering-core tasks that author protocols and deterministic harnesses. It authorizes no participant mutation, empirical or gate outcome capture, candidate creation, PASS claim, publication, or rollout.

### G0-A2 — protocol, population, and owner-task admission

After the G0-A1 authoring tasks complete, G0-A2 passes only when:

- the reviewed population manifest and canonical/raw digests exist under the projection ceiling above;
- every participant owner has recorded acceptance of an exact scoped task and declared validation commands, baseline state, evidence custody, reviewers, transfer policy, isolation boundary, rollback boundary, and final proof-workspace posture;
- the empirical owner, owning repository, selection authority, exact owner-local task, evidence custody, transfer policy, and independent reviewer are named;
- the compatibility-manifest schema and candidate-independent inventory enumerate every required class/field/assertion under the constitution above; current documented surfaces and retained protocol IDs are inventoried as inputs, while final candidate values remain unassigned;
- the G1 public-journey oracle; G2 canonical envelope, ingress/egress adapter contract, negotiation/downgrade-resistance algorithm, candidate-independent fixtures, justified resource bounds, normalization algorithm, threat matrix, and deterministic materialization rules; separately accepted G3 prospective empirical protocol, power/sensitivity code, case-cluster manifest, owner-balanced allocations, estimand, metrics, thresholds, missingness rules, forecast provenance, and analysis code; G4 live-pilot and deterministic lifecycle-conformance matrices; and gate-conformance source, mode schemas, and negative fixtures are frozen before affected output;
- the rendered-product schema/inventory covers every stable content/help/no-effect surface. Its oracle requires source/root/package parity, installation of the exact built wheel into an empty environment, execution from the exact extracted sdist through its documented workflow, normalized candidate-bound output comparison, links/front matter, deterministic promises, hostile rendering, and no checkout-local paths;
- the transition-template manifest labels each artifact as a G0-A2 template or future G0-B instance, records candidate identity as unassigned, and permits no candidate-dependent bytes or expected-result digest to be fabricated at G0-A2;
- an impact matrix maps each candidate or protocol change to mandatory reruns;
- the engineering-core coordination budget is mapped to exact tasks;
- AK edges—not titles, notes, or deferrals—make G0-A3 depend on every convergence-implementation, G4-A owner, content-owner, and review task; G0-B depends on G0-A3 candidate preparation; G5 depends on every G1–G4 production/review task.

G0-A2 releases only exact engineering-core **convergence-implementation** tasks and separately owner-accepted G4-A pilots. Implementation tasks may build frozen public/proof mechanisms but cannot set `1.0.0`, form a candidate, capture G1–G4 outcomes, publish, or mutate participants.

### G0-A3 — implementation and candidate-preparation admission

After all G0-A2 implementation and G4-A production/review/disposition tasks complete, G0-A3 independently verifies their fan-in, accepted content/negative lineage, clean source state, and unresolved rerun obligations. Only then may it release one exact engineering-core candidate-preparation task.

That task is confined to an isolated non-`main` branch/PR and a candidate-bound effect allowlist. It may integrate accepted bytes, materialize final manifests/instances, set final version metadata, run candidate checks, and publish only an immutable proof commit to the declared proof channel. It may not merge main, create/move a tag or Release, upload public assets, execute G1–G4, mutate participants, or claim PASS. Drift/failure leaves no candidate or creates a new candidate identity after correction and required reruns.

### G0-B — immutable release candidate

After the G0-A3 task produces its exact commit, G0-B passes only when:

- one final-byte `1.0.0` candidate exists on a non-`main` branch/PR and immutable remote commit. That commit is an unsupported proof channel until the exact tag and Release exist;
- after all G4-A landings, the final compatibility/rendered-product manifests materialize every entry, normative source, executable assertion and retained-protocol baseline against the exact candidate; version fields, catalogs/history, changelog, pre-v1 break/transition map, one release note, README, support policy, schemas, workflow, and lockfile are synchronized and digest-bound;
- the candidate contains the frozen conformance entrypoint, materializer, tests/negative fixtures, rendered-product validator, and public transition/recovery/rollback/removal instructions, all portable without home/sibling/untracked dependencies;
- one immutable toolchain manifest governs candidate proof and publication, and the actual workflow invokes fail-closed `pre-publish` before tag/upload for identity, stale/extra artifact, missing-evidence, pre-existing release, and toolchain drift cases;
- the read-only materializer changes only declared binding fields and emits separately custodied transition, fixture-instance, and independent-oracle expected-result digests reviewed before G2 output;
- per-participant G1 manifests, a default-deny candidate/G5 effect allowlist with before/after/custody/disposal receipts, and a G4 accepted-content/negative-lineage inclusion map are complete;
- a new checkout without `dist/` passes locked sync, release verification, exact-wheel installation in an empty environment, exact-sdist extraction/workflow execution, candidate-bound rendering/conformance, clean index, and effect inventory without undeclared residue/child; and
- remote tag/Release are absent, while G0-B records the exact candidate, immutable v1.0 compatibility/assertion baseline, population, protocol/template/instance/transition, effects, G4 inclusion, toolchain, and workflow digests used by later gates.

**Failure rule:** the RFC itself authorizes no effects. Only the exact tasks released by G0-A1/A2/A3 may perform their bounded stage. G1–G3 and G4-B require G0-B; release/publication require G5 plus a separate operator-approved task.

## Gate G1 — Dependable Adoption

### Required journeys and frozen oracles

Mutation, failure, removal, and rollback journeys run in a disposable owner-controlled clone or equivalent replica with an independent Git common directory and isolated `HOME`, XDG, temporary, cache, credential, and configuration state. The replica contains no production credentials or endpoints. Network is denied except for manifest-approved immutable fetches whose commit/tree, dependencies, and executable build inputs are digest-bound. A linked worktree is sufficient only for read-only observation.

Before the first run, each G0-B journey manifest records starting/ending checkpoints, candidate argv/runbook digest, environment/network/timeout, status/schema, effects, validation, and recovery. If any operation touches owner-writable files, a non-empty mixed-ownership map covers every applicable structured and textual pattern; omissions need independent `not_applicable` review. Invocation, approval, or final validation alone is not PASS. Journey 4 binds the reviewed plan digest; drift requires renewed review.

Each baseline executes ten categories through candidate commands or rendered-manifest path/digest runbooks; harnesses only isolate, invoke, observe, and validate:

1. resolve and install or invoke the immutable remote candidate without a local-checkout fallback;
2. retrieve and explain the selected guidance, dependencies, omissions, pilots, local deviations, stability class, and applicable pre-v1 break without hidden workspace context;
3. select `clean_adopt`, `clean_transition`, or an explicitly shipped `migration` mode; invoke the public planner and review its exact proposed plan/diff, preserved local truth, backup, recovery, and removal effects;
4. apply the exact owner-approved plan artifact. The public apply surface consumes or cryptographically binds the reviewed plan digest and starting-state preconditions, rejects drift, and provides atomic completion or documented recovery without accepted partial state;
5. diagnose and scan the resulting v1 adoption without executing undeclared commands, URLs, models, observations, or patches;
6. for each manifest-declared adoption/resolution scope—including legitimate package-local scopes—prove one active v1 resolution, no active pre-v1/mixed-runtime dependency, and preserved owner truth; clean-slate adoption also proves idempotence;
7. prove minimum failure boundaries: malformed pins fail before DNS/network/helpers/import/build/mutation; unavailable well-formed pins contact only the approved credentialless fixture remote with no interactive/helper auth and fail before dependency/import/build/mutation; malformed policy fails before consumer command/mutation. Interruption/failure is then injected at every durable mutation boundary, unless fault injection proves transactional atomicity at each boundary. Public recovery leaves no fabricated/partial state, helper, or process;
8. from a post-apply v1 checkpoint, execute the candidate public rollback/recovery procedure and restore the exact starting posture; Git/filesystem comparison remain independent oracles;
9. for every baseline, branch from post-apply state, add a frozen owner edit to each mixed-ownership case, then execute candidate removal. Drift requires a new reviewed removal plan or structured refusal. PASS requires repository validation without engineering-core; absence of every classified active pin, selection, generated adoption surface, and runtime dependency; preservation of unrelated fields/content, owner runtime truth, and historical evidence; and no no-op success;
10. restore the G0-B-predeclared final **proof-workspace** posture, validate it, inventory residual tracked/untracked/ignored and external state, then dispose of or quarantine the replica. This does not land participant changes or establish current adoption.

The selected negative control is an explicit manifest member at one immutable revision. Every command including it has frozen missing/absent fields. It counts only in completeness, remains read-only, executes no command, and has identical pre/post revision/filesystem receipts.

### Exact pass threshold

G1 passes only if:

- every frozen assertion/postcondition passes for all ten categories and every positive baseline: **10 × N of 10 × N required journeys**, where `N` is the accepted manifest denominator;
- the accepted clean-slate baseline begins at its exact manifest revision under a current owner task authorizing only the disposable replica;
- every command that explicitly includes the negative control returns its frozen missing/absent schema result: **100%**, without mutation or invented denominator membership;
- the malformed-pin, well-formed-unavailable-pin, malformed-policy, and interruption cases are detected at their distinct frozen boundaries before their prohibited effects: **100%**;
- every declared pre-change, post-change, rollback, removal, and final validation succeeds;
- remote-source portability succeeds for every positive baseline with zero local `git+file` or workspace-checkout resolution;
- there are zero unresolved objective diagnostics, silent deviation losses, undeclared residual effects, authority-loss events, or observed synthetic-secret disclosures across the frozen sink matrix;
- failure and recovery evidence remains owner-local or is exposed to reviewers only through an owner-approved transfer or bounded attested receipt.

Usability timings and operator commentary are retained as descriptive evidence. They cannot compensate for a failed required journey.

## Gate G2 — Federated Interoperation

### Required cross-owner matrix

Before any conformance output, G0-A2 freezes an RFC-8785-canonical candidate-independent fixture-template manifest, its raw/canonical digests, harness version, normalization/comparison algorithm, expected results and digests for candidate-independent fixtures, deterministic candidate-materialization rules, and entrypoint-to-threat matrix. Candidate identity remains unassigned; candidate bytes, candidate-dependent fixtures, and their expected-result digests are not fabricated or inferred at this stage.

At G0-B, after the exact candidate exists but before any G2 system-under-test output is visible, the frozen materializer binds the template to that candidate and emits a separate candidate-bound fixture manifest and transition record. The instance adds the candidate release fixture, raw/canonical digests, and expected normalized results determined through the frozen independent oracle rather than candidate execution. Independent review verifies that only declared transition fields changed. Neither materialization nor review mutates the candidate.

The matrix covers every command, parser, renderer, Git/subprocess call, output path, owner-boundary transfer, and model-response sink. It defines the exact denominator for every count or percentage. The resulting candidate-bound corpus includes:

- pre-v1 `clean_transition|explicit_migration|unsupported`, canonical candidate-v1, additive v1.x, and unsupported future-major/critical-extension records;
- every positive output plus the selected control; complete/partial/unavailable/denied/redacted/stale/unsupported populations; duplicates/reordering, unknown fields/schemas, and catalog skew;
- malformed/duplicate JSON, invalid UTF-8, depth/size/growth and exact-limit cases; absolute/empty/dot/traversal/control/option/revision-ambiguous paths;
- symlink/hard-link/special/unreadable/unwritable files, parent/final replacement and TOCTOU races, hostile Git/helpers, terminal/Markdown/HTML/link injection, URLs/tool instructions, patches, and model responses.

Before output, G0-A2 freezes each protocol family's version grammar/total order, local minimum semantic/security floor, critical-extension namespace, and negotiation transcript. A peer authenticates its **complete offer** with peer identities, offer ID, freshness/replay scope, channel or artifact binding, and payload digest. The reader intersects that offer with its trusted allowlist, rejects stale/replayed/stripped offers, selects the highest common version at or above its floor, and binds the full offer, selection, identities, floor, and payload digest in the result. Parse errors, attacker claims, or unknown critical extensions never trigger fallback; unknown non-critical fields follow the protocol's preserve/ignore rule.

Conversion occurs once at ingress under the adapter status rules above. The append-only record binds input/output digests, adapter executable/configuration, trust decision, transformations/loss, and prior chain; double conversion and chain truncation fail. Absence of a common safe version or conversion yields structured `unsupported`/`incomplete`.

Fixtures freeze trusted roots; every component is no-follow checked. Missing primitives, concurrent change, reopen, special/symlink targets, unapproved overwrite, partial output, or outside-root destination fail closed.

The candidate compatibility manifest freezes public parser/schema acceptance guarantees—nesting, members, strings, file/payload/path sizes and other validity ceilings—with exact-limit/over-limit fixtures. V1.x cannot lower them. Separately, G0-A2 derives qualification-only population, filesystem, output, memory, CPU, subprocess, and wall-clock budgets from measured supported-platform baselines and a safety margin. It freezes benchmark/toolchain/rationale and process-tree handling before output; budgets cannot be raised after visibility and cannot undercut public acceptance guarantees. Permission probes never elevate/repair. Timeout/cancellation kills the tree and leaves no accepted partial artifact.

Synthetic canaries cover policy, paths, Git, malformed input, diagnostics/reports/caches, and requests/responses. Output escapes controls/redacts private metadata. Supplied content is inert: no tools, URLs, helpers, imports/builds, or patches.

### Exact pass threshold

G2 passes only if:

- every positive baseline produces an owner-local bounded observation at its revalidated task revision;
- at least two positive owner groups independently consume identical approved aggregate bytes and produce results equal under the frozen normalization algorithm;
- deterministic payloads are byte-identical across two runs with the same ordered inputs, and normalized results are invariant only to the explicitly permitted ordering transformations;
- every valid fixture passes and every invalid/unsupported fixture fails at its frozen boundary with structured, bounded, sanitized diagnostics: **100% of the frozen corpus and entrypoint matrix**;
- every applicable entrypoint × threat cell contains a fixture, including offer replay/stripping and adapter-chain loss, or an independently reviewed `not_applicable` rationale;
- missing, unavailable, private, stale, and unsupported records remain explicitly incomplete and are never coerced to adopted, healthy, current, or verified;
- duplicate physical identities cannot inflate denominators or evidence counts;
- no command, model, URL, observation reference, supplied patch, Git helper, or hostile content is executed by scan/aggregation paths;
- generated reports/remediation remain in consuming-owner scope, and transfers use exact bytes approved under the universal **Default-deny transfer and custody** rule;
- operation requires no hosted control plane or centrally invented society denominator;
- there are zero observed synthetic-canary disclosures, path escapes, authority promotions, bound overruns, blocking special-file reads, surviving processes, or partial accepted outputs across the frozen matrix.

Any G0-A2 template, normalization rule, bound, sink, oracle, materialization rule, or G0-B candidate-bound fixture/expected result change after the applicable output-visibility boundary creates a new protocol revision and restarts G2.

## Gate G3 — Evidence Calibration

G3 is executed by the exact empirical owner/repository/task admitted at G0-A2. Engineering-core supplies bounded schemas and candidate artifacts; it does not score itself, operate the empirical task, or turn a study result into doctrine, governance, release, or rollout authority. Results support only the frozen population, tasks, models, and estimand.

### Accepted prospective empirical protocol

Before **any** development-arm, static-arm, evidence-arm, forecast, or confirmatory output is visible, the empirical owner MUST obtain acceptance of a linked protocol decision. That protocol freezes and justifies:

- target population, independent clusters, disjoint development/confirmatory split, arm-neutral rubric, objective oracle, exclusions, the sole treatment contrast, prompts/context, model set, allocations, executors, masking/contamination controls, stopping rule, scoring code/environment, multiplicity/error control, transfer bytes, missingness, and reviewer;
- a smallest effect of practical interest derived from owner decision costs, the interval/error criterion, a separately justified design alternative, prospective paired-cluster simulation or exact power analysis, attrition inflation, sensitivity to discordance and task correlation, and the resulting total/per-cell sample—not an RFC-invented fixed floor;
- equal top-level primary-estimand weight per owner group. Within each owner's fixed unit weight, frozen baseline × model weights sum to one, so adding a baseline or model cannot increase owner influence;
- the same frozen set of at least two distinct base-model families/identities in every positive owner group. Prompt, seed, temperature, endpoint, adapter, or quantization variants of one base model do not count as diversity;
- calibration metric(s), binning or smooth estimator, interval procedure, threshold, missing-forecast treatment, and a disjoint-development reference forecast. A constant reference is lawful only when prospectively justified against expected prevalence;
- cell and marginal harm boundaries with sensitivity analysis; no aggregate effect can waive a frozen harm stop; and
- a separate insufficient-evidence safety set with at least one case in every owner-group × base-model cell, excluded from improvement and calibration estimates.

The static plan is generated once and reused byte-for-byte. Within each paired cluster, arms have the same task, base plan, model identity/configuration, instructions except the declared treatment slot, tools, context outside that slot, execution budget, executor policy, and validation. Only the predeclared owner-evidence/advice payload differs. If the protocol changes a broader bundle, G3 may claim only that bundle comparison, not an evidence effect. Both arms use owner-authorized disposable replicas; allocation/order are randomized or isolated against contamination. Reviewers are masked as far as possible; breaches and objective-only sensitivity are reported.

For cluster `i` and arm `a`, `Y[a,i]=1` only when the arm satisfies the same frozen owner constraints, participant validation, and objective claim/patch verification rule; otherwise it is `0`. Evidence use, citation, stored claim, owner preference, pre-v1 behavior preservation, or owner disposition does not set `Y`. Old repository snapshots may supply heterogeneous context, but the outcome measures only supported target-v1 tasks.

The probability used for recommendation-calibration proof MUST be emitted by the evidence-advice surface for its exact `Y` outcome before execution, validation, or review. If a separate forecaster supplies it, the result is explicitly a forecaster-calibration claim and cannot qualify the advice surface. Forecasts remain hidden from outcome reviewers.

All frozen clusters remain intention-to-treat. Arm-attributable no-output, invalid output, or failed validation is `Y=0`. Administrative missingness is pessimistically bounded for superiority, calibration, and every harm boundary; unresolved harm-relevant missingness fails G3. There is no optional stopping, outcome-driven top-up, substitution, or recommendation-level pseudoreplication. Loss of prospective power fails.

Owner dispositions, validation, outcomes, forecasts, receipts, and governance decisions remain separate. Every transfer follows the universal **Default-deny transfer and custody** rule, including SDK metadata, telemetry, redirects/fallbacks, and region.

### Exact pass rule

G3 passes only if:

- every frozen confirmatory and safety cluster is reported, including negative and missing outcomes;
- the point estimate reaches the accepted practical-effect threshold and its predeclared lower interval bound is above no improvement under the pessimistic missingness analysis;
- every owner-group × base-model cell and each frozen marginal stratum is reported and no harm boundary fires;
- forecast calibration and skill satisfy the accepted prospective thresholds and reference comparison;
- every insufficient-evidence safety case emits machine-checkable `abstain` or `unknown`, with all actionable fields absent: **100% of the frozen safety set**;
- there are zero observed synthetic-canary disclosures, invalid citations, unbound patches, owner-identity mixups, unauthorized transfers, production effects, or authority promotions;
- the empirical owner publishes the protocol decision, power/sensitivity evidence, bounded results, replay/configuration receipt, limitations, masking breaches, exclusions, missingness, and counterevidence; and
- an independent reviewer confirms acceptance/freeze preceded output and **no frozen protocol field** changed after visibility.

Failure of power, practical/interval boundaries, multiplicity control, harm, calibration, safety, transfer, or prospective integrity leaves G3 failed. Any protocol change requires a fresh accepted empirical decision, held-out corpus, and affected reruns; failed studies remain in lineage.

## Gate G4 — Review-Governed Evolution

### Authority split

Participant owners authorize only their local proposal, pilot, evidence, rollback, and disposition. They cannot transition shared engineering-core content. The engineering-core content owner alone may accept, reject, revise, deprecate, retire, or promote shared content under an exact task, accepted decision where required, and repository validation. Validation, participant disposition, content-owner transition, package distribution, and adoption remain separate facts.

### G4-A — live legitimacy plus transition conformance

After G0-A2, the G4 protocol selects three distinct positive owner groups, each originating one substantial candidate under an exact task. Before output, the matrix freezes candidates, origin/pilot groups, owner/content-owner tasks, reviewers/conflicts, digests, success/harm/falsification criteria, minimum-supported-v1 consumer, expiry/review event, rollback, and transfer.

A live cycle is:

```text
proposal record
  -> opt-in bounded pilot
    -> evidence and counterevidence
      -> participant-local disposition
        -> engineering-core content-owner decision
          -> rollback/expiry/final state with preserved lineage
```

Every candidate includes the minimum decision record from `docs/content-lifecycle.md`. Independent contexts means distinct positive owner groups; TeachingCo's two baselines count as one. Participant evidence never changes shared state by itself. Promotion, when evidence supports it, still requires at least two distinct positive owner groups including one other than the originator. The emergency exception cannot satisfy ordinary promotion proof.

**No distribution of live outcomes is required.** Every candidate is judged only against its frozen criteria. A lawful promotion, revision, rejection, deprecation, retirement, or other content-owner disposition counts as a completed cycle; expiry without the required decision does not. The release gate cannot demand a sacrificial rejection, force a promotion, or reinterpret evidence to fill a quota.

Separately, G0-A2 freezes a deterministic lifecycle-conformance suite covering proposal, pilot selection, promotion, revision/split, rejection, deprecation, retirement, expiry, rollback, invalid transition, stale evidence, and unauthorized promotion. It uses synthetic fixtures or prospectively selected immutable owner-attested historical cases. This suite proves transition mechanics and lineage only; it does not count as live owner evidence or dictate a live outcome.

A rollback drill remains mandatory because it tests reversibility rather than substantive judgment: from an explicit pilot selection, restore the exact prior stable selection without erasing proposal, evidence, decision, or failure history.

All live pilots, content-owner decisions, accepted candidate landings, and negative lineage complete before G0-B. Even accepted content remains pre-v1 candidate input until G0-B materializes the final compatibility/rendered manifests and exact release candidate; G4-A therefore cannot mutate an already frozen v1 baseline.

### G4-B — post-candidate verification

After G0-B, G4-B is non-mutating verification. It checks the exact candidate's inclusion map from every accepted G4-A digest to its candidate path/digest and from every rejected, reverted, revised, deprecated, retired, or expired outcome to preserved immutable lineage. It replays the deterministic transition suite and reproduces minimum-v1 compatibility, rollback, and participant-validation evidence without changing the candidate. A defect requiring content/code change creates a new candidate and invokes the impact matrix.

### Exact pass rule

G4 passes only if:

- all three live candidates preserve problem, audience/scope, invariant, load triggers, strongest alternative, evidence, counterevidence, falsification, v1 compatibility/transition effect, rollback, review trigger, retirement signal, and semantic references where applicable;
- every pilot is opt-in, bounded, expires or reaches a named review event, and cannot silently become default;
- each live cycle reaches an evidence-supported participant disposition and content-owner decision without any required outcome distribution;
- the deterministic suite passes every valid and invalid transition fixture, including the separately exercised rollback, with preserved immutable lineage;
- participant validation, participant disposition, content-owner transition, AK authority, distribution status, and adoption status remain separate fields;
- every shared transition is recorded by the engineering-core owner surface and linked to owner-attested evidence; participant/model/loop output cannot perform it;
- accepted changes land before G0-B only through exact engineering-core tasks and complete repository validation; G4-B performs no mutation;
- stable catalog/docs/package projections are synchronized, while negative and superseded material remains historically interpretable without requiring executable pre-v1 compatibility;
- every previously valid minimum-supported-v1 use remains compatible. A structured migration/downgrade result may cover only a newly optional capability or explicit owner-selected transition; it cannot substitute for broken v1 behavior; and
- there are zero unowned defaults, irreversible owner-local transitions, erased negative results, coerced dispositions, or automatic promotions.

## Gate G5 — cumulative v1 release readiness

G5 is evidence fan-in over the exact G0-B commit, never release authority. It passes only when:

1. G0–G4 each have a PASS artifact, independent review, and no open blocker;
2. all artifacts bind one candidate/population digest and AK dependency edges—not titles, notes, or deferrals—show every production/review task complete;
3. two standalone checkouts start without `dist/`, enforce/inventory effects, leave no residue/child, and pass toolchain/repo/release/conformance/clean-index checks plus all candidate-bound render assertions by installing each exact wheel into an empty environment and executing each exact extracted sdist through its documented workflow;
4. both builds produce only the named wheel, sdist, and `SHA256SUMS`; artifact/manifest bytes are identical and their digests, toolchain, effect inventories, custody, and disposal/quarantine receipts are recorded;
5. candidate-head and merge-test SHAs are distinct facts, and required platform CI passes on the recorded merge-test SHA without being called candidate-SHA evidence;
6. the release note, pre-v1 break/transition map, v1 compatibility and rendered-product manifests, README, support policy, changelog, catalogs, schemas, workflow, and artifacts match their G0-B digests and tell one status-accurate story;
7. every positive baseline installs the immutable remote candidate and the untouched negative control returns its frozen result;
8. AK passport/direction/task closure, evidence/counterevidence, rollback, transition, protocol/instance, artifact/effect, and rerun records are complete;
9. final independent review confirms candidate/population identity, stage transitions, fan-in, residual effects, release controls, and status language; and
10. only after those inputs exist, the candidate-contained `readiness` mode independently verifies their digests/fields/toolchain/artifacts/workflow and returns `pass`.

A G5 PASS authorizes no merge, push, tag, publication, rollout, external-task closure, or future major.

### Separate release and verification

A separate exact release task and explicit operator approval may open one serialized window for the recorded candidate and current remote-main SHA. Immediately before mutation it refetches main/tags, proves the tag/Release absent, verifies remote main is an ancestor of the candidate, and stops on changed identities or lost serialization.

Only the approved exact-SHA fast-forward is allowed. After exact-main CI, mutation automation runs candidate-contained `pre-publish` mode before tag/upload. Candidate, triggering CI head, current remote main, release build SHA, and proposed peeled tag target MUST be equal; the toolchain and absence checks MUST still pass.

Publication consumes the exact G5 artifact bytes or reproduces and byte-compares them plus `SHA256SUMS` before creating the tag. Mismatch blocks tag and upload; an existing tag never redirects a build; manual fallback requires a separate exact task and the same proof. Downstream rollout remains owner-authorized.

A dependent post-release task downloads into an empty directory, admits only the approved wheel/sdist/checksums, compares bytes and identities, then permits **published-and-verified** status. The explicit states are `candidate`, `release-blocked` (main updated/no tag), `tag-created-release-absent` (lineage point of no return), `published-verification-pending`, and `published-and-verified`. Failure preserves the reached state and lineage, stops rollout, quarantines affected copies, and requires an explicit corrective/completion/withdrawal decision; a public tag is never retargeted or reused.

## Rollback and stop rules

- Rejection leaves v0.10.0 current and preserves/defer-closes lineage; a failed pre-release candidate stays isolated and fixes create a new candidate plus impact-matrix reruns.
- G1 restores/quarantines its replica without pretending Git reverses external effects; G2 withholds the aggregate path without touching owner records.
- G3 failure leaves evidence advice experimental; G4 preserves evidence-supported dispositions and restores prior selection where rollback applies.
- Participant withdrawal creates a new accepted population digest and affected reruns.
- Disclosure, unauthorized transfer/execution/egress, permission bypass, path escape, fabrication, substitution, failed deadman, surviving process, undeclared effect, authority promotion, task drift, or unbound proof stops work immediately.
- Owner-led incident response records blast radius, notification/rotation/deletion, quarantine/invalidation, restoration, root cause, protocol correction, reruns, and independent closure. Irrecoverable transferred bytes are never called rolled back; negative fixtures count only at frozen boundaries.

## AK execution shape

The intended authority graph is:

```text
RFC review/synthesis -> owner acceptance + ADR (G0-A1)
  -> protocol/harness authoring -> admission (G0-A2)
    -> bounded convergence implementation + G4-A pilots/dispositions
      -> implementation/pilot fan-in + exact candidate task (G0-A3)
        -> immutable candidate assessment (G0-B)
          -> G1/G2/G3 + non-mutating G4-B -> G5 evidence
            -> separate release task -> post-release verification
```

Each arrow is an AK dependency/task gate; deferrals cannot waive it. Cross-repo tasks exist only in owning repos after owner acceptance.

## Alternatives considered

### Stable core v1 with calibration and governance outside release qualification

Strongest case: stabilize only the portable deterministic CLI/content/protocol core, keep calibration and governed-evolution claims experimental or separately certified, release sooner, and reduce dependence on external empirical and owner campaigns. This yields a smaller compatibility promise and repeatable release control.

Rejected because the durable product promise already treats evidence-bounded improvement and reversible multi-owner evolution as product properties, not optional certifications. Calling the core v1 while those advertised properties remain unqualified would narrow the product claim rather than prove it. Model A accepts the real costs—later release, owner/empirical dependencies, and more evidence—but isolates qualification tooling from semver. Owner refusal or failed proof leaves v0.10.0 current; it never justifies coercion or a deadline waiver.

### Remain pre-v1 and mature pillars independently

Rejected. It preserves flexibility but withholds a stable consumer constitution after the product already exposes substantial adoption and protocol surfaces. Model A instead permits a clean v0-to-v1 break, then demands compatible v1.x evolution.

### One major version per pillar or compensation across pillars

Rejected. The pillars are categorical properties of one product, not delivery versions or an average score. A strong pillar cannot waive a different failure mode.

### Declare v1 from existing mechanisms

Rejected. v0.10.0 breadth is not complete operator, federation, calibration, or lifecycle proof.

### Require an external organization

Deferred. Public portability is mandatory; the initial conditional claim is limited to independently governed AI Society owner groups.

## Review questions

1. Does the constitution define a clean pre-v1 break and a sufficiently exact stable v1/v1.x surface?
2. Are public core, owner adapters, experimental content, and internal qualification tooling separated without loopholes?
3. Do G1 journeys prove candidate-shipped transition, recovery, rollback, removal, and rendered behavior rather than harness proxies?
4. Does G2 distinguish unsupported history from compatibility and prevent downgrade or adapter-induced semantic loss?
5. Does the accepted G3 protocol make power, weighting, thresholds, forecasts, and harm stops prospective and justified?
6. Does G4 prove live legitimacy and all lifecycle mechanics without requiring a distribution of owner decisions?
7. Can every gate fail visibly while preserving owner authority, exact-candidate proof, incident containment, and truthful status?
