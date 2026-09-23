---
summary: "Many-of-the-Greats adjudication for keeping executable lane configs true: why the ts lane shipped four silent defects and what the conformance harness proves."
read_when:
  - "Changing lane config blocks (biome.json, tsconfig.json, bunfig.toml, package.json scripts) or the lane conformance harness."
  - "Deciding whether a lane config claim is gated at release, checked offline, or left to dependency updates."
type: "decision"
---

# Lane config conformance adjudication (AK #5908)

## QUESTION

Engineering-core lanes embed configuration that consumers copy verbatim. The ts lane shipped four defects that its own validation couldn't see:

1. Biome `complexity/useLiteralKeys` (recommended) demands `obj.key`, while tsconfig `noPropertyAccessFromIndexSignature` demands `obj["key"]`. No line can pass both.
2. tsconfig `baseUrl` is rejected by tsgo (TypeScript 7, TS5102), so the lane's primary typecheck fails before it reads code.
3. The lane names its Bun config `bun.toml`. Bun reads only `bunfig.toml`, so `exact`, `frozenLockfile`, and `autoInstall = false` never apply. Verified: `bun add zod` writes `^4.6.5` under `bun.toml` and `4.6.5` under `bunfig.toml`.
4. `typecheck:fallback` runs `tsc`, but the lane's devDependencies don't include `typescript`; tool versions were `latest` and `^1.9.3`, which contradicts the lane's own exact-pin policy.

Root cause: the lane treats executable artifacts as prose. Their truth depends on external tools that release independently, and nothing in engineering-core executes them. Correctness was asserted, never proven, and tool drift was invisible.

Question: what mechanism keeps embedded configs true over time, and where should it gate?

## MODE 1 — MANY OF THE GREATS

### School 1: Hermetic reproducibility (Bazel/Nix)
- Core claim: a claim is true only relative to exact, pinned inputs. Unpinned inputs make every proof perishable.
- Premises: builds are functions of their inputs; `latest` is an undeclared input.
- Strongest case: defect 4 existed because "the lane's config" had no defined target. With `latest`, the same doc is right on Monday and wrong on Friday.
- What it sees that others miss: a conformance check against unpinned tools isn't a gate; it's a lottery.

### School 2: Live at head (continuous freshness)
- Core claim: pinning hides rot. The only honest signal is testing against what consumers will actually install next.
- Premises: consumers adopt new majors on their own schedule (the fleet already runs Biome 1.9 and 2.x side by side). A doc proven against old pins still misleads new adopters.
- Strongest case: defects 1–3 came from tool evolution (Biome 2, TS 7) the lane never saw. Pins would have frozen the lane on proven-but-obsolete tools.
- What it sees that others miss: a green pinned gate can be a comfortable lie about the present.

### School 3: Executable single source (config-as-code)
- Core claim: documents must not contain unexecuted artifacts. The source of truth is a real, tested file; the prose is a projection or a pointer.
- Premises: anything copied by humans or agents is code; code without execution decays.
- Strongest case: all four defects share one property: the config existed only inside Markdown.
- What it sees that others miss: the prose/test split itself is the defect class.

### School 4: Type authority over syntax (tool ownership)
- Core claim: when a type-aware tool and a syntactic linter disagree about a construct, the type-aware tool owns it, and the syntactic rule must yield.
- Premises: Biome is syntax-only; it can't tell an index signature from a declared property. typescript-eslint made the same call (`dot-notation` `allowIndexSignaturePropertyAccess`).
- What it sees that others miss: the conflict isn't a preference; one tool has the information to decide and the other doesn't.

## MODE 2 — CONFRONTATION

### Clash 1: Hermetic vs Live at head
- Fundamental contradiction: a gate must be deterministic (School 1), while freshness requires a nondeterministic input (School 2).
- Incompatible assumptions: "a release proves a fixed claim" vs "a release proves current reality."
- School 1 explains better why release gates must not flip on a Tuesday npm publish; School 2 explains better why the lane went stale unnoticed for two majors.
- Residual tension: irreducible within one gate. It's resolvable only by giving each concern a different gate.

### Clash 2: Executable single source vs doc-as-authority
- Fundamental contradiction: School 3 would move the configs into real files and generate the doc. Engineering-core's model makes `src/engineering_core/lanes/*.md` the authority (AGENTS.md "source docs"), with skills projected from it.
- Incompatible assumptions: School 3's real premise is "a single source, executed"; file-vs-Markdown is incidental.
- Resolution: extracting the fenced blocks from the authoritative doc and executing them satisfies School 3's actual premise (one source, executed) without inverting the authority map. Verbal, not fundamental.

### Clash 3: Type authority vs lint completeness
- Turning `useLiteralKeys` off also loses the rule's valid cases (`{ ["b"]: d }`, brackets on declared types). That loss is cosmetic; the alternative loses a type-level typo guard. There's no irreducible tension.

## MODE 3 — INTEGRATION OR DECISION

