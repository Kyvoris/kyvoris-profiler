# Release Notes

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
