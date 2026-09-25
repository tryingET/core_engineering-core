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
| **8. Code Quality** | **`Ruff`** (for linting & formatting) • **`ty`** (for type checking; ty has no strict mode, so the lane sets every rule to `error` and fails on warnings). Both are pinned dev dependencies configured in `pyproject.toml` (below). |
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

### **Project configuration and quality gates (`pyproject.toml`)**

uv has no task runner. Don't add a `[tool.uv.scripts]` table: uv rejects it (`Failed to parse pyproject.toml during settings discovery … unknown field scripts`) and then ignores **every other** project-level `[tool.uv]` setting, including a project `exclude-newer` quarantine; `uv run lint` fails with `Failed to spawn: lint` and `uv run test` silently runs `/usr/bin/test`. Put tasks in the `Justfile` (thin recipes over the commands below) and reserve `[project.scripts]` for real console entry points. The user-level quarantine in `~/.config/uv/uv.toml` is unaffected.

**pyproject.toml:**
```toml
[project]
name = "example-service"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = []

[dependency-groups]
dev = ["pytest==9.1.1", "ruff==0.16.8", "ty==0.0.81"]

[build-system]
requires = ["uv_build>=0.12.17,<0.13.0"]
build-backend = "uv_build"

[tool.uv]
required-version = ">=0.12.0"
exclude-newer = "7 days"

[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM", "RUF"]

[tool.ty.environment]
python-version = "3.13"

[tool.ty.rules]
all = "error"

[tool.ty.terminal]
error-on-warning = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = ["--strict-markers", "--strict-config"]
```

Rename the project. Every tool here must fail on config it doesn't understand, never warn and carry on: ruff exits 2 on unknown keys, `--strict-config` makes pytest fail on them, and `error-on-warning` makes ty fail on unknown rules. uv only warns about a `pyproject.toml` it can't parse (and then ignores all project `[tool.uv]` settings) and has no strict mode, so the `config` gate below fails on any warning from `uv lock --check`.

`exclude-newer = "7 days"` puts the package-age quarantine in the project, so it also applies in CI and on machines without a user-level `~/.config/uv/uv.toml`. The lock records the span (`exclude-newer-span = "P7D"`), not a date, so a committed lock doesn't go stale as days pass.

**.python-version:**
```text
3.13
```

**Quality gates:**
```bash
# toolchain
uv run --locked python --version | grep -F 'Python 3.13.'
# config
out="$(uv lock --check 2>&1)" || { printf '%s\n' "$out"; exit 1; }; printf '%s\n' "$out"; ! grep -q '^warning:' <<<"$out"
# lint
uv run --locked ruff check .
# fmt
uv run --locked ruff format --check .
# typecheck
uv run --locked ty check
# test
uv run --locked python -m pytest
```

`--locked` fails when `uv.lock` is out of date instead of re-resolving. `ruff format .` is the fixer; the gate is `ruff format --check .`. `scripts/lane-conformance.py py` runs these gates on a fixture project at every engineering-core release.

---

### **Testing & Templating Guidance**

- Default unit/integration runner: **pytest**
- Property-based testing implementation: **Hypothesis**
- Behavior/Gherkin implementation: **pytest-bdd** when `disciplines/testing.md` says executable scenarios are justified
- OpenAPI contract testing implementation: **schemathesis** when API schema behavior needs executable coverage
- Text/config/html templating: **Jinja2** when the repo benefits from reusable template files or user-visible rendering surfaces
- Prefer plain Python functions / f-strings for small local formatting tasks
- Installed-wheel smoke tests that inject doubles into a subprocess interpreter load them through a `.pth` file in its site-packages, not `sitecustomize.py`: distribution Pythons (Debian, Ubuntu) ship their own `sitecustomize` earlier on `sys.path` and silently shadow it (see `disciplines/testing.md`, Isolation)

### **Packaging & Release (PyPI)**

Applies `disciplines/release-package.md`:

- Build with `uv build --clear` so a stale wheel from an earlier version never sits beside the new one.
- Publish from CI through PyPI trusted publishing (`pypa/gh-action-pypi-publish` in a job with only `id-token: write`, inside a protected environment restricted to release tags); no API tokens.
- A `README.md` used as `readme` in `pyproject.toml` is rendered on PyPI: use absolute links and image URLs.
- uv's `exclude-newer` quarantine hides a fresh upload; verify a new release with `uvx --exclude-newer-package <name>=<date> --from <name>==<version> <command>` rather than turning the quarantine off.

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
    *   Remove a dependency: `uv remove fastapi`; remove a development dependency: `uv remove --dev pytest`
*   **Synchronize Environment from Lockfile:** (Installs all dependencies from `uv.lock`)
    `uv sync`
*   **Update All Dependencies in Lockfile:**
    `uv sync --upgrade`
*   **Run the project:** (uv has no task runner; call tools directly or through the `Justfile`)
    *   Start the dev server (FastAPI on Granian): install with `uv add fastapi 'granian[reload]'`, run `uv run granian --interface asgi --reload example_service.asgi:app`. `--reload` needs the `granian[reload]` extra, and `--interface asgi` is required because Granian defaults to RSGI.
    *   Run tests: `uv run python -m pytest`
    *   Run the quality gates: the **Quality gates** block above
*   **Ad-Hoc Script Management:** (For utility scripts without polluting the main environment)
    *   Add dependencies to a script: `uv add --script scripts/my_script.py 'pandas' 'polars'`
    *   Run a script with its managed dependencies: `uv run --script scripts/my_script.py`
*   **Manage Standalone Tools:** (Install hook runners and other CLIs into a shared, isolated environment)
    *   Cross-lane default hook runner when a repo needs Git hooks: `uv tool run prek install` or `uvx prek install`
    *   `prek` is language-agnostic and can run `prek.toml` or compatible `.pre-commit-config.yaml` hook definitions; Python repos usually pair it with Ruff hook definitions or repo-local wrappers.
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
- ❌ `uv run python -m pytest coordination.tests.test_module` (pytest takes file paths, not dotted module paths, under any runner; use the file path or `--pyargs coordination.tests.test_module`)
- ❌ `python -m pytest` (wrong Python environment)

**Use**: `uv run python -m pytest <file_path>` (`uv run pytest` and `uv run -m pytest` are equivalent)

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
