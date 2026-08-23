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

# RFC: engineering-core v1.0 convergence contract — revision 2

## Status and authority

- **RFC state:** revised proposal; not accepted and not an execution or release authorization.
- **Supersedes for review:** `docs/rfc/2026-08-23-v1-convergence-contract.md`; that artifact and its review remain immutable history.
- **AK decision:** `128` (`review_pending`; strict convergence with multi-lane synthesis at authoring time).
- **Revision authority:** AK task `4907` plus the operator decision that v1.0 owes no backward compatibility to pre-v1 package releases.
- **Lifecycle inputs:** `docs/project/2026-08-23-v1-convergence-problem-brief.md`, `docs/project/2026-08-23-v1-convergence-evidence-note.md`, and `docs/project/2026-08-23-v1-convergence-review-set-plan-r2.md`.
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

G0-A2 MUST produce a canonical v1 compatibility manifest using these default-deny classifications:

| Class | Required meaning |
|---|---|
| **Public stable** | Every documented CLI command/subcommand and declared option/exit meaning; every retained versioned protocol identifier and field meaning; stable catalog/content identifiers and selection semantics; packaged retrieval/rendering behavior; documented adoption, transition, diagnosis, rollback, and removal behavior; declared artifact names and supported platform/Python floor. Compatible v1.x rules apply. |
| **Experimental/pilot** | Explicitly labeled pilot content or optional preview surface that cannot become a default, stable dependency, or compatibility promise without a reviewed promotion. |
| **Internal qualification** | Gate envelopes, fixture corpora, study allocations, release-effect inventories, conformance implementation details, and review orchestration used only to qualify a release. Inclusion in the repository does not make them public, but exposing them through an otherwise public installed surface does. |
| **Owner adapter** | Owner-local AK, empirical, model/provider, repository, dashboard, or transport integration outside the portable core. It remains optional, replaceable, and owned by its source surface. |

An unlabeled documented consumer-facing surface defaults to **public stable**. The G0-A2 manifest mechanically enumerates surfaces under these rules; it cannot silently reclassify or exclude one to make a candidate pass. Any disputed classification is an architecture question requiring an accepted decision revision before candidate evidence.

### v1.x compatibility rules

Within the accepted v1 public surface:

- a patch release may correct behavior without changing documented meaning;
- a minor release may add optional behavior, fields, content, or commands while preserving existing valid use;
- deprecation may warn and name a replacement, but removal or semantic repurposing waits for a future major decision;
- incompatible command, exit, schema, catalog, content-identity, artifact-name, or supported-platform contraction is a major change;
- unknown non-critical extensions may be retained or ignored only as the owning protocol declares; unknown critical extensions fail closed; and
- no parser may treat malformed input as permission to negotiate or fall back to weaker semantics.

Package semver and protocol identifiers are independent namespaces. Existing identifiers such as `*-v1` MUST either retain their already-declared meaning and be ratified into the v1 manifest or be replaced by a new unambiguous identifier. Package `1.0.0` does not reset a protocol identifier.

### Stable core and adapter membrane

Portable core readers consume only canonical v1 envelopes. Version- or owner-specific conversion occurs at bounded ingress/egress adapters, never as historical-version branches spread through core logic. An adapter MUST be side-effect-free by default, preserve original identity and digest, record its own identity/version plus every default, transformation, and loss, then run canonical invariant validation. No safe conversion yields structured `unsupported` or `incomplete`, not guessed state.

Proof protocols may mature prospectively through separately accepted owner decisions without becoming semver APIs. A protocol revision restarts affected evidence. A change to a public surface, constitutional invariant, owner boundary, or pillar definition reopens this architecture decision rather than hiding inside a qualification protocol.

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

## Predeclared proof population

### Producer and coordination owner

| Role | Repository | Purpose | Counts as an independent positive adopter? |
|---|---|---|---|
| Product producer | `core/engineering-core` | Freeze candidate contracts, provide deterministic harnesses, validate artifacts, and integrate bounded references. | No |

