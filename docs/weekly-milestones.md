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

- Add memory profiling for peak process memory.
- Add optional CPU usage snapshots.
- Document measurement limits clearly.
- Add tests for metric collection fallbacks.

## Week 3: 0.4.0 CLI

- Add `kyvoris-profiler` command.
- Support iterations, warmup, report format, and output path flags.
- Add CLI smoke tests.
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

## Long-Term Cadence

- Keep weekly work small enough to review.
- Open issues before implementation starts.
- Link every pull request to its issue.
- Update release notes during the change, not after.
- Write a technical design document before adding shared architecture,
  persistence, integrations, or new public APIs.
