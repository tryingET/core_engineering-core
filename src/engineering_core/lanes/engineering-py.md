---
summary: "Python engineering lane for ecosystem-specific tooling, commands, and implementation defaults."
read_when:
  - "Working in a repo or package whose selected engineering-core lane is py."
  - "Choosing Python tooling, command surfaces, quality defaults, or ecosystem-specific validation."
type: "guide"
---

### **Python engineering lane**

The philosophy remains: **Everything is a file.** The state of your project is declarative, version-controlled, and instantly reproducible.

| Category | The Latest & Greatest Tooling |
| :--- | :--- |
| **1. Core Engine** | **`uv`**: The complete Python project and package manager. Replaces `pyenv`, `venv`, `pip`, and `pip-tools`. Manages Python installation, virtual environments (`uv venv`), dependency management (`uv add`), locking (`uv lock`), and installation (`uv sync`). |
| **2. Web/API Framework** | **FastAPI**: The premier choice for building performant, type-safe APIs with Python. |
| **3. Data Validation & Settings**| **Pydantic V2**: The core of modern Python data handling. Used by FastAPI for automatic request/response validation and contract generation. Also used for type-safe settings management from environment variables. |
| **4. Application Server** | **Granian**: A Rust-based, high-performance ASGI server that outpaces traditional servers like Uvicorn, aligning with the lane's focus on speed. |
| **5. Data Layer** | **PostgreSQL** • **SQLAlchemy 2.x** (with async support) • **Alembic** (for schema migrations). |
| **6. Cache / Job Queue** | **Valkey**: The community-driven, open-source successor to Redis. Used for both caching and as a message broker for Celery. |
| **7. Async Task Processing** | **Celery**: The battle-tested framework for running background tasks, using the Valkey broker. |
| **8. Code Quality** | **`Ruff`** (for linting & formatting) • **`ty`** (for strict type checking). Both are configured directly in `pyproject.toml`. |
| **9. Testing Suite** | **pytest** • **Hypothesis** (for property-based testing) • **pytest-bdd** (for Gherkin/BDD workflows when executable scenarios are useful) • **schemathesis** (for OpenAPI contract testing). |
| **10. Observability** | **OpenTelemetry SDK**: Integrated directly into FastAPI for traces and metrics. Exports to an **OTel Collector** for processing and forwarding. |
| **11. Deployment** | **Docker**: Using multi-stage builds with `uv sync` for creating minimal, secure, and rapidly built images. Deployed to modern platforms like **Fly.io** or **Cloud Run**. |

---

### Applicable cross-language disciplines

Load disciplines when the concern applies:

- `validation` and `testing` for tiering, command evidence, and test selection.
- `dependency-governance` and `security-privacy` for dependency, secret, and privacy review.
- `service-api` for FastAPI/service boundaries, request/response contracts, auth, idempotency, workers, migrations, deployment, and rollback.
- `observability` for FastAPI/services, workers, and runtime evidence.
- `performance` for profiling, latency/memory/startup budgets, benchmark hygiene, and regression gates.
- `ai-ml` for model assets, inference boundaries, evals, dataset/prompt/model provenance, safety/privacy claims, and reproducibility.
- `data-governance` for canonical data, schemas, identifiers, lineage, migrations/backfills, projections, retention, and quality.
- `domain-modeling` for vocabulary, invariants, workflows, state transitions, and anti-corruption boundaries.
- `design-patterns` when reviewing named patterns such as factory, adapter, actor, repository, saga, state machine, or policy object.
- `local-first-data` for durable local files/DBs, migrations, projections, and sync.
- `design-system` and `accessibility` for generated HTML/docs, dashboards, or user-facing UI.
- `release-package` for packages/wheels/containers, changelogs, artifact provenance, compatibility, and rollback.
- `documentation` for docs authority, generated outputs, and front matter.

### **Project Scripts (`pyproject.toml`)**

Define Python-native tasks in `pyproject.toml` so they are discoverable and runnable with `uv`. When a repo adopts the cross-language `just` command surface, keep `Justfile` recipes as thin aliases over these Python-native commands or existing repo scripts.

```toml
[tool.uv.scripts]
dev = "granian src.hello_svc.asgi:app --reload"
test = "pytest"
lint = "ruff check ."
format = "ruff format ."
```