Engineering-core may validate portable records and coordinate the product-level assessment. It MUST NOT execute participant commands by default, own participant dashboards, or convert supplied evidence into participant approval.

### Positive owner groups and participant baselines

Three independently governed owner groups and four positive participant baselines are REQUIRED. The extra TeachingCo baseline supplies the new-adopter journey that the three current adopters cannot.

| Owner group | Exact repository/baseline | Pre-RFC observed posture | Required proof role |
|---|---|---|---|
| HoldingCo | `holdingco/fcos-control-board` | Governance product; pre-v1 local immutable pin; declared planning/advisor/owner-use capabilities; historical owner-round-trip receipt. | Existing-adopter clean transition and governed owner-use/lifecycle canary; no pre-v1 behavior is presumed compatible. |
| TeachingCo | `teachingco/mathe` | Content-heavy project; pre-v1 local immutable pin; planning declared; prior static adoption history. | Small existing-adopter clean transition, portability, stale-posture detection, rollback, and removal canary. |
| TeachingCo | `teachingco/wib@316c45747560392fdab03498849652e8d7e94fcb` | Immutable historical product-content baseline immediately before its first engineering-core adoption; the three adoption surfaces are absent at this commit. | Owner-approved historical clean-slate adoption, failure recovery, removal, and restoration canary. It does not claim current `wib` is unadopted. |
| SoftwareCo | `softwareco/owned/pi-extensions` | Large TypeScript/Pi monorepo; immutable pre-v1 remote commit; heterogeneous package adoption surfaces. | Existing-adopter clean transition plus v1 federation, package-boundary, partial-population, and hostile historical-input canary. |

These are dated routing observations, not durable participant truth or successful proof. G0 MUST replace them with a reviewed population manifest containing exact full revisions, roles, immutable-source references, owner task IDs, validation contracts, baseline posture, and an authority ceiling. Every participant refreshes its Git, AK, policy, and validation state before owner acceptance. Pre-v1 pins identify starting evidence only. They create neither support nor compatibility obligations; each owner selects a frozen clean-transition, explicit-migration, or structured-unsupported path before proof.

### Required negative control

| Owner group | Exact repository | Pre-RFC observed posture | Required proof role |
|---|---|---|---|
| HealthCo | `healthco/agents` | No tracked engineering-core adoption surface or immutable pin at the assessed root. | Remain a truthful missing/non-adopter control during federation scans. No adoption mutation is required for v1. |

A missing participant MUST remain missing or unknown, not be inferred as adopted, unhealthy, or consenting. A later HealthCo adoption would require its own owner task and is outside this gate unless the RFC is revised before evidence capture.

### Population manifest and changes

G0-A2 MUST freeze `docs/project/v1-proof-population.json`. Its canonical digest is SHA-256 over UTF-8 JSON Canonicalization Scheme (RFC 8785) bytes; the raw transport-byte SHA-256 and byte length are recorded separately. Every G1–G5 artifact records the canonical digest.

The manifest is canonical only as the immutable population input for one protocol/candidate revision. It does not become current task, owner, validation, custody, or adoption truth. It identifies each positive baseline and negative control by owner, physical repository identity, full Git revision, immutable source, starting posture, permitted role, exact AK task ID, observed task state and observation time, owner-approval reference, validation contract, evidence custody, and authority ceiling. Every run re-resolves live AK and owner state; missing, stale, conflicting, or unknown state blocks execution rather than being repaired from the manifest.

A participant may decline, become unavailable, or prove structurally unsuitable. Replacement requires, before any replacement evidence is captured:

1. an RFC revision naming the replacement and preserving the reason;
2. an **accepted AK decision revision** referencing the new RFC and population manifest;
3. an exact owner-authorized task in the replacement repository;
4. a fresh preflight, protocol, metric declaration, and reviewer assignment;
5. a new population-manifest digest.

