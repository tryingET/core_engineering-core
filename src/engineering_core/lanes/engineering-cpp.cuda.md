# C++ lane addendum — CUDA / GPU kernels

Read this addendum only after loading `engineering-cpp.md`, and only when the repo actually builds, profiles, benchmarks, or validates CUDA/GPU code.


## Applicable cross-language disciplines

Load disciplines when the concern applies:

- `validation` and `testing` for benchmark/correctness tiers and evidence.
- `observability` for GPU profiles, runtime measurements, and production claims.
- `dependency-governance` and `security-privacy` for CUDA/PyTorch/native dependency risk, drivers, and deployment constraints.
- `documentation` for hardware/toolkit/driver provenance.

## 1. When to load this addendum

Load this addendum for:

- `.cu` / `.cuh` sources or CUDA Toolkit build dependencies
- native CUDA/C++ kernels, CUDA runtime memory management, or device libraries
- PyTorch C++/CUDA extensions and custom operators
- PTX/SASS inspection, `ptxas` diagnostics, `cuobjdump`, `nvdisasm`, Nsight profiling, or Compute Sanitizer
- GPU benchmark evidence, GPU architecture targeting, or GPU-specific reproducibility claims

Do not load it for ordinary C++ projects that merely run on a machine with an NVIDIA GPU.

## 2. CUDA Toolkit / driver / architecture targeting

- Keep driver, CUDA Toolkit, compiler, and PyTorch CUDA build compatibility explicit in repo docs.
- Prefer repo-local checks such as `nvidia-smi`, `nvcc --version`, and a tiny compile/run smoke test over assumptions.
- Record target GPU architecture in code review. For the RTX PRO 6000 Blackwell Workstation Edition, NVIDIA's compute capability table maps it to compute capability 12.0, so native targets should include `sm_120` / `compute_120` when the installed CUDA Toolkit supports it.
- For CMake CUDA builds, set `CMAKE_CUDA_ARCHITECTURES` deliberately. Example for a local Blackwell-only research build: `-DCMAKE_CUDA_ARCHITECTURES=120`.
- For redistributable artifacts, include all supported production architectures and a PTX fallback where appropriate; document the resulting binary size and startup/JIT tradeoffs.

## 3. `nvcc`, `ptxas`, `cuobjdump`, and Nsight guidance

- Use `nvcc` through CMake or a repo-local build script; do not hand-copy undocumented internal `nvcc` subcommands into build scripts.
- Enable `ptxas` resource diagnostics for kernel work, for example with `-Xptxas=-v`, and record register/shared-memory changes in performance-sensitive reviews.
- Use `cuobjdump --dump-ptx` and `cuobjdump --dump-sass` only on trusted artifacts built by the repo or in a sandbox; binary-inspection tools have had CUDA Toolkit security advisories.
- Use Nsight Systems for end-to-end timeline evidence and Nsight Compute for kernel-level metrics. Keep profiler reports out of source unless the repo explicitly stores benchmark artifacts.
- Use Compute Sanitizer for memory/race/init validation when kernel correctness or memory safety is in question.

## 4. `sm_*` architecture handling

- Treat architecture lists as product decisions, not incidental flags.
- Use native `sm_*` cubins for GPUs that are deployed or benchmarked.
- Include `compute_*` PTX only when forward compatibility or JIT fallback is intentional.
- Avoid shipping a single local workstation architecture as a production default unless production hardware is the same.
- Keep architecture changes visible in diffs: CMake presets, toolchain files, or documented variables are better than hidden shell defaults.

## 5. PTX/SASS inspection

Use PTX/SASS inspection to answer specific questions:

- Did the build target the intended architecture?
- Did an optimization change register count, spills, instruction selection, or memory path?
- Is the kernel using expected tensor-core, vectorized, or memory instructions?

Common commands:

```bash
nvcc -arch=sm_120 -Xptxas=-v -c src/kernel.cu -o build/kernel.o
cuobjdump --dump-ptx build/my_binary > build/my_binary.ptx
cuobjdump --dump-sass build/my_binary > build/my_binary.sass
```

Do not treat PTX/SASS inspection alone as correctness or downstream performance evidence.

## 6. PyTorch C++/CUDA extension guidance

- Prefer PyTorch's custom operator / C++ extension path for tensor operations that must integrate with PyTorch dispatch, autograd, compilation, or packaging.
- Keep extension builds in a local Python environment; never require global `pip`, global CUDA installs from scripts, or privileged package mutation.
- Pin PyTorch and CUDA build compatibility in the same dependency group that builds/tests the extension.
- Use `torch.utils.cpp_extension` or `CUDAExtension` when that is the repo's chosen PyTorch path; remember PyTorch does not include the external compiler/CUDA Toolkit needed to compile extensions.
- For Python bindings that are not PyTorch tensor operators, compare pybind11 and nanobind before selecting one. Prefer pybind11 for maturity/ecosystem compatibility; consider nanobind when stable ABI, smaller bindings, or compile/runtime benefits are material and tested.
- Use scikit-build-core only when the project benefits from a pyproject/CMake wheel build. Do not add it for simple pure-Python wrappers.

