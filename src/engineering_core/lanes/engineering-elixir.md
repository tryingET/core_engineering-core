---
summary: "Elixir engineering lane for ecosystem-specific tooling, commands, and implementation defaults."
read_when:
  - "Working in a repo or package whose selected engineering-core lane is elixir."
  - "Choosing Elixir tooling, command surfaces, quality defaults, or ecosystem-specific validation."
type: "guide"
---

### **Elixir engineering lane**

The philosophy remains: **Everything important is explicit, supervised, and observable.** Keep pure business logic in plain modules, reserve processes for stateful boundaries, and make failure handling part of the design instead of an afterthought.

| Category | The Latest & Greatest Tooling |
| :--- | :--- |
| **1. Toolchain & Build** | **`mix` + `hex` + `rebar3`**: core Elixir workflow for project creation, dependencies, compilation, tasks, and releases. Pin Elixir/OTP with **`mise`** or `.tool-versions` where the repo standardizes toolchain versions. |
| **2. Web/API Framework** | **Phoenix 1.8+** with **Bandit**: the default for HTTP APIs and web apps. Strong routing, plugs, channels, telemetry hooks, and battle-tested operational behavior. |
| **3. Realtime / Server-Rendered UI** | **Phoenix LiveView + HEEx**: default when the product benefits from rich real-time UI without pushing a large SPA to the browser. Use client-side frameworks only when the interaction model truly demands them. |
| **4. Validation & Contracts** | **Ecto Changesets** for external input and persistence boundaries • **NimbleOptions** for runtime/config option validation • **OpenApiSpex** when REST contracts must be generated or enforced explicitly. |
| **5. Data Layer** | **PostgreSQL** • **Ecto** / **Ecto SQL** • **Ecto Migrations**. Use **Ecto.Multi** for multi-step state transitions that must stay transactional. |
| **6. HTTP / External Integrations** | **Req** as the default HTTP client, backed by **Finch** where pooled, supervised outbound HTTP matters. Wrap third-party calls behind behaviours so adapters stay replaceable. |
| **7. Background Jobs & Workflows** | **Oban**: default for durable jobs, retries, scheduling, and operational visibility. Prefer Oban over introducing a separate queueing system unless cross-language or platform constraints force it. |
| **8. Code Quality** | **`mix format`** • **Credo** • **Dialyxir/Dialyzer** • **Sobelow** for Phoenix/web security review. Treat warnings as real design feedback, not cosmetic noise. |
| **9. Testing Suite** | **ExUnit** • **StreamData** for property-based testing • **Mox** for behaviour-based mocks • **Bypass** for external HTTP simulations • **Phoenix.ConnTest** / **Phoenix.LiveViewTest** for web boundaries. |
| **10. Observability** | **Telemetry** events everywhere important • **OpenTelemetry** exporters for traces/metrics • **Phoenix LiveDashboard** for runtime introspection. Emit events at workflow boundaries, not just infrastructure edges. |
| **11. Deployment** | **Mix releases** in Docker images. Default to immutable release artifacts, runtime config via environment, and rolling deploys on **Fly.io**, **Render**, **Cloud Run**, or k8s depending on operational complexity. |


### Applicable cross-language disciplines

Load disciplines when the concern applies:

- `validation` and `testing` for command tiers, ExUnit/property/E2E choices, and evidence.
- `dependency-governance` and `security-privacy` for Hex deps, secrets, auth, and deployment risk.
- `observability` for Telemetry/OpenTelemetry, LiveDashboard, services, and runtime evidence.
- `local-first-data` for Ecto persistence, migrations, projections, imports/exports, and sync.
- `design-system` and `accessibility` for Phoenix/LiveView/HEEx and generated docs/UI.
- `documentation` for docs authority and generated artifacts.

---

### **OTP-First Patterns (The Elixir Way)**