If population-dependent evidence has begun, every affected population gate restarts against the new digest. Silent substitution, a supporting artifact without accepted decision revision, or post-result population changes invalidate G1–G5 fan-in.

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
14. **Public behavior, not harness substitution.** Journeys use candidate-shipped commands or literal runbooks. Harnesses isolate, drive, and observe; they cannot substitute transition, apply, recovery, rollback, removal, or rendering. Git/filesystem state is an oracle, not the operator procedure.
15. **Compatibility differs from robustness.** Every historical fixture declares `clean_transition`, `explicit_migration`, or `unsupported`; release provenance never implies compatibility.
16. **Prospectively governed qualification.** Exact empirical thresholds, power, resource limits, and denominators require an owner-approved, justified protocol before affected output. They are qualification facts, not semver APIs, and cannot alter a constitutional invariant.

## Gate G0 — contract, authority, protocol, and candidate freeze

G0 has three ordered checkpoints.

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
- a canonical v1 compatibility manifest enumerates every public command, option and exit meaning, protocol/schema identifier, catalog/content identifier and semantic promise, support-platform floor, artifact name, transition surface, rollback/removal surface, experimental surface, internal qualification component, and owner adapter under the classification rules above; retained pre-v1 protocol identifiers are ratified or replaced explicitly;
- the G1 public-journey oracle; G2 canonical envelope, ingress/egress adapter contract, negotiation/downgrade-resistance algorithm, candidate-independent fixtures, justified resource bounds, normalization algorithm, threat matrix, and deterministic materialization rules; separately accepted G3 prospective empirical protocol, power/sensitivity code, case-cluster manifest, owner-balanced allocations, estimand, metrics, thresholds, missingness rules, forecast provenance, and analysis code; G4 live-pilot and deterministic lifecycle-conformance matrices; and gate-conformance source, mode schemas, and negative fixtures are frozen before affected output;
- a catalog-derived rendered-product manifest enumerates every stable lane, discipline, addendum, template, profile, policy/document projection, help surface, and documented no-effect example. Its oracle checks source/root/package parity, installed-wheel rendering, extracted-sdist rendering, links/front matter, deterministic bytes where promised, escaped hostile Markdown/terminal content, and absence of checkout-local paths;
- the transition-template manifest labels each artifact as a G0-A2 template or future G0-B instance, records candidate identity as unassigned, and permits no candidate-dependent bytes or expected-result digest to be fabricated at G0-A2;
- an impact matrix maps each candidate or protocol change to mandatory reruns;
- the engineering-core coordination budget is mapped to exact tasks;
- AK dependency edges—not titles, notes, artifact links, or deferral prose—make G0-B depend directly or transitively on every G4-A owner and engineering-core disposition task, and make G5 depend on every G1–G4 production and independent-review task.

Only G0-A2 releases separately owner-accepted G4-A pilot tasks. It does not release G1, G2, G3, G4-B, a candidate, publication, or rollout.

### G0-B — immutable release candidate

After G4-A and accepted convergence implementation complete, G0-B passes only when:

- one final-byte `1.0.0` candidate exists on a non-`main` branch/PR and immutable remote commit. That commit is an unsupported proof channel until the exact tag and Release exist;
- version fields, v1 compatibility/rendered-product manifests, catalogs/history, changelog, pre-v1 break/transition map, one release note, README, support policy, schemas, workflow, and lockfile are synchronized and digest-bound;
- the candidate contains the frozen conformance entrypoint, materializer, tests/negative fixtures, rendered-product validator, and public transition/recovery/rollback/removal instructions, all portable without home/sibling/untracked dependencies;
- one immutable toolchain manifest governs candidate proof and publication, and the actual workflow invokes fail-closed `pre-publish` before tag/upload for identity, stale/extra artifact, missing-evidence, pre-existing release, and toolchain drift cases;
- the read-only materializer changes only declared binding fields and emits separately custodied transition, fixture-instance, and independent-oracle expected-result digests reviewed before G2 output;
- per-participant G1 manifests, a default-deny candidate/G5 effect allowlist with before/after/custody/disposal receipts, and a G4 accepted-content/negative-lineage inclusion map are complete;
- a new checkout without `dist/` passes locked sync, `release-local.py verify --version 1.0.0`, candidate conformance/rendered docs, clean tracked/index checks, and effect inventory with no undeclared residue or child; and
- remote tag/Release are absent, while G0-B records the exact candidate, population, protocol/template/instance/transition, effects, G4 inclusion, toolchain, and workflow digests used by later gates.

