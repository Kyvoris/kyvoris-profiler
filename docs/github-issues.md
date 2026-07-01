# GitHub Issues

Use issues to describe the problem, acceptance criteria, and validation before
implementation starts.

## Labels

- `type:feature`
- `type:bug`
- `type:docs`
- `type:test`
- `area:benchmark`
- `area:reports`
- `area:cli`
- `area:metrics`
- `release:0.2.0`
- `release:0.3.0`

## 0.3.0 Issues

### Add Resource Profiling API

**Problem:** Latency alone does not show whether an inference path is CPU-heavy
or creates avoidable Python allocations.

**Acceptance criteria:**

- Public `profile_callable()` API exists.
- Existing `benchmark_callable()` behavior remains compatible.
- Resource collection is opt-in.
- Tests cover latency-only and resource-enabled behavior.

### Add Process CPU Time Metrics

**Problem:** Benchmarks need a lightweight CPU signal without adding platform
dependencies.

**Acceptance criteria:**

- `collect_cpu=True` records process CPU time per measured iteration.
- Summary includes average, minimum, and maximum CPU time.
- Reports include CPU metrics only when collected.

### Add Peak Python Memory Metrics

**Problem:** Benchmarks need a first memory signal for Python-heavy inference
wrappers, preprocessing, and postprocessing.

**Acceptance criteria:**

- `collect_memory=True` records peak Python-traced allocations.
- Documentation clearly states that this is not GPU or full native memory.
- Reports include memory metrics only when collected.

## 0.2.0 Issues

### Add Warmup Iterations

**Problem:** Benchmarks need untimed warmup calls so model setup, tokenization,
and first-run caches do not distort repeated inference latency.

**Acceptance criteria:**

- `benchmark_callable()` accepts `warmup`.
- Warmup calls run before measured iterations.
- Negative warmup values raise `ValueError`.
- Reports include warmup count.
- Tests cover default and configured warmup behavior.

### Add JSON Report Formatter

**Problem:** Benchmark results need a structured format for automation,
storage, and future comparisons.

**Acceptance criteria:**

- Public `format_json_report()` API exists.
- JSON contains title, schema version, and metrics.
- Output is deterministic enough for tests.

### Add HTML Report Formatter

**Problem:** Benchmark results should be shareable as a standalone artifact.

**Acceptance criteria:**

- Public `format_html_report()` API exists.
- HTML contains benchmark title and all metrics.
- User-provided title is escaped.

### Add Release Workflow Documentation

**Problem:** The project needs a repeatable professional workflow for planning,
pull requests, and releases.

**Acceptance criteria:**

- Weekly milestone document exists.
- Release notes document exists.
- PR description guidance exists.
- Technical design document structure exists.
