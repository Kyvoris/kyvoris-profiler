# Weekly Milestones

Use this milestone plan to keep development focused and easy to communicate.
Each week should produce issues, one or more pull requests, tests, and a short
release note draft.

## Week 1: 0.2.0 Release Foundation

- Add warmup iterations.
- Add JSON and HTML reports.
- Add release notes and GitHub templates.
- Update examples and documentation.
- Verify pytest and unittest pass.

## Week 2: 0.3.0 Metrics Expansion

- Add memory profiling for peak Python-traced allocations.
- Add optional process CPU time metrics.
- Document measurement limits clearly.
- Add tests for metric collection fallbacks.

## Week 3: 0.4.0 CLI

- Add `kyvoris-profiler` command.
- Support iterations, warmup, report format, output path, CPU, and memory flags.
- Add CLI tests for stdout, file output, loading, and validation.
- Document local and CI usage.

## Week 4: 0.5.0 Async and Endpoint Benchmarks

- Add async callable benchmarking.
- Add example for HTTP or model-server inference.
- Track failures without hiding successful iterations.
- Add benchmark result schema notes.

## Week 5: 0.6.0 Comparisons

- Compare two benchmark results.
- Report percentage change for latency metrics.
- Add Markdown and HTML comparison output.
- Document branch-to-branch and model-to-model workflows.

## Week 6: 0.7.0 Regression Gates

- Add threshold evaluation for comparison results.
- Add CLI flags for allowed regression percentage and selected metrics.
- Return a non-zero exit code when `--fail-on-regression` is requested.
- Add passing and failing smoke tests.

## Week 7: 0.7.1 Configuration

- Add TOML configuration for repeatable comparison commands.
- Keep CLI flags as overrides for configured values.
- Add config smoke tests and documentation.
- Document why TOML is the preferred local configuration format.

## Week 8: 0.8.0 Report Formats

- Add CSV reports for summary and comparison output.
- Document JSON and CSV report schemas.
- Add CSV CLI and formatter tests.
- Update release notes and PR descriptions.

## Week 9: 0.9.0 Benchmark History

- Add JSONL history records for saved benchmark summaries.
- Add CLI commands for appending reports and comparing latest records.
- Reuse comparison report formats and threshold checks for history.
- Add test runner coverage and schema documentation.

## Long-Term Cadence

- Keep weekly work small enough to review.
- Open issues before implementation starts.
- Link every pull request to its issue.
- Update release notes during the change, not after.
- Write a technical design document before adding shared architecture,
  persistence, integrations, or new public APIs.