**Failure rule:** this RFC authorizes no implementation. G0-A1 releases only protocol/harness authoring; G0-A2 releases only separately accepted G4-A pilots; G1–G3 and G4-B require both G0-A2 and G0-B.

## Gate G1 — Dependable Adoption

### Required journeys and frozen oracles

Mutation, failure, removal, and rollback journeys run in a disposable owner-controlled clone or equivalent replica with an independent Git common directory and isolated `HOME`, XDG, temporary, cache, credential, and configuration state. The replica contains no production credentials or endpoints. Network is denied except for manifest-approved immutable fetches whose commit/tree, dependencies, and executable build inputs are digest-bound. A linked worktree is sufficient only for read-only observation.

Before the first run, each G0-B participant journey manifest records for every numbered journey: starting checkpoint/digest; exact argv, cwd, environment, network policy, candidate resolution, and timeout; expected exit code, schema fields/statuses, allowed diff and writes, prohibited effects, validation, recovery operation, ending checkpoint, and artifact name. Invocation, owner approval, or final validation alone is not PASS. The dry-run plan/diff digest reviewed in journey 3 MUST be the input applied in journey 4; drift requires renewed review. An oracle change after evidence capture creates a new protocol revision and restarts affected evidence.

Each positive baseline executes these ten journey categories through candidate-shipped public commands or literal runbooks frozen in its manifest. Participant harnesses provide isolation and observation only:

1. resolve and install or invoke the immutable remote candidate without a local-checkout fallback;
2. retrieve and explain the selected guidance, dependencies, omissions, pilots, local deviations, stability class, and applicable pre-v1 break without hidden workspace context;
3. select `clean_adopt`, `clean_transition`, or an explicitly shipped `migration` mode; invoke the public planner and review its exact proposed plan/diff, preserved local truth, backup, recovery, and removal effects;
4. apply the exact owner-approved plan artifact. The public apply surface consumes or cryptographically binds the reviewed plan digest and starting-state preconditions, rejects drift, and provides atomic completion or documented recovery without accepted partial state;
5. diagnose and scan the resulting v1 adoption without executing undeclared commands, URLs, models, observations, or patches;
6. for existing adopters, complete the selected clean transition or explicit migration from the recorded starting state without claiming old behavior is compatible; for the historical clean-slate baseline, repeat plan/apply and prove documented idempotence;
7. separately inject (a) a syntactically malformed pin, (b) a syntactically valid but unavailable immutable commit on a manifest-approved credentialless fixture remote, (c) a malformed policy, and (d) one cancellation/interruption at the first mutation boundary. The malformed pin fails locally before DNS/network, credential-helper, import/build, or mutation effects. The unavailable pin may perform only approved DNS/network and Git object resolution against the named fixture; isolated configuration disables credential helpers and interactive authentication. Malformed policy fails before consumer-command or mutation effects; interruption leaves no residual process or accepted partial write. Each case invokes the public recovery path and ends at its frozen checkpoint without fabricated state or undeclared effect;
8. from a named post-apply v1 checkpoint, execute the candidate's public rollback/recovery procedure in an independent proof branch and restore the frozen starting posture. Git and filesystem comparison are independent oracles, not the rollback mechanism;
9. from a separate branch of that same post-apply checkpoint, execute the candidate's public removal procedure. Clean-slate removal follows successful application and cannot pass as a no-op. Only proof-introduced or owner-classified engineering-core fields/files may be removed; named runtime and operational-truth surfaces MUST remain intact;
10. restore the G0-B-predeclared final **proof-workspace** posture, validate it, inventory residual tracked/untracked/ignored and external state, then dispose of or quarantine the replica. This does not land participant changes or establish current adoption.

HealthCo is an explicit manifest member only as a negative control at one immutable revision. For every frozen G1/G2 command whose explicit input includes it, G0-B declares the exact versioned schema fields and expected missing/absent values. It counts in completeness reporting, never in the positive-adopter denominator. Its checkout remains read-only, no command executes inside it, and pre/post revision and filesystem receipts MUST match.

