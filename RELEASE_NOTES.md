# Release Notes

## 1.0.1

`1.0.1` fixes Python 3.10 compatibility in CI.

### Fixed

- Replaced `datetime.UTC` usage with Python 3.10-compatible `timezone.utc`.
- Added a `tomllib` fallback through `tomli` for Python 3.10.

### Changed

- Project metadata version is now `1.0.1`.

### Validation

- `python -m pytest`
- `python -m unittest discover -s tests`
- `powershell -ExecutionPolicy Bypass -File .\scripts\test-all.ps1`
- `powershell -ExecutionPolicy Bypass -File .\scripts\release-check.ps1`

## 1.0.0

`1.0.0` is the first stable Kyvoris Profiler release.

### Added

- GitHub Actions CI for Python 3.10, 3.11, 3.12, and 3.13.
- CI coverage for pytest, unittest, and package release checks.

### Changed

- Project metadata version is now `1.0.0`.
- Development status classifier is now production/stable.

### Validation

- `python -m pytest`
- `python -m unittest discover -s tests`
- `powershell -ExecutionPolicy Bypass -File .\scripts\test-all.ps1`
- `powershell -ExecutionPolicy Bypass -File .\scripts\release-check.ps1`

## 0.14.0

`0.14.0` adds packaging and release-readiness checks before the 1.0.0 push.

### Added

- `scripts/release-check.ps1` for building, validating, and clean-installing
  package artifacts.
- `docs/release-checklist.md`.
- Project URLs in package metadata.
- Build and twine tools in the `dev` optional dependency group.

### Changed

- Project metadata version is now `0.14.0`.
- Development status classifier is now beta.

### Validation

- `python -m pytest`
- `python -m unittest discover -s tests`
- `powershell -ExecutionPolicy Bypass -File .\scripts\test-all.ps1`
- `powershell -ExecutionPolicy Bypass -File .\scripts\release-check.ps1`

## 0.13.0

`0.13.0` adds saved history comparison presets.

### Added

- `[history_presets]` support in `kyvoris-profiler.toml`.
- `kyvoris-profiler history compare --preset NAME`.
- CLI overrides for preset values such as format and output path.
- Test runner coverage for preset-based history comparison.

### Changed

- Project metadata version is now `0.13.0`.

### Validation

- `python -m pytest`
- `python -m unittest discover -s tests`
- `powershell -ExecutionPolicy Bypass -File .\scripts\test-all.ps1`

## 0.12.0

`0.12.0` adds filtering for benchmark history and latest-label selectors.

### Added

- Public `filter_history_records()` helper.
- `kyvoris-profiler history list --label`.
- `kyvoris-profiler history list --metadata KEY=VALUE`.
- `kyvoris-profiler history list --limit N`.
- `latest:LABEL` selectors for `kyvoris-profiler history compare`.
- Test runner coverage for filtered history lists and latest-label comparison.

### Changed

- Project metadata version is now `0.12.0`.

### Validation

- `python -m pytest`
- `python -m unittest discover -s tests`
- `powershell -ExecutionPolicy Bypass -File .\scripts\test-all.ps1`

## 0.11.0

`0.11.0` adds targeted benchmark history comparisons.

### Added

- Public history selection helpers for selecting records by index or label.
- `kyvoris-profiler history compare` for comparing any two saved records.
- CLI support for `--baseline` and `--candidate` history selectors.
- Test runner coverage for selected history comparison output.

### Changed

- Project metadata version is now `0.11.0`.

### Validation

- `python -m pytest`
- `python -m unittest discover -s tests`
- `powershell -ExecutionPolicy Bypass -File .\scripts\test-all.ps1`

## 0.10.0

`0.10.0` improves benchmark history with metadata and list output.

### Added

- History records can store metadata alongside benchmark summaries.
- `collect_environment_metadata()` captures Python, platform, and git commit
  details when available.
- `kyvoris-profiler history append --metadata KEY=VALUE`.
- `kyvoris-profiler history append --no-environment-metadata`.
- `kyvoris-profiler history list` for viewing saved records.
- Test runner coverage for history list output.