---

### **Testing & Templating Guidance**

- Default unit/integration runner: **pytest**
- Property-based testing implementation: **Hypothesis**
- Behavior/Gherkin implementation: **pytest-bdd** when `disciplines/testing.md` says executable scenarios are justified
- OpenAPI contract testing implementation: **schemathesis** when API schema behavior needs executable coverage
- Text/config/html templating: **Jinja2** when the repo benefits from reusable template files or user-visible rendering surfaces
- Prefer plain Python functions / f-strings for small local formatting tasks

---

### **Skeleton Commands (The Developer Workflow)**

This is the complete lifecycle, from project creation to daily work.

*   **Initialize a New Project:**
    `uv init`
*   **Create Virtual Environment:** (Handled automatically, but can be done manually)
    `uv venv`
*   **Manage Project Dependencies:**
    *   Add a production dependency: `uv add fastapi`
    *   Add a development-only dependency: `uv add --dev pytest`
    *   Remove a dependency: `uv remove pytest`
*   **Synchronize Environment from Lockfile:** (Installs all dependencies from `uv.lock`)
    `uv sync`
*   **Update All Dependencies in Lockfile:**
    `uv sync --upgrade`
*   **Run Project Scripts:** (The primary way to interact with your project)
    *   Start the dev server: `uv run dev`
    *   Run tests: `uv run test`
    *   Run quality checks: `uv run lint && uv run format`
*   **Ad-Hoc Script Management:** (For utility scripts without polluting the main environment)
    *   Add dependencies to a script: `uv add --script scripts/my_script.py 'pandas' 'polars'`
    *   Run a script with its managed dependencies: `uv run --script scripts/my_script.py`
*   **Manage Standalone Tools:** (Install tools like `pre-commit` into a shared, isolated environment)
    *   Install a tool: `uv tool install pre-commit`
    *   Run an installed tool: `uv tool run pre-commit install`
    *   List installed tools: `uv tool list`

---

### **Test Execution Pattern (Critical for Executors)**

The correct way to run tests with `uv` and `pytest`:

*   **Run all tests in a directory:**
    `uv run python -m pytest tests/`
*   **Run a specific test file:**
    `uv run python -m pytest tests/integration/test_file.py`
*   **Run with verbose output:**
    `uv run python -m pytest tests/integration/test_file.py -v`
*   **Run with short traceback:**
    `uv run python -m pytest tests/ -v --tb=short`
*   **Run a specific test class:**
    `uv run python -m pytest tests/integration/test_file.py::TestClassName`
*   **Run a specific test method:**
    `uv run python -m pytest tests/integration/test_file.py::TestClassName::test_method_name`

**IMPORTANT**: Do NOT use:
- ❌ `pytest tests/` (not in global Python)
- ❌ `uv run -m pytest coordination.tests.module` (module paths don't work)
- ❌ `python -m pytest` (wrong Python environment)

**Always use**: `uv run python -m pytest <file_path>`

**Common Test Dependencies**:
```bash
# Add test dependencies
uv add --dev pytest
uv add --dev pytest-asyncio  # For async tests
uv add --dev pytest-bdd      # For Gherkin/BDD scenarios
uv add --dev pytest-cov       # For coverage reports
uv add --dev pytest-mock      # For mocking
```

---
#### **Service SLO seed**

Use `disciplines/observability.md` for runtime evidence and SLO discipline. Example seed for Python API services after repo-local acceptance:

- SLI latency: p95 `< 200ms` on key `/api/*` paths
- Availability: `99.9%`
- Error budget policy: freeze feature deploys if budget < 25% until back above threshold

---

#### **Fit with 6E → CLARITY**
- **Edges** = APIs/events/files—drive **COMPLEXITY points** and test scope.
- **Constraints** (MUST/MUST‑NOT) codified in contracts + CI gates.
- **Traceability**: decision cards + OpenTelemetry traces provide explainability.

## Conditionally loaded addenda

### Justfile addendum

Read the lane-specific Justfile addendum only when:
- `Justfile` is missing
- the standardized targets are absent or drifting
- you are explicitly establishing or reconciling the repo-local `Justfile`

Otherwise, do not load the addendum by default.

Companion doc:
- `engineering-py.justfile.md`