### Exact pass threshold

G1 passes only if:

- every frozen assertion and postcondition passes for all ten journey categories and four positive baselines: **40/40 required participant-journeys**;
- the historical `teachingco/wib` run begins from exact commit `316c45747560392fdab03498849652e8d7e94fcb`, under a current TeachingCo task authorizing only the disposable historical replica;
- every command that explicitly includes the negative control returns its frozen missing/absent schema result: **100%**, without mutation or invented denominator membership;
- the malformed-pin, well-formed-unavailable-pin, malformed-policy, and interruption cases are detected at their distinct frozen boundaries before their prohibited effects: **100%**;
- every declared pre-change, post-change, rollback, removal, and final validation succeeds;
- remote-source portability succeeds for all four positive baselines with zero local `git+file` or workspace-checkout resolution;
- there are zero unresolved objective diagnostics, silent deviation losses, undeclared residual effects, authority-loss events, or observed synthetic-secret disclosures across the frozen sink matrix;
- failure and recovery evidence remains owner-local or is exposed to reviewers only through an owner-approved transfer or bounded attested receipt.

Usability timings and operator commentary are retained as descriptive evidence. They cannot compensate for a failed required journey.

## Gate G2 — Federated Interoperation

### Required cross-owner matrix

Before any conformance output, G0-A2 freezes an RFC-8785-canonical candidate-independent fixture-template manifest, its raw/canonical digests, harness version, normalization/comparison algorithm, expected results and digests for candidate-independent fixtures, deterministic candidate-materialization rules, and entrypoint-to-threat matrix. Candidate identity remains unassigned; candidate bytes, candidate-dependent fixtures, and their expected-result digests are not fabricated or inferred at this stage.

At G0-B, after the exact candidate exists but before any G2 system-under-test output is visible, the frozen materializer binds the template to that candidate and emits a separate candidate-bound fixture manifest and transition record. The instance adds the candidate release fixture, raw/canonical digests, and expected normalized results determined through the frozen independent oracle rather than candidate execution. Independent review verifies that only declared transition fields changed. Neither materialization nor review mutates the candidate.

The matrix covers every command, parser, renderer, Git/subprocess call, output path, owner-boundary transfer, and model-response sink. It defines the exact denominator for every count or percentage. The resulting candidate-bound corpus includes:

- representative pre-v1 records labeled only as `clean_transition`, `explicit_migration`, or `unsupported` fixtures; canonical candidate-v1 records; synthetic additive v1.x records; and unsupported future-major/critical-extension records;
- all four positive outputs plus the explicit HealthCo control;
- complete, partial, unavailable, permission-denied, privacy-redacted, stale, and unsupported populations;
- reordered and duplicate identities, unknown future fields, unsupported schemas, and catalog skew;
- malformed/duplicate-member JSON, invalid UTF-8, deep or huge inputs, sparse/growing files, and exact-limit/over-limit cases;
- absolute, empty, dot, dot-dot, overlong, undecodable, traversal, control-character, leading-option, and revision/path-ambiguous names;
- symlinked final components and parents, hard-linked outside-root aliases, FIFO/socket/device files, unreadable parents/files, and unwritable outputs;
- final/parent rename, relink, replacement, same-size/mtime-restored mutation, and output-destination TOCTOU races;
- hostile Git configuration/environment/helpers, ANSI/bidi/terminal controls, Markdown/HTML/table/link injection, URL/tool instructions, and supplied patches or model responses.

The v1 federation envelope and negotiation algorithm are frozen before output. A reader intersects only its trusted local allowlist with a peer's authenticated declared versions, selects the highest common v1 protocol, and records that choice. Parse errors, attacker-controlled claims, or unknown critical extensions never trigger fallback. Unknown non-critical fields follow the owning protocol's declared preserve/ignore rule. Any conversion runs once at ingress through a named adapter and retains original bytes/digest, adapter identity, transformations, defaults, and loss. No common safe version yields structured `unsupported` or `incomplete`.