```elixir
# 1. Prefer tagged tuples for domain flow
@spec create_user(map()) :: {:ok, User.t()} | {:error, Ecto.Changeset.t()}
def create_user(attrs) do
  %User{}
  |> User.changeset(attrs)
  |> Repo.insert()
end

# 2. Use behaviours at integration boundaries
#    This keeps adapters swappable and tests cheap.
defmodule BillingGateway do
  @callback create_customer(map()) :: {:ok, map()} | {:error, term()}
end

# 3. Use Ecto.Multi for transactional workflows
Ecto.Multi.new()
|> Ecto.Multi.insert(:user, User.changeset(%User{}, attrs))
|> Ecto.Multi.insert(:audit_log, AuditLog.changeset(%AuditLog{}, %{event: "user_created"}))
|> Repo.transaction()

# 4. Add telemetry at meaningful workflow edges
:telemetry.execute(
  [:my_app, :billing, :customer_created],
  %{count: 1},
  %{user_id: user.id, provider: :stripe}
)

# 5. Only introduce GenServer when you truly own state, a resource, or lifecycle
#    Otherwise, keep it as a plain module.
```

**Default design bias:**
- Plain modules first
- Processes when state/resource ownership is real
- Behaviours at external boundaries
- `{:ok, value}` / `{:error, reason}` over exception-driven domain logic
- Supervision trees explicit and boring
- Telemetry on important transitions

---

### **Project Aliases (`mix.exs`)**

Define common workflows as aliases so contributors and CI both use the same commands.

```elixir
def project do
  [
    app: :my_app,
    version: "0.1.0",
    elixir: "~> 1.17",
    start_permanent: Mix.env() == :prod,
    aliases: aliases(),
    deps: deps()
  ]
end

defp aliases do
  [
    setup: ["deps.get", "ecto.setup"],
    "ecto.setup": ["ecto.create", "ecto.migrate", "run priv/repo/seeds.exs"],
    "ecto.reset": ["ecto.drop", "ecto.setup"],
    quality: ["format --check-formatted", "credo --strict", "dialyzer"],
    ci: ["deps.get", "compile --warnings-as-errors", "test", "format --check-formatted", "credo --strict"]
  ]
end
```

For Phoenix projects with assets, extend `setup` / `ci` with asset install and build commands instead of inventing a parallel task runner.

---

### **Skeleton Commands (The Developer Workflow)**

This is the complete lifecycle, from project creation to daily work.

*   **Initialize a supervised OTP app:**
    `mix new my_app --sup`
*   **Initialize a Phoenix app:**
    `mix phx.new my_app --database postgres`
*   **Fetch project dependencies:**
    `mix deps.get`
*   **Compile the project:**
    `mix compile`
*   **Run the test suite:**
    `mix test`
*   **Format code:**
    `mix format`
*   **Run linting:**
    `mix credo --strict`
*   **Run static analysis:**
    `mix dialyzer`
*   **Prepare local database:**
    `mix ecto.setup`
*   **Reset local database:**
    `mix ecto.reset`
*   **Start Phoenix server:**
    `mix phx.server`
*   **Start Phoenix server with IEx attached:**
    `iex -S mix phx.server`
*   **Run a one-off script inside the app context:**
    `mix run priv/repo/seeds.exs`
*   **Open an interactive shell with the app booted:**
    `iex -S mix`
*   **Build a production release:**
    `MIX_ENV=prod mix release`

**Dependency management pattern:**
- add dependency by editing `mix.exs`
- then run `mix deps.get`
- when upgrading, prefer targeted updates first: `mix deps.update phoenix oban`
- only use `mix deps.update --all` when you intend a full dependency sweep

---

### **Test Execution Pattern (Critical for Executors)**

The correct way to run tests in Elixir:

*   **Run all tests:**
    `mix test`
*   **Run a specific test file:**
    `mix test test/my_app/accounts_test.exs`
*   **Run a specific line in a test file:**
    `mix test test/my_app/accounts_test.exs:42`
*   **Run only previously failed tests:**
    `mix test --failed`
*   **Run stale tests first:**
    `mix test --stale`
*   **Run with coverage:**
    `mix test --cover`
*   **Run with a fixed seed for reproducibility:**
    `mix test --seed 12345`
*   **Trace a single test synchronously:**
    `mix test test/my_app/accounts_test.exs --trace`

**Phoenix-specific test helpers:**
- controller / HTTP boundary tests: `Phoenix.ConnTest`
- LiveView interaction tests: `Phoenix.LiveViewTest`
- outbound HTTP simulation: `Bypass`
- behaviour-based integration doubles: `Mox`
- property testing for invariants: `StreamData`

