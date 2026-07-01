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
- `release:0.4.0`
- `release:0.5.0`
- `release:0.6.0`
- `release:0.7.0`
- `release:0.7.1`
- `release:0.8.0`
- `release:0.9.0`
- `release:0.10.0`

## 0.10.0 Issues

### Add History Metadata

**Problem:** Saved benchmark records need context such as model name, Python
version, platform, and git commit to make later comparisons meaningful.

**Acceptance criteria:**

- History records support a metadata object.
- Append commands add environment metadata by default.
- Users can add custom `KEY=VALUE` metadata.
- Older history records without metadata still load.

### Add History List Command

**Problem:** Users need to inspect saved history records without opening JSONL
files manually.

**Acceptance criteria:**

- `kyvoris-profiler history list` prints saved records.
- Output includes index, timestamp, label, average latency, p95 latency, and key
  metadata.
- Test runner includes a history list smoke check.

## 0.9.0 Issues

### Add Benchmark History Storage

**Problem:** Users need a simple way to keep repeated benchmark summaries
without building custom storage.

**Acceptance criteria:**

- Public history helpers can append and read JSONL records.
- History records include timestamp, label, optional source path, and summary
  metrics.
- Tests cover appending from a summary JSON report.

### Add CLI History Comparison

**Problem:** Users need to compare the latest saved benchmark runs from the CLI.

**Acceptance criteria:**

- `kyvoris-profiler history append` appends a summary JSON report to JSONL.
- `kyvoris-profiler history compare-latest` compares the latest two records.
- History comparison supports report formats and threshold flags.
- Test runner includes history smoke checks.

## 0.8.0 Issues

### Add CSV Report Format

**Problem:** Users need benchmark and comparison output that opens easily in
spreadsheet tools.

**Acceptance criteria:**

- Summary reports support `--format csv`.
- Comparison reports support `--format csv`.
- CSV formatters are exposed through the public API.
- Tests cover formatter and CLI output behavior.

### Document Report Schemas

**Problem:** Automation and future dashboards need stable documentation for
machine-readable report formats.

**Acceptance criteria:**

- `docs/report-schema.md` documents summary JSON and CSV.
- `docs/report-schema.md` documents comparison JSON and CSV.
- README links to the schema documentation.

## 0.7.1 Issues

### Add TOML Comparison Config

**Problem:** Teams should not need to repeat long comparison and threshold flags
in every CI command.

**Acceptance criteria:**

- `kyvoris-profiler compare --config kyvoris-profiler.toml` works.
- CLI arguments override config values.
- Tests cover config loading and override behavior.
- Test runner includes a config-based comparison smoke check.

## 0.7.0 Issues

### Add Threshold Evaluation API

**Problem:** CI workflows need an explicit pass/fail signal when benchmark
metrics regress beyond an allowed tolerance.

**Acceptance criteria:**

- Public `evaluate_thresholds()` API exists.
- Threshold results include pass/fail status and violations.
- Tests cover passing, failing, and invalid threshold cases.

### Add CLI Regression Gate

**Problem:** Users need to fail CI from saved comparison reports without writing
custom Python scripts.

**Acceptance criteria:**

- `kyvoris-profiler compare` supports `--max-regression-percent`.
- `kyvoris-profiler compare` supports `--threshold-metric`.
- `--fail-on-regression` exits with code 1 when violations are found.
- Test runner covers passing and failing threshold smoke checks.


## 0.6.0 Issues

### Add Profile Comparison API

**Problem:** Users need to compare benchmark results across branches, models, or
optimization attempts.

**Acceptance criteria:**

- Public `compare_profiles()` API exists.
- Comparison includes baseline, candidate, delta, percent change, and result.
- Tests cover improved and regressed metrics.

### Add Comparison Reports

**Problem:** Comparison results should be shareable in CI comments and release
artifacts.

**Acceptance criteria:**

- Text, Markdown, JSON, and HTML comparison formatters exist.
- Tests cover key formatter output.

### Add CLI Compare Command

**Problem:** Users need to compare saved JSON reports without writing Python.

**Acceptance criteria:**

- `kyvoris-profiler compare baseline.json candidate.json` works.
- CLI supports output format and output path.
- Test runner includes a CLI comparison smoke check.

## 0.5.0 Issues

### Add Async Callable Profiling

**Problem:** Many inference clients and endpoint SDKs are async-first.

**Acceptance criteria:**

- Public `profile_async_callable()` API exists.
- Public `benchmark_async_callable()` convenience API exists.
- Reports use the existing `ProfileSummary` shape.
- Tests cover async latency and resource profiling.

### Add Endpoint Profiling Helper

**Problem:** Users need a quick way to profile a simple HTTP endpoint without
writing request boilerplate.

**Acceptance criteria:**

- Public `profile_http_endpoint()` API exists.
- Implementation uses the standard library.
- Tests use a local HTTP server rather than a public network dependency.

### Add Failure Counts

**Problem:** Endpoint-like workloads can have intermittent failures, and users
need visibility into those failures without losing successful measurements.

**Acceptance criteria:**

- `continue_on_error=True` captures failed measured iterations.
- `ProfileSummary` includes `failed_iterations`.
- Reports include failure count.

## 0.4.0 Issues

### Add CLI Entry Point

**Problem:** Users should be able to run a benchmark without writing a custom
Python driver script.

**Acceptance criteria:**

- `kyvoris-profiler` console script exists.
- `python -m kyvoris_profiler` works.
- CLI accepts targets in `module:function` format.
- Tests cover target loading and command execution.

### Add CLI Report Output Options

**Problem:** CLI users need reports in the same formats available from the
Python API.

**Acceptance criteria:**

- CLI supports text, Markdown, JSON, and HTML output.
- CLI can write reports to a file path.
- Tests cover JSON output files.

### Add CLI Metric Flags

**Problem:** Resource profiling should be available from the command line.

**Acceptance criteria:**

- CLI supports `--collect-cpu`.
- CLI supports `--collect-memory`.
- CLI reports include resource rows only when collected.

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