The fixture freezes trusted input/output root identities. Every component is no-follow checked; platforms without the required primitive fail closed. Paths are not reopened after validation, concurrent change is rejected, and no symlink, special file, unapproved existing file, partial output, or outside-root destination may be followed or overwritten.

G0-A2 freezes finite population, filesystem, parser, path, byte, traversal, output, memory, CPU, subprocess, and wall-clock limits from measured supported-platform baselines plus a documented safety margin. The protocol records the benchmark corpus, toolchain, rationale, exact-limit/over-limit fixtures, deadline start, and process-tree termination behavior before output. Limits cannot be raised after visibility to rescue a failure. Lower owning-schema limits still apply. Permission probes run without elevation or permission repair. Timeout or cancellation kills the process tree and leaves no accepted partial artifact.

Synthetic secret canaries cover policy values, file/path names, Git metadata, malformed inputs, diagnostics, reports, caches, and every approved request/response. Diagnostics and renderers escape controls and redact unapproved private metadata. Supplied content is data only: it cannot execute tools, fetch URLs, invoke credential helpers, import/build code, or apply patches.

### Exact pass threshold

G2 passes only if:

- every positive baseline produces an owner-local bounded observation at its revalidated task revision;
- at least two positive owner groups independently consume identical approved aggregate bytes and produce results equal under the frozen normalization algorithm;
- deterministic payloads are byte-identical across two runs with the same ordered inputs, and normalized results are invariant only to the explicitly permitted ordering transformations;
- every valid fixture passes and every invalid/unsupported fixture fails at its frozen boundary with structured, bounded, sanitized diagnostics: **100% of the frozen corpus and entrypoint matrix**;
- missing, unavailable, private, stale, and unsupported records remain explicitly incomplete and are never coerced to adopted, healthy, current, or verified;
- duplicate physical identities cannot inflate denominators or evidence counts;
- no command, model, URL, observation reference, supplied patch, Git helper, or hostile content is executed by scan/aggregation paths;
- generated reports and remediation queues remain in the consuming owner scope, and transfers use the exact approved bytes from universal rule 8;
- operation requires no hosted control plane or centrally invented society denominator;
- there are zero observed synthetic-canary disclosures, path escapes, authority promotions, bound overruns, blocking special-file reads, surviving processes, or partial accepted outputs across the frozen matrix.

Any G0-A2 template, normalization rule, bound, sink, oracle, materialization rule, or G0-B candidate-bound fixture/expected result change after the applicable output-visibility boundary creates a new protocol revision and restarts G2.

## Gate G3 — Evidence Calibration

G3 is executed by the exact empirical owner/repository/task admitted at G0-A2. Engineering-core supplies bounded schemas and candidate artifacts; it does not score itself, operate the empirical task, or turn a study result into doctrine, governance, release, or rollout authority. Results support only the frozen population, tasks, models, and estimand.

### Accepted prospective empirical protocol

Before **any** development-arm, static-arm, evidence-arm, forecast, or confirmatory output is visible, the empirical owner MUST obtain acceptance of a linked protocol decision. That protocol freezes and justifies:

- the target population, independent task clusters, disjoint development/confirmatory split, arm-neutral rubric, objective outcome oracle, exclusions, prompts/context, model identities, allocations, executors, masking, contamination controls, stopping rule, scoring environment/code, transfer bytes, missingness, and independent reviewer;
- a smallest effect of practical interest derived from owner decision costs, the interval/error criterion, a separately justified design alternative, prospective paired-cluster simulation or exact power analysis, attrition inflation, sensitivity to discordance and task correlation, and the resulting total/per-cell sample—not an RFC-invented fixed floor;
- equal total primary-estimand weight per **owner group × base-model identity** cell. Multiple baselines from one owner share that owner's weight under a frozen within-owner rule; adding a baseline cannot inflate its owner group's influence;
- at least two distinct base-model families/identities represented in every positive owner group. Prompt, seed, temperature, endpoint, adapter, or quantization variants of one base model do not count as model diversity;
- calibration metric(s), binning or smooth estimator, interval procedure, threshold, missing-forecast treatment, and a disjoint-development reference forecast. A constant reference is lawful only when prospectively justified against expected prevalence;
- cell and marginal harm boundaries with sensitivity analysis; no aggregate effect can waive a frozen harm stop; and
- a separate insufficient-evidence safety set with at least one case in every owner-group × base-model cell, excluded from improvement and calibration estimates.