### **Testing & Template Guidance**

- Default unit/integration runner: `ExUnit`
- Property testing: `StreamData`
- Behavior/Gherkin testing: no default BDD/Gherkin package; only add one when cross-role executable scenarios clearly justify the maintenance cost
- Server-rendered HTML/UI templates: `HEEx` (plus Phoenix function components)
- Text/email/config templates: `EEx` when a template file is clearer than plain functions
- Prefer plain modules/functions over template indirection when rendering is simple

**IMPORTANT**: Do NOT use:
- ❌ `elixir test/my_test.exs` (wrong execution path)
- ❌ `iex test/my_test.exs` (does not boot the project correctly)
- ❌ ad-hoc shell scripts when `mix test` can target the exact file/line

**Always use**: `mix test <file_or_line_target>`

---

### **Phoenix / OTP Operational Defaults**

- Prefer **Phoenix + Bandit** over building raw Plug stacks unless the repo is intentionally minimal.
- Prefer **LiveView** before defaulting to SPA complexity for internal tools and workflow-heavy apps.
- Prefer **Oban** for reliable async work before reaching for Redis-backed job systems.
- Prefer **Req** at HTTP boundaries; wrap third-party integrations behind behaviours.
- Prefer **umbrella apps** only when bounded subsystems truly have separate ownership or lifecycle. Do not split into umbrellas just to look “enterprisey.”
- Prefer **runtime config** (`config/runtime.exs`) for deploy-time values and keep compile-time config minimal.

---

### **Deployment with Docker + Releases**

**Dockerfile:**
```dockerfile
FROM hexpm/elixir:1.17.3-erlang-27.2-debian-bookworm-20241007 AS build

RUN apt-get update && apt-get install -y --no-install-recommends build-essential git \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN mix local.hex --force && mix local.rebar --force

COPY mix.exs mix.lock ./
COPY config config
RUN mix deps.get --only prod
RUN mix deps.compile

COPY lib lib
COPY priv priv
COPY assets assets
RUN MIX_ENV=prod mix compile
RUN MIX_ENV=prod mix release

FROM debian:bookworm-slim AS runner
RUN apt-get update && apt-get install -y --no-install-recommends openssl libstdc++6 ncurses-bin \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=build /app/_build/prod/rel/my_app ./

ENV HOME=/app
CMD ["bin/my_app", "start"]
```

Default production shape:
- build release once
- inject runtime config via env vars / secrets manager
- run database migrations as an explicit deploy step
- ship logs/metrics/traces to central observability, not local files only

---

### **Service SLO seed**

Use `disciplines/observability.md` for runtime evidence and SLO discipline. Example seed for Elixir service repos after repo-local acceptance:

- **SLI latency**: p95 `< 150ms` on key synchronous API paths
- **Availability**: `99.9%`
- **Error budget policy**: freeze feature deploys if budget < 25% until service health recovers
- **Queue health**: Oban queue latency and retry depth must be visible and alertable
- **Warnings policy**: treat compiler + Credo + Dialyzer warnings as backlog items at minimum, and as merge blockers for critical paths

---

### **Fit with 6E → CLARITY**

- **Edges**: Phoenix routes, message boundaries, behaviours, and DB transactions define system edges clearly.
- **Constraints**: changesets, options validation, and supervision trees encode what is allowed.
- **Boundaries**: OTP processes own state/resources explicitly instead of hiding lifecycle in incidental objects.
- **Assumptions**: telemetry + tagged tuples make success/failure paths inspectable.
- **Dependencies**: Mix/Hex keeps dependency state declarative and reproducible.
- **Exceptions**: retries, backoff, and supervisors make failure handling operational rather than magical.
- **Traceability**: Telemetry, OpenTelemetry, and release/versioned config provide explainability across the runtime.

## Conditionally loaded addenda

### Justfile addendum

Read the lane-specific Justfile addendum only when:
- `Justfile` is missing
- the standardized targets are absent or drifting
- you are explicitly establishing or reconciling the repo-local `Justfile`

Otherwise, do not load the addendum by default.

Companion doc:
- `engineering-elixir.justfile.md`