### Changed

- Project metadata version is now `0.10.0`.

### Validation

- `python -m pytest`
- `python -m unittest discover -s tests`
- `powershell -ExecutionPolicy Bypass -File .\scripts\test-all.ps1`

## 0.9.0

`0.9.0` adds benchmark history storage and latest-run comparison workflows.

### Added

- Public benchmark history helpers for JSONL storage.
- `kyvoris-profiler history append` for saving summary JSON reports.
- `kyvoris-profiler history compare-latest` for comparing the latest two saved
  records.
- Threshold checks for history comparisons.
- History smoke checks in `scripts/test-all.ps1`.
- Documentation for history CLI usage and JSONL schema.
- Hugging Face model example now benchmarks three curated sentiment models by
  default.

### Changed

- Project metadata version is now `0.9.0`.

### Validation

- `python -m pytest`
- `python -m unittest discover -s tests`
- `powershell -ExecutionPolicy Bypass -File .\scripts\test-all.ps1`

## 0.8.0

`0.8.0` adds CSV reports and schema documentation for report consumers.

### Added

- CSV report formatter for benchmark summaries.
- CSV report formatter for benchmark comparisons.
- CLI `--format csv` support for benchmark and comparison reports.
- CSV smoke checks in `scripts/test-all.ps1`.
- Report schema documentation in `docs/report-schema.md`.
- Tests for CSV formatter and CLI output behavior.

### Changed

- Project metadata version is now `0.8.0`.

### Validation

- `python -m pytest`
- `python -m unittest discover -s tests`
- `powershell -ExecutionPolicy Bypass -File .\scripts\test-all.ps1`

## 0.7.1

`0.7.1` adds repeatable TOML configuration for comparison and threshold
workflows.

### Added

- `kyvoris-profiler.toml` example config file.
- `kyvoris-profiler compare --config kyvoris-profiler.toml`.
- CLI override support when a config file is provided.
- Test runner coverage for config-based comparison.
- Documentation for TOML config usage.

### Changed

- Project metadata version is now `0.7.1`.

### Validation

- `python -m pytest`
- `python -m unittest discover -s tests`
- `powershell -ExecutionPolicy Bypass -File .\scripts\test-all.ps1`

## 0.7.0

`0.7.0` adds threshold evaluation for CI-friendly performance regression gates.

### Added

- `evaluate_thresholds()` for checking comparison regressions against an allowed
  percentage.
- `ThresholdViolation` and `ThresholdEvaluation` dataclasses.
- CLI comparison flags:
  - `--max-regression-percent`
  - `--threshold-metric`
  - `--fail-on-regression`
- TOML comparison config support with `--config`.
- Example `kyvoris-profiler.toml` config file.
- Test runner smoke checks for passing and failing threshold behavior.
- Tests for threshold API validation and CLI exit codes.

### Changed

- Project metadata version is now `0.7.0`.

### Validation

- `python -m pytest`
- `python -m unittest discover -s tests`
- `powershell -ExecutionPolicy Bypass -File .\scripts\test-all.ps1`

## 0.6.0

`0.6.0` adds benchmark comparison utilities for branch-to-branch,
model-to-model, and before/after performance checks.

### Added

- `compare_profiles()` for comparing two `ProfileSummary` objects.
- `MetricComparison` and `ProfileComparison` dataclasses.
- Text, Markdown, JSON, and HTML comparison report formatters.
- `kyvoris-profiler compare` for comparing two JSON reports from the CLI.
- Comparison demo script.
- Detailed metrics explanation guide in `docs/metrics.md`.
- Test runner coverage for comparison demo and CLI comparison output.
- Tests for comparison metrics and report formatting.

### Changed

- Project metadata version is now `0.6.0`.

### Validation

- `python -m pytest`
- `python -m unittest discover -s tests`
- `powershell -ExecutionPolicy Bypass -File .\scripts\test-all.ps1`

## 0.5.0

`0.5.0` adds async and endpoint profiling for modern inference workflows.

### Added