The static plan is generated once, digest-bound, and reused byte-for-byte as the base for both arms. Both arms run in owner-authorized disposable replicas without shared branches or production effects. Allocation is block-randomized under the frozen protocol; executor and arm order are randomized or separated so one arm cannot learn from the other. Reviewers are masked to arm, forecast, model/provider, and owner disposition as far as technically possible; breaches and objective-only sensitivity results are reported.

For cluster `i` and arm `a`, `Y[a,i]=1` only when the arm satisfies the same frozen owner constraints, participant validation, and objective claim/patch verification rule; otherwise it is `0`. Evidence use, citation, stored claim, owner preference, pre-v1 behavior preservation, or owner disposition does not set `Y`. Old repository snapshots may supply heterogeneous context, but the outcome measures only supported target-v1 tasks.

The probability used for recommendation-calibration proof MUST be emitted by the evidence-advice surface for its exact `Y` outcome before execution, validation, or review. If a separate forecaster supplies it, the result is explicitly a forecaster-calibration claim and cannot qualify the advice surface. Forecasts remain hidden from outcome reviewers.

All frozen clusters remain intention-to-treat. Arm-attributable no-output, invalid output, or failed validation is `Y=0`. Administrative missingness is bounded pessimistically for superiority and calibration under the accepted protocol. There is no optional stopping, outcome-driven top-up, case substitution, or recommendation-level pseudoreplication. Loss of prospective power fails the study.

Owner dispositions, validation results, empirical outcomes, forecasts, receipts, and governance decisions remain separate. Every transfer uses universal rule 8, including SDK-injected metadata, telemetry, redirects/fallbacks, and destination region.

### Exact pass rule

G3 passes only if:

- every frozen confirmatory and safety cluster is reported, including negative and missing outcomes;
- the point estimate reaches the accepted practical-effect threshold and its predeclared lower interval bound is above no improvement under the pessimistic missingness analysis;
- every owner-group × base-model cell and each frozen marginal stratum is reported and no harm boundary fires;
- forecast calibration and skill satisfy the accepted prospective thresholds and reference comparison;
- every insufficient-evidence safety case emits machine-checkable `abstain` or `unknown`, with all actionable fields absent: **100% of the frozen safety set**;
- there are zero observed synthetic-canary disclosures, invalid citations, unbound patches, owner-identity mixups, unauthorized transfers, production effects, or authority promotions;
- the empirical owner publishes the protocol decision, power/sensitivity evidence, bounded results, replay/configuration receipt, limitations, masking breaches, exclusions, missingness, and counterevidence; and
- an independent reviewer confirms that acceptance/freeze preceded output and that no case, allocation, exclusion, forecast rule, metric, transfer rule, or stopping rule changed after visibility.

Failure of power, practical or interval boundaries, a harm stop, calibration, safety, transfer controls, or prospective integrity leaves G3 failed. A changed protocol requires a fresh accepted empirical decision, held-out corpus, and affected reruns; failed studies remain in lineage.

## Gate G4 — Review-Governed Evolution

### Authority split

Participant owners authorize only their local proposal, pilot, evidence, rollback, and disposition. They cannot transition shared engineering-core content. The engineering-core content owner alone may accept, reject, revise, deprecate, retire, or promote shared content under an exact task, accepted decision where required, and repository validation. Validation, participant disposition, content-owner transition, package distribution, and adoption remain separate facts.

### G4-A — live legitimacy plus transition conformance

After G0-A2, each positive owner group originates one substantial shared-content candidate under an exact owner task, for three independently governed live cycles. Before pilot output, the frozen matrix names each candidate, origin group, opt-in pilot groups, exact owner/content-owner tasks, reviewers/conflicts, content/protocol digests, success, harm and falsification criteria, minimum-supported-v1 consumer, expiry/review event, rollback checkpoint, and permitted transfer.

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

