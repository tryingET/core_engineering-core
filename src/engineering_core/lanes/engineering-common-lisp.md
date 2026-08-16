---
summary: "Common Lisp engineering lane for language extension, REPL-driven development, ASDF systems, dependencies, testing, and validation."
read_when:
  - "Working in a repo or package whose selected engineering-core lane is common-lisp."
  - "Choosing Common Lisp implementations, ASDF structure, dependency workflows, testing, or validation."
type: "guide"
---

# Common Lisp lane — libraries, CLIs, services, and long-lived systems

Use this lane when Common Lisp is the requested implementation language. Prefer a small, explicit system definition and reproducible non-interactive commands over development flows that depend on an editor image or ambient user configuration.

## Baseline toolchain

- **Implementation:** SBCL is the default development and CI implementation. Add CCL, ECL, ABCL, or another implementation only when portability, embedding, platform, or JVM requirements make it part of the supported contract.
- **System definition and build:** ASDF. Commit every `.asd` file and keep system names, source layout, test systems, and dependencies explicit.
- **Portable utilities:** use UIOP before adding a dependency for process, path, environment, or portability helpers that it already supplies.
- **Dependency availability:** Quicklisp is a common ecosystem distribution, but ambient Quicklisp state is not a reproducible project dependency contract.
- **Reproducible dependency workflow:** use Qlot when the repo needs checked-in project-local dependency resolution. CLPM is a valid alternative when deliberately selected and documented.
- **Testing:** expose the canonical suite through `asdf:test-system`. Follow an established repo framework; FiveAM, Parachute, and Rove are valid choices, but no framework is mandatory across all Common Lisp repos.

## Language extension is a first-class design option

Do not treat Common Lisp as a conventional language with parentheses. One of its central engineering advantages is that programs can add domain-appropriate language constructs in the language itself.

When the specification or libraries do not provide the abstraction a problem needs, actively evaluate these options instead of defaulting to repetitive boilerplate or importing another language's architecture:

1. a function or higher-order function when ordinary evaluation rules are sufficient;
2. a generic function, method combination, or CLOS protocol when behavior varies by type or role;
3. a macro when the abstraction needs new evaluation rules, binding forms, control flow, compile-time translation, or declarative syntax;
4. a reader extension only when genuinely new surface syntax repays its effects on tooling, composition, and security;
5. the Metaobject Protocol when the project intentionally needs to specialize class, slot, generic-function, or method behavior and accepts the portability contract.

Agents working in Common Lisp should explicitly consider language extension when they encounter a missing operator, repetitive domain form, state-machine notation, query language, policy language, resource-management construct, or object protocol. The absence of a construct from ANSI Common Lisp does not imply that the design is blocked. It may be a prompt to build the smallest coherent extension.

That power does not make every abstraction a macro:

- prefer a function when it can express the same contract;
- keep macro expansions small and move runtime behavior into testable functions or generic functions;
- evaluate user forms exactly as documented, preserve order, and use generated symbols to avoid accidental variable capture;
- inspect `macroexpand-1`/`macroexpand` output and test both expansion shape and runtime behavior for consequential macros;
- make compile-time dependencies and `eval-when` staging explicit;
- preserve source locations and debuggability where the implementation/tooling permits;
- treat reader macros, code generation, and compile-time execution as security and supply-chain boundaries;
- do not claim static/type guarantees from a macro-generated type layer without compiler diagnostics, runtime checks, and tests that prove the actual contract.

### CLOS and the Metaobject Protocol

Use CLOS before assuming the host object model is fixed. Generic functions, multiple dispatch, method combinations, class redefinition, conditions, and restarts are language-level tools for creating protocols that would require frameworks or generators elsewhere.

The Metaobject Protocol described by *The Art of the Metaobject Protocol* is foundational guidance for understanding and extending object behavior, but the full MOP is not the ANSI Common Lisp specification. When a project depends on MOP behavior, use a documented portability layer where appropriate, identify the supported implementations, and test that matrix.

Authoritative references:

- [Common Lisp HyperSpec](https://www.lispworks.com/documentation/HyperSpec/Front/index_tx.htm) for ANSI Common Lisp semantics.
- [The Art of the Metaobject Protocol](https://ldbeth.sdf.org/The_Art_of_the_Metaobject_Protocol.pdf) for CLOS/MOP design and extension.

Clojure, Scheme, Racket, and other Lisps can provide useful ideas, but they are separate languages with different specifications and runtime contracts. Do not describe a Clojure feature—such as its `agent` reference type—as a Common Lisp feature without an explicit Common Lisp implementation or library.

## REPL-driven development and safe redefinition

The live image is a powerful development environment, not a replacement for source, fresh-process proof, or a source-rebuild proof. A fresh process removes REPL history but may still load cached ASDF FASLs; keep every intended change in source and require recompilation separately when that distinction matters.

Redefinition rules that agents must account for:

- **Macros:** redefining a macro does not rewrite functions already compiled from its old expansion. Recompile every dependent form/system; use a clean ASDF rebuild when the dependency boundary is uncertain.
- **Inline/compiled calls:** function redefinition usually updates subsequent calls through the global function binding, but captured function objects, compiler-macro expansions, and inlined call sites can retain earlier behavior. Recompile dependents when these mechanisms apply.
- **`defvar` versus `defparameter`:** `defvar` initializes only when the variable is unbound and therefore preserves an existing live value. `defparameter` assigns every time it is evaluated or loaded. Choose intentionally—use `defparameter` when reload should reset configuration, and `defvar` when preserving live state is the desired contract.
- **Classes versus structures:** ANSI Common Lisp does not define portable `defstruct` redefinition semantics. Do not use `defstruct` for shapes expected to evolve through hot redefinition; prefer `defclass`, whose class-redefinition and instance-update protocol is designed for evolution.
- **Constants:** do not casually redefine `defconstant` values during live development; portable consequences are constrained and implementation behavior differs.
- **Compile/load staging:** changes to macros, compiler macros, packages, readtables, type definitions, declarations, or `eval-when` behavior widen impact. Restart and rebuild when image history makes the result uncertain.

A productive loop is:

1. explore and redefine in the REPL;
2. immediately preserve the intended definition in source;
3. recompile affected dependents, not only the changed defining form;
4. run focused tests in a fresh process;
5. periodically run the full ASDF test/build path in a fresh process;
6. for macro/staging changes and release evidence, force the repo's declared source-rebuild path rather than relying on cached FASLs.

This keeps the interactive advantage without mistaking a historically mutated image for reproducible evidence.

## Project and package structure

A small library or application usually starts with:

```text
my-system.asd
src/
t/
```

Recommended conventions:

- define a separate test system, commonly `my-system/tests`, and connect it to `asdf:test-system`;
- keep `defpackage` forms explicit and avoid accidental reliance on the current package;
- keep readtables, implementation extensions, and feature expressions visible at system boundaries;
- separate library loading from executable startup so tests and tools can load the system without starting the application;
- use ASDF `program-op` or a documented repo wrapper when the project produces an executable image.

## Reproducibility and dependency guidance

- Pin the implementation version when implementation behavior is part of the build or runtime contract.
- Commit `qlfile` and its lockfile when Qlot owns dependency resolution; run commands through the project-local Qlot environment.
- Do not make CI depend on a developer's `~/.sbclrc`, local Quicklisp checkout, preloaded image, or inherited ASDF source registry.
- `--no-sysinit --no-userinit` disables SBCL init files only; it does not suppress ASDF source-registry or output-translation configuration. Do not describe those flags alone as hermetic.
- For isolated CI, use a reviewed repo wrapper that initializes ASDF with bounded source roots and `:ignore-inherited-configuration`, controls output translations, and loads the declared `.asd` file. A project-local Qlot environment may own dependency resolution, but the repo should still expose one explicit validation entrypoint.
- Review Quicklisp/CLPM source and transitive systems like any other dependency supply chain; do not curl-pipe unreviewed bootstrap code.
- Keep implementation-specific code behind narrow packages and test the promised implementation matrix rather than claiming portability from SBCL-only evidence.

## Code quality

Common Lisp has no universal formatter or linter baseline comparable to `gofmt` or `cargo fmt`.

- Treat compiler notes, warnings, and style warnings according to an explicit repo policy; do not silently discard them.
- Use a deterministic non-interactive load/compile command as the minimum quality gate.
- If the repo chooses a formatter, linter, or static analyzer, pin it and expose separate check and write modes through repo-local wrappers.
- Avoid broad optimization declarations. Measure first, then localize type and optimization declarations to proven hot paths.
- Use conditions and restarts intentionally at recoverable boundaries; do not convert every failure into an unstructured catch-all.

## Command baseline

System names and `.asd` paths are repo-specific. Replace `my-system` and `my-system.asd` below with the repository's declarations, or delegate to its checked-in wrapper. Explicitly loading the repo-owned `.asd` file makes the project system discoverable; it does not by itself isolate transitive dependencies from inherited ASDF configuration.

```bash
# Toolchain sanity
sbcl --version

# Non-interactive repo-system load/compile check
sbcl --noinform --non-interactive --disable-debugger --no-sysinit --no-userinit \
  --eval '(require :asdf)' \
  --eval '(asdf:load-asd (truename "my-system.asd"))' \
  --eval '(asdf:load-system "my-system")'

# Canonical test operation
sbcl --noinform --non-interactive --disable-debugger --no-sysinit --no-userinit \
  --eval '(require :asdf)' \
  --eval '(asdf:load-asd (truename "my-system.asd"))' \
  --eval '(asdf:test-system "my-system")'
```

When Qlot owns dependencies, invoke the same SBCL operations through `qlot exec` or a checked-in script. Prefer a script once isolation, source-registry/output configuration, quoting, bootstrap, warning policy, or multiple implementations make raw shell commands hard to review.

## Testing guidance

- Unit and integration tests: run through `asdf:test-system`, regardless of the underlying framework.
- Targeted tests: use the framework's documented selector through a repo wrapper; keep `just test` or the canonical CI command as the full-suite surface.
- Property testing: add a maintained property-testing library only for invariant-heavy logic that repays the dependency and debugging cost.
- Portability testing: use a CI implementation matrix only for implementations the package actually supports.
- Image/runtime tests: start from a fresh process when initialization order or saved-image history matters; separately force source recompilation when executable delivery or compile-time changes require source-rebuild evidence.

## Applicable cross-language disciplines

Load disciplines when the concern applies:

- `validation` and `testing` for command tiers, focused/full suites, portability matrices, and evidence.
- `dependency-governance` and `security-privacy` for Quicklisp/CLPM/Qlot inputs, bootstrap code, secrets, reader behavior, and supply chain.
- `service-api` for HTTP, RPC, jobs, contracts, auth, migrations, deployment, and rollback.
- `observability` for services, background workers, CLIs, and image/runtime evidence.
- `performance` for profiling, declarations, compilation strategy, latency/throughput/memory/startup budgets, and regression gates.
- `local-first-data` and `data-governance` for files, databases, migrations, projections, retention, and canonical data.
- `domain-modeling` and `design-patterns` for vocabulary, generic functions, protocols, state transitions, and recurring solution shapes.
- `release-package` for ASDF systems, executable images, containers, changelogs, compatibility, and artifact provenance.
- `documentation` for package/system boundaries, generated docs, and operational commands.
- `specification-and-dsls` when macros, reader extensions, compiler macros, MOP customization, or declarative forms create a project language/DSL; document expansion, staging, error, and compatibility contracts.

## Conditionally loaded addenda

### Justfile addendum

Read the lane-specific Justfile addendum only when:
- `Justfile` is missing
- the standardized targets are absent or drifting
- you are explicitly establishing or reconciling the repo-local `Justfile`

Otherwise, do not load the addendum by default.

Companion doc:
- `engineering-common-lisp.justfile.md`
