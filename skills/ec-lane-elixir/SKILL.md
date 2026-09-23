---
name: ec-lane-elixir
description: "[ec-lane] Elixir engineering lane for ecosystem-specific tooling, commands, and implementation defaults. Load when: Working in a repo or package whose selected engineering-core lane is elixir.; Choosing Elixir tooling, command surfaces, quality defaults, or ecosystem-specific validation."
---

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
- `service-api` for Phoenix/API/event/job boundaries, contracts, auth, idempotency, migrations, deployment, and rollback.
- `observability` for Telemetry/OpenTelemetry, LiveDashboard, services, and runtime evidence.
- `performance` for latency/throughput/memory/startup budgets, profiling, and regression gates.
- `ai-ml` when Elixir orchestrates inference, LLM/tooling workflows, or model-backed services.
- `data-governance` for canonical data, schemas, identifiers, lineage, migrations/backfills, projections, retention, and quality.
- `domain-modeling` for vocabulary, invariants, workflows, state transitions, and anti-corruption boundaries.
- `design-patterns` when reviewing named patterns such as factory, adapter, actor, repository, saga, state machine, or policy object.
- `local-first-data` for Ecto persistence, migrations, projections, imports/exports, and sync.
- `release-package` for Mix releases/packages/containers, changelogs, artifact provenance, compatibility, and rollback.
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
|> Repo.transact()

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

### **Project Aliases and Quality Gates (`mix.exs`)**

Define common workflows as aliases so contributors and CI both use the same commands. `def cli` sets the environment an alias runs in: without `preferred_envs: [ci: :test]`, `mix ci` aborts with `"mix test" is running in the "dev" environment`. Keep `mix.exs` itself `mix format`-clean, or the alias fails its own format check.

**mix.exs:**
```elixir
defmodule MyApp.MixProject do
  use Mix.Project

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

  def cli do
    [preferred_envs: [ci: :test]]
  end

  def application do
    [
      extra_applications: [:logger],
      mod: {MyApp.Application, []}
    ]
  end

  defp deps do
    [
      {:credo, "~> 1.7", only: [:dev, :test], runtime: false},
      {:dialyxir, "~> 1.4", only: [:dev, :test], runtime: false}
    ]
  end

  defp aliases do
    [
      quality: ["format --check-formatted", "credo --strict", "dialyzer"],
      ci: [
        "deps.get --check-locked",
        "compile --warnings-as-errors",
        "format --check-formatted",
        "credo --strict",
        "test"
      ]
    ]
  end
end
```

Commit `mix.lock`; `--check-locked` fails when it would change. Phoenix/Ecto apps: `mix phx.new` generates `setup` and `ecto.*` aliases (they fail in apps without Ecto) and a `precommit` alias with its own `preferred_envs`; keep those, add `{:sobelow, "~> 0.13", only: [:dev, :test], runtime: false}`, and extend `ci` with `sobelow` and the asset build instead of inventing a parallel task runner.

**.tool-versions:**
```text
elixir 1.20.2-otp-29
erlang 29.0.5
```

mise/asdf read `.tool-versions`, and CI's `erlef/setup-beam` can read it with `version-file: .tool-versions`. The Docker image below uses the same Elixir and OTP (it's the newest Elixir 1.20.2 image; hexpm publishes no 1.20.2 image on OTP 29.0.6).

**Quality gates:**
```bash
# toolchain
elixir --version | grep -F 'Elixir 1.20.2 (compiled with Erlang/OTP 29)'
# deps
mix deps.get --check-locked
# fmt
mix format --check-formatted
# compile
MIX_ENV=test mix compile --warnings-as-errors
# lint
mix credo --strict
# typecheck
mix dialyzer
# test
mix test
# ci
mix ci
```

`scripts/lane-conformance.py elixir` runs these gates, plus `docker build --check` on the Dockerfile below, on a fixture app at every engineering-core release.

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
- Prefer **runtime config** (`config/runtime.exs`) for deploy-time values and keep compile-tim

[projected skill truncated; read the full doc in engineering-core]