- Chosen path: contextual dominance.
- Result:
  - School 1 dominates the release gate. The harness runs against exact tool pins declared in the lane doc, installed from a committed `bun.lock` with `--frozen-lockfile --ignore-scripts`. Same inputs, same verdict.
  - School 2 dominates the update path, not the gate. Freshness is the job of `dependency-update-flywheel`: bump the lane pin, refresh the lock, and let the harness prove the new pin. Nondeterministic runs against the newest versions never block a release.
  - School 3 dominates the source question as reinterpreted. The lane doc stays authoritative; the harness extracts its fenced blocks, so there's no second copy to drift.
  - School 4 dominates the lint conflict: `useLiteralKeys` off, `noPropertyAccessFromIndexSignature` kept.
- Why this path is justified: each school is right about a different gate. Collapsing them into one gate either makes releases flaky (2 in 1) or hides staleness (1 without 2).
- What remains unresolved: pins still age between updates. That's accepted and made explicit, not hidden: the pin is visible in the lane, and staleness is a dependency-update decision.

## PRACTICAL CONSEQUENCE

- Offline unit tests (`tests/test_lane_ts_configs.py`) check the structural claims on every run: exact tool pins, a lock that matches the pins, and a `bunfig.toml` filename.
- The executable harness (`scripts/lane-conformance.py ts`) installs the pinned tools into a temporary directory and runs the lane's own `package.json` scripts on a fixture. It includes must-fail probes that prove each gate bites, so a config that silently fails to load can't pass.
- `scripts/release-local.py verify` runs the harness, so every release proves the ts lane configs work with their pinned tools.
- Second-order effects accepted: releases need Bun and an npm registry (or a warm Bun cache). Supply-chain exposure is bounded by exact pins, lockfile integrity, and `--ignore-scripts`.
- Second-order effect handled: `release-local.py verify` runs in the `ci.yml` release-proof, `release.yml`, and `auto-release.yml` jobs. Each now installs Bun `1.3.12` via `oven-sh/setup-bun@v2`, and an offline scenario fails if any job that runs verify lacks it.

## Refutations recorded during implementation

- **Exit code alone does not prove the contradiction is gone.** Mutation testing reintroduced `useLiteralKeys` into a copy of the lane doc, and the harness still passed: Biome 2.x reports that rule at `info` severity, which doesn't fail `biome check`. On 2.x the conflict shows up as advice to rewrite conformant code into code that fails TS4111, and agents and `--write --unsafe` act on that advice. The pass scenarios now also require zero `lint/…` diagnostics. After that change, all four mutations (useLiteralKeys on, baseUrl back, noExplicitAny off, noPropertyAccessFromIndexSignature off) fail the harness.
- **Hypothesis refuted:** `"types": ["bun-types"]` does resolve with `@types/bun` under Bun 1.3.12. It stays.

## Open decision surfaced (not part of AK #5908)

TypeScript 7.0.2 (stable, 2026-07-08) ships a native `tsc`, and `@typescript/native-preview` stopped publishing on 2026-07-07. The lane's split between `tsgo` as the primary typecheck and a JavaScript `tsc` as fallback is therefore obsolete. Under School 2's ruling that freshness belongs to the update path, #5908 pins what's proven (native-preview `7.0.0-dev.20260707.2`, typescript `6.0.3`); both the lane config and the lane's `typecheck` scripts pass TypeScript 7.0.2. Retiring the tsgo staging touches the ts lane, the pi-ts lane, and the TypeScript quality and Justfile addenda, so it's a separate doctrine change for the operator to decide.

**Resolved by AK #5916 (operator-approved 2026-09-23):** both the ts and pi-ts lanes now typecheck with `tsc --noEmit` from exactly pinned `typescript@7` (`7.0.2`). `@typescript/native-preview` and the dual-compiler `typecheck:fallback` are gone; recovering from a compiler regression means rolling back the pin. On a 400-file test project: TS 7 `tsc` 84 ms, the last `tsgo` preview 109 ms, TS 6 `tsc` 452 ms. TypeScript 7 drops the classic compiler API. An initial draft routed dev tools that still need it to `@typescript/typescript6`; the operator ruled "no fallback", so both lanes now say: TypeScript 7 only; dev tools needing the classic API are replaced, not kept on TS 6 (Biome instead of typescript-eslint; `tsc --declaration --emitDeclarationOnly` with an explicit `rootDir` for `.d.ts` output, verified on 7.0.2). Runtime product use of the compiler API is a declared library dependency under its explicit package name, never `typescript`. Impact scan across the workspace's ts/pi-ts lane repos found no classic-API dev tools. Twelve packages still pin `@typescript/native-preview` (11 in pi-extensions plus replay-fabric) and must migrate to `typescript@7`. `pi-typescript-tool` imports the classic API at runtime under the name `typescript` (6.0.3), so it must move that dependency to an explicit name. `ts-quality` pins its own `typescript` and doesn't affect consumer typechecks. Harness: 6/6 scenarios pass. The stale lockfile was rejected (`lockfile is frozen`) until it was refreshed.

- Third-order effect: the same defect class almost certainly exists in other lanes (py/ruff/pyright, rust, pi-ts). The harness is keyed by lane so they can be added one at a time; that's a follow-up, not part of #5908.