- `profile_async_callable()` for no-argument async callables.
- `benchmark_async_callable()` as the async latency-only convenience API.
- `profile_http_endpoint()` for simple dependency-free HTTP endpoint profiling.
- `failed_iterations` on `ProfileSummary`.
- `continue_on_error=True` support for sync and async profiling.
- Async demo and HTTP endpoint demo scripts.
- CLI support for async `module:function` targets.
- Tests for async profiling, failure capture, async CLI targets, and local HTTP
  endpoint profiling.

### Changed

- Text, Markdown, JSON, and HTML reports now include failure count.
- `scripts/test-all.ps1` now runs async example and async CLI smoke checks.
- Project metadata version is now `0.5.0`.

### Validation

- `python -m pytest`
- `python -m unittest discover -s tests`
- `powershell -ExecutionPolicy Bypass -File .\scripts\test-all.ps1`

## 0.4.1

`0.4.1` patches the CLI release with smoother local testing and clearer test
commands.

### Added

- `scripts/test-all.ps1` for running pytest, unittest, examples, inline
  profiling, CLI smoke checks, and optional Hugging Face model checks.
- README commands for direct CLI testing and the full test runner.
- Regression test for loading CLI targets from the current working directory.

### Fixed

- CLI target loading now adds the current working directory to `sys.path`, so
  repo-local targets such as `examples.run_demo:simulated_inference` work from
  the project root.

### Changed

- Ignored generated `*.egg-info/` packaging metadata.
- Project metadata version is now `0.4.1`.

### Validation

- `powershell -ExecutionPolicy Bypass -File .\scripts\test-all.ps1`

## 0.4.0

`0.4.0` adds a command-line interface for running Kyvoris Profiler without
writing a custom benchmark script.

### Added

- `kyvoris-profiler` console script.
- `python -m kyvoris_profiler` module entry point.
- CLI support for `module:function` targets.
- CLI flags for iterations, warmup, report format, output path, title, CPU
  metrics, and memory metrics.
- CLI tests for loading targets, stdout reports, JSON file output, and error
  handling.
- CLI usage documentation in `docs/cli.md`.

### Changed

- Project metadata version is now `0.4.0`.
- README and planning docs now include CLI workflows.

### Validation

- `python -m pytest`
- `python -m unittest discover -s tests`

## 0.3.0

`0.3.0` expands Kyvoris Profiler from latency-only benchmarking into opt-in
resource profiling.

### Added

- `profile_callable()` for latency plus optional resource metrics.
- Optional process CPU time collection with `collect_cpu=True`.
- Optional peak Python-traced memory collection with `collect_memory=True`.
- `ProfileSummary` as the primary summary type.
- Resource metric rows in text, Markdown, JSON, and HTML reports.
- Tests for CPU, memory, validation, and report output behavior.

### Changed

- `benchmark_callable()` now delegates to `profile_callable()` while preserving
  existing latency-only behavior.
- `LatencySummary` remains available as a compatibility alias for
  `ProfileSummary`.
- Project metadata version is now `0.3.0`.

### Validation

- `python -m pytest`
- `python -m unittest discover -s tests`

## 0.2.0

`0.2.0` turns Kyvoris Profiler from a basic latency helper into a more
release-ready profiling foundation.

### Added

- Warmup iterations through `benchmark_callable(..., warmup=N)`.
- `warmup_iterations` on `LatencySummary`.
- JSON reports with `format_json_report()`.
- Standalone HTML reports with `format_html_report()`.
- Weekly milestone planning in `docs/weekly-milestones.md`.
- GitHub issue guidance in `docs/github-issues.md`.
- Pull request description guidance in `docs/pull-request-descriptions.md`.
- Technical design documentation in `docs/design/technical-design.md`.
- GitHub pull request and issue templates under `.github/`.

### Changed

- Text and Markdown reports now include warmup count.
- Hugging Face and simulated examples use configured warmup iterations.
- Project metadata version is now `0.2.0`.

### Validation

- `python -m pytest`
- `python -m unittest discover -s tests`

## 0.1.0

Initial project foundation with callable benchmarking, latency summaries,
plain-text and Markdown reports, examples, and tests.