All live pilot mutations, content-owner decisions, accepted shared-content landings, and preserved negative lineage complete before G0-B. G0-B contains the final accepted state and immutable references for every other disposition.

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
- the minimum-supported-v1 consumer receives compatible behavior or the frozen structured v1 migration/downgrade result; and
- there are zero unowned defaults, irreversible owner-local transitions, erased negative results, coerced dispositions, or automatic promotions.

## Gate G5 — cumulative v1 release readiness

G5 is evidence fan-in over the exact G0-B commit, never release authority. It passes only when:

1. G0–G4 each have a PASS artifact, independent review, and no open blocker;
2. all artifacts bind one candidate/population digest and AK dependency edges—not titles, notes, or deferrals—show every production/review task complete;
3. two newly created standalone checkouts at that candidate start without `dist/`, enforce the effect allowlist, capture before/after repository/process/cache/network/service/configuration inventories, leave no undeclared effect or child, and pass the frozen toolchain, repository validation, `release-local.py verify --version 1.0.0`, rendered-product/docs checks, candidate conformance, and clean-index/diff checks;
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

- Rejection of this RFC leaves `v0.10.0` as the latest stable product and archives/defer-closes dependent tasks without rewriting evidence.
- Before the exact release action, a failed candidate remains isolated; fixes create a new candidate and impact-matrix reruns.
- A G1 failure restores or quarantines the disposable replica and preserves owner-local failure evidence; Git rollback is not claimed to reverse network, cache, process, service, or provider effects.
- A G2 failure withholds the incompatible aggregate path; owner-local source records remain untouched.
- A G3 failure leaves evidence-informed advice advisory/experimental and cannot be reframed as governance success.
- A G4 failure keeps candidates in their evidence-supported lifecycle states and restores the exact prior stable selection where rollback applies.
- Participant withdrawal invalidates the population digest and invokes the accepted prospective replacement process.
- Secret-canary disclosure, unauthorized transfer/execution/egress, permission bypass, path escape, fabricated evidence, silent substitution, deadman failure, surviving process, undeclared external effect, or authority promotion is an immediate stop.
- Incident recovery requires owner-led blast-radius assessment, notification, rotation/deletion requests where applicable, artifact invalidation/quarantine, compensating restoration, root-cause correction, affected-gate/protocol revision, required reruns, and independent closure. Irrecoverable transferred bytes are never described as rolled back.
- Expected negative fixtures count only at their frozen boundaries. Visible-loop, peer, and subagent work stops on task-scope drift, unresolved pre-existing changes, unexpected validation failure, or inability to bind proof to the exact owner task.

## AK execution shape

The intended authority graph is:

```text
RFC adversarial review + decision-support synthesis
  -> owner acceptance, ADR, immutable RFC binding (G0-A1)
    -> engineering-core protocol/harness authoring
      -> population, owner/empirical tasks, protocols, dependency admission (G0-A2)
        -> G4-A owner pilots + engineering-core dispositions
          -> immutable 1.0.0 candidate (G0-B)
            -> G1/G2/G3 + non-mutating G4-B
              -> cumulative G5 readiness evidence
                -> separate exact release task
                  -> dependent post-release verification task
```

The G0-A1 release task cannot complete until accepted decision/ADR and immutable review closure exist. G0-B depends directly or transitively on every exact G4-A owner and content-owner task. G5 depends on every exact G1–G4 production and review task. Deferrals remain active until those edges exist; clearing a deferral cannot waive fan-in. Cross-repository tasks are created only in their owning repositories after exact owner acceptance; they are never shadow tasks in engineering-core.

## Alternatives considered

### Stable core v1 with calibration and governance outside release qualification

Rejected as the release model, but its boundary insight is adopted. Qualification protocols remain internal/owner-governed rather than semver APIs; all four demonstrated pillars still gate the v1 product claim. Otherwise engineering-core could declare v1 while two advertised maturity properties remained unproven.

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