## 7. Python venv isolation when Python-bound

- Use repo-local virtual environments or `uv` workflows; do not install into system Python.
- Keep build, test, and benchmark dependency groups pinned.
- Use lockfiles where supported.
- Keep PyTorch CUDA wheel/source choices explicit; do not mix incompatible binary channels casually.
- Ensure extension tests import the wheel/installed artifact that users will run, not only an in-tree module path.

## 8. Benchmarking methodology

A GPU benchmark report must include:

- warmup iterations before measurement
- repeat counts and summary statistics, not one-off timings
- explicit synchronization policy
- CUDA events for kernel timing when measuring device work
- clear inclusion/exclusion of host-device copies and allocations
- fixed input shapes, dtypes, strides/layout, seeds, and stream behavior
- noise controls: idle system notes, power/thermal notes, driver/toolkit versions, GPU model, and build type
- machine-readable metrics such as JSON/CSV for trend comparison

Use CPU timers only with explicit synchronization. For device-only timing, prefer CUDA events around the measured work. Avoid accidental synchronization inside logging, tensor printing, `.item()`, blocking copies, profiler setup, or allocator churn.

Standalone kernel evidence is not the same as downstream runtime integration evidence. A faster isolated kernel still needs integrated PyTorch/service/application measurements before product claims.

## 9. Correctness strategy

- Keep a reference implementation: CPU C++, Python/PyTorch, or a known-good library path.
- Validate outputs against the reference before benchmarking.
- Use dtype-specific tolerances. FP32, FP16, BF16, FP8/FP4, integer, and mixed-accumulation paths need different expectations.
- Test edge shapes: zero sizes, non-contiguous strides, misalignment, small sizes, large sizes, boundary block counts, odd dimensions, and maximum expected batch/sequence sizes.
- Test deterministic seeds and document nondeterministic operations.
- Check kernel launch errors immediately and synchronize in tests so asynchronous failures surface deterministically.

## 10. Memory discipline

- Preallocate benchmark buffers and keep the measured hot path allocation-free unless allocation is the thing being measured.
- Separate setup, transfer, kernel, and teardown timings.
- Avoid hidden host-device synchronization from pageable memory copies, tensor printing, debug checks, or framework API calls.
- Document ownership/lifetime of device buffers and streams at API boundaries.
- Prefer explicit workspace sizing over repeated dynamic allocations.
- Check memory errors with Compute Sanitizer on smoke/fast tiers where runtime is acceptable.

## 11. Dependency safety

- Avoid global installs, `sudo`, curl-pipe-shell installers, and unreviewed `.run`/binary installers.
- Pin local dependencies and record the official source for CUDA Toolkit, PyTorch, binding libraries, and build backends.
- Review transitive dependencies for Python-bound builds and wheel release tooling.
- Treat downloaded cubins, Nsight reports, benchmark artifacts, and sample repos as untrusted inputs.
- Do not run installer scripts, issue-provided repro scripts, or third-party benchmark harnesses without review.
- Make GPU-specific tooling optional unless the repo is fundamentally a CUDA/GPU repo.

## 12. Recommended validation tiers

- **Smoke:** `nvidia-smi`, `nvcc --version`, configure/build one CUDA target, run one tiny kernel/test, verify no global install is required.
- **Fast:** unit tests against reference outputs, selected edge shapes, sanitizer/error-checking where feasible, format/lint for touched files.
- **Full:** all tests, full shape/dtype matrix, Compute Sanitizer pass for critical kernels, packaging/import checks for Python-bound extensions.
- **Benchmark:** release/RelWithDebInfo build, warmups/repeats, CUDA events, machine-readable metrics, profiler evidence for changed kernels, and integrated downstream runtime evidence.

## 13. Project skeleton for CUDA kernel repos

```text
CMakeLists.txt
CMakePresets.json
include/<project>/
src/
  kernels/
    *.cu
    *.cuh
  host/
tests/
  reference/
  cuda/
bench/
  kernels/
  integration/
python/                       # optional PyTorch/Python bindings
  pyproject.toml
  tests/
profiles/                     # optional ignored/output-only unless policy says otherwise
docs/engineering.local.md
policy/engineering-lane.json
```

## 14. Experimental GPU research repos vs production service repos

Experimental GPU research repos may optimize for rapid kernel iteration, local Blackwell-native builds, and detailed benchmark notebooks, but must still keep dependency provenance, local isolation, correctness references, and machine-readable results.

Production service repos must optimize for reproducibility and operations: supported GPU fleet, driver/toolkit compatibility, deploy artifact strategy, observability, rollback, capacity planning, and integrated latency/throughput evidence. Production claims require downstream runtime measurements, not only standalone kernel benchmarks.
