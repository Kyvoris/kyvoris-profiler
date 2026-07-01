# Release Notes

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
