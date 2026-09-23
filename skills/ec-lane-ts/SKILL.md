---
name: ec-lane-ts
description: "[ec-lane] TypeScript engineering lane for ecosystem-specific tooling, commands, and implementation defaults. Load when: Working in a repo or package whose selected engineering-core lane is ts.; Choosing TypeScript tooling, command surfaces, quality defaults, or ecosystem-specific validation."
---

---
summary: "TypeScript engineering lane for ecosystem-specific tooling, commands, and implementation defaults."
read_when:
  - "Working in a repo or package whose selected engineering-core lane is ts."
  - "Choosing TypeScript tooling, command surfaces, quality defaults, or ecosystem-specific validation."
type: "guide"
---

### **TypeScript engineering lane**

The philosophy remains: **Everything is a file.** The state of your project is declarative, version-controlled, and instantly reproducible. Following Matt Pocock's type-safe patterns: **Make impossible states impossible.**

| Category | The Latest & Greatest Tooling |
| :--- | :--- |
| **1. Runtime & Package Manager** | **`Bun`**: The all-in-one JavaScript runtime. Replaces Node.js, npm/yarn/pnpm. Lightning-fast startup, built-in TypeScript, testing, and bundling. Native SQLite, WebSockets, and .env support. |
| **2. Type System** | **TypeScript 5.5+**: With `strict: true`, `exactOptionalPropertyTypes`, `noUncheckedIndexedAccess`. Use type predicates, branded types, and const assertions everywhere. |
| **3. Web/API Framework** | **Hono**: Ultra-fast, type-safe, edge-first framework. Works everywhere (Bun, Node, Cloudflare Workers). Built-in RPC mode for end-to-end type safety. |
| **4. Data Validation & Contracts** | **Zod**: Schema-first validation with TypeScript inference. Use `z.infer<>` for automatic type generation. Integrates perfectly with Hono for request/response validation. |
| **5. Data Layer** | **PostgreSQL** • **Drizzle ORM** (fully type-safe, SQL-like) • **Drizzle Kit** (for migrations). Alternative: **Kysely** for query builder purists. |
| **6. Cache / Queue** | **Valkey**: Open-source Redis successor. Use with **BullMQ** for type-safe job queues with Zod schemas for job payloads. |
| **7. Code Quality** | **Biome**: Single tool for linting, formatting, and import sorting. Faster than ESLint + Prettier combined. Zero config, sensible defaults. |
| **8. Testing Suite** | **Bun Test**: Built into Bun, Jest-compatible but 10x faster. **Vitest** as alternative for complex scenarios. **fast-check** for property-based testing. **Cucumber.js** for Gherkin/BDD workflows when executable user scenarios matter. |
| **9. Observability** | **OpenTelemetry SDK**: With Hono middleware for automatic tracing. Export to **Jaeger** or **Tempo** for distributed tracing. |
| **10. Deployment** | **Docker**: Multi-stage builds with `bun install --frozen-lockfile`. Deploy to **Fly.io**, **Railway**, or **Cloudflare Workers** (Hono's native environment). |
| **11. Monorepo Tools** | **Turborepo**: For build orchestration. **Changesets** for versioning. Keep it simple - Bun workspaces handle most needs. |

### Baseline vs service defaults

The baseline TypeScript lane is: package-manager/runtime discipline, strict TypeScript, deterministic format/lint, tests, typecheck, lockfile installs, and reviewed dependency changes.

For browser apps, SPAs, local-first frontend user data, camera/media UI, or design-heavy frontend work, also load `engineering-ts.frontend.md` plus applicable disciplines. Do not add frontend-only dependencies to backend-only packages, small utilities, static pages, or libraries that do not own interactive UI state.

Hono, Zod, Drizzle, BullMQ, OpenTelemetry, Turborepo, Changesets, and deployment targets are service/workspace defaults only when the repo actually needs those capabilities. Do not add the full web/API dependency set to small libraries, CLIs, scripts, package-only repos, or one-off tools unless the repo-local contract justifies it.

---

### **Type-Safe Patterns (The Matt Pocock Way)**

```typescript
// 1. Branded Types for Domain Modeling
type UserId = string & { __brand: "UserId" }
type Email = string & { __brand: "Email" }

const createUserId = (id: string): UserId => {
  if (!id.match(/^user_[a-z0-9]{8}$/)) {
    throw new Error("Invalid user ID format")
  }
  return id as UserId
}

// 2. Const Assertions for Literals
const ROLES = ["admin", "user", "guest"] as const
type Role = typeof ROLES[number] // "admin" | "user" | "guest"

// 3. Type Predicates for Narrowing
const isError = <T>(result: T | Error): result is Error => {
  return result instanceof Error
}

// 4. Result Types (No Exceptions)
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E }

// 5. Exhaustive Switch with Never
type Action =
  | { type: "INCREMENT"; by: number }
  | { type: "DECREMENT"; by: number }
  | { type: "RESET" }

const reducer = (action: Action): number => {
  switch (action.type) {
    case "INCREMENT": return action.by
    case "DECREMENT": return -action.by
    case "RESET": return 0
    default: {
      const _exhaustive: never = action
      throw new Error(`Unhandled action: ${JSON.stringify(action)}`)
    }
  }
}
```

---

### Applicable cross-language disciplines

Load disciplines when the concern applies:

- `validation` and `testing` for command tiers and test selection.
- `dependency-governance` and `security-privacy` for dependency and supply-chain risk.
- `service-api` for HTTP/RPC/event boundaries, schema contracts, auth, idempotency, jobs, migrations, deployment, and rollback.
- `observability` for service/runtime evidence.
- `performance` for latency, frontend frame budgets, memory/startup, benchmark evidence, and regression gates.
- `ai-ml` for browser/server ML, model assets, inference boundaries, prompts, evals, and safety/privacy claims.
- `data-governance` for canonical data, schemas, identifiers, lineage, migrations/backfills, projections, retention, and quality.
- `domain-modeling` for vocabulary, invariants, workflows, state transitions, and anti-corruption boundaries.
- `design-patterns` when reviewing named patterns such as factory, adapter, actor, repository, saga, state machine, or policy object.
- `local-first-data` for durable local state, migrations, and sync.
- `design-system` and `accessibility` with `engineering-ts.frontend.md` for browser/product UI.
- `release-package` for npm/packages, changelogs, artifact provenance, compatibility, and rollback.
- `documentation` for docs authority, generated projections, and read triggers.

### **Project Configuration (`bunfig.toml` + `biome.json`)**

**bunfig.toml:**
```toml
# Bun configuration (Bun reads bunfig.toml only; a bun.toml file is silently ignored)
[install]
# Always use exact versions
exact = true
# Deterministic installs
frozenLockfile = true

[run]
# Keep CI/review contexts explicit; enable autoInstall only in a repo-local override
# when convenience is worth the supply-chain tradeoff.
autoInstall = false
```

**Recommended global Bun freshness gate (`~/.bunfig.toml`):**
```toml
[install]
minimumReleaseAge = 604800  # 7 days
```

`bun test` finds `*.test.ts` files anywhere outside `node_modules`. Don't set `[test] root`: `root = "./src"` silently skips tests in `test/`, which this lane's tsconfig includes.

Coverage is a gate only when the repo accepts it. Opt in with:

```toml
[test]
coverage = true
coverageThreshold = { lines = 0.8, functions = 0.8 }
```

Set both keys explicitly (they're plural). A misspelled key such as `line` is silently ignored and disables the threshold, and a failing threshold exits 1 without a message; the coverage table shows which column fell short.

Use this when you want Bun to avoid resolving npm packages published in the last 7 days. This affects new resolution, not already-pinned lockfile entries.

**biome.json:**
```json
{
  "$schema": "https://biomejs.dev/schemas/2.5.14/schema.json",
  "assist": { "actions": { "source": { "organizeImports": "on" } } },
  "linter": {
    "enabled": true,
    "rules": {
      "preset": "recommended",
      "suspicious": {
        "noExplicitAny": "error",
        "noImplicitAnyLet": "error",
        "useAwait": "error"
      },
      "style": {
        "noNonNullAssertion": "error",
        "useConst": "error",
        "useTemplate": "error",
        "useNodejsImportProtocol": "error"
      },
      "correctness": {
        "noUnusedVariables": "error",
        "noUnusedImports": "error",
        "useExhaustiveDependencies": "error"
      },
      "complexity": {
        "useLiteralKeys": "off",
        "noBannedTypes": "error",
        "noStaticOnlyClass": "error",
        "noThisInStatic": "error"
      },
      "performance": {
        "noAccumulatingSpread": "error",
        "noDelete": "error"
      }
    }
  },
  "formatter": {
    "enabled": true,
    "formatWithErrors": false,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100,
    "lineEnding": "lf"
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "double",
      "jsxQuoteStyle": "double",
      "semicolons": "asNeeded",
      "trailingCommas": "all",
      "arrowParentheses": "always"
    }
  },
  "files": {
    "includes": ["**", "!**/node_modules", "!**/dist", "!**/.turbo", "!**/coverage"]
  }
}
```

This config targets Biome 2.x; keep `$schema` equal to the exact pinned `@biomejs/biome` version. Repos still on Biome 1.9.x can run `biome migrate --write` after bumping, which rewrites `organizeImports` to `assist` and `files.ignore` to `files.includes`.

`complexity/useLiteralKeys` is off on purpose. The tsconfig below sets `noPropertyAccessFromIndexSignature`, which requires `obj["key"]` for index-signature types (for example `process.env["X"]`), while `useLiteralKeys` demands `obj.key`. The two can't both pass on the same line. The TypeScript option wins because it marks dynamic lookups the type system can't check; the Biome rule is only style.

### Biome as the TypeScript quality-tool realization

Biome is the TypeScript/JavaScript implementation of the cross-lane quality-tool pattern:

- checked-in config (`biome.json`)
- deterministic CLI invocation through the repo package manager
- write/fix mode for local edits (`biome check --write` / `biome format --write`)
- CI-safe check mode (`biome check .`)
- generated/vendor/build-output ignores
- no editor-only enforcement or ambient global install assumption

Treat Biome as the default TypeScript quality surface, not a reason to add unrelated web/API dependencies.

**tsconfig.json:**
```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "compilerOptions": {
    // Type Safety: Matt Pocock's Strict Config
    "strict": true,
    "exactOptionalPropertyTypes": true,
    "noUncheckedIndexedAccess": true,
    "noPropertyAccessFromIndexSignature": true,

    // Module Resolution
    "module": "ESNext",
    "target": "ES2022",
    "moduleResolution": "bundler",
    "moduleDetection": "force",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,

    // Emit Configuration
    "noEmit": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,

    // Path Aliases (resolved relative to this file; TypeScript 7 rejects baseUrl)
    "paths": {
      "@/*": ["./src/*"],
      "@/test/*": ["./test/*"]
    },

    // Type Roots
    "types": ["bun-types"],

    // JSX (if needed)
    "jsx": "react-jsx",
    "jsxImportSource": "hono/jsx"
  },
  "include": ["src/**/*", "test/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

---

### **Skeleton Commands (The Developer Workflow)**

This is the complete lifecycle, from project creation to daily work.

*   **Initialize a New Project:**
    `bun init` (creates package.json, tsconfig.json, and basic structure)
*   **Install Dependencies:**
    *   Add service dependencies: `bun add hono zod drizzle-orm`
    *   Add a development dependency: `bun add -d @types/bun vitest`
    *   Remove a dependency: `bun remove package-name`
*   **Install All Dependencies from Lockfile:**
    `bun install --frozen-lockfile`
*   **Update Dependencies:**
    `bun update` (updates all to latest within semver range)
*   **Run Scripts:** (Defined in package.json)
    *   Start dev server: `bun run dev`
    *   Run tests: `bun test`
    *   Type chec

[projected skill truncated; read the full doc in engineering-core]
