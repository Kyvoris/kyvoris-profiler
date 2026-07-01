# Technical Design

This document captures the long-term architecture direction for Kyvoris
Profiler. Create a dedicated design document before making major public API,
storage, CLI, adapter, or reporting changes.

## Current Architecture

Kyvoris Profiler is intentionally split into three small layers:

- `benchmark.py` runs repeatable callables and captures raw timings.
- `metrics.py` turns raw timings into typed summary objects.
- `report.py` converts summaries into human-readable or machine-readable output.

This separation keeps measurement, statistics, and presentation independent.

## 0.2.0 Design Decision

Warmup is part of `benchmark_callable()` because it controls execution behavior.
The measured result records `warmup_iterations`, but warmup calls are excluded
from latency statistics.

JSON and HTML are formatter concerns, so they belong in `report.py`. The JSON
report includes a `schema_version` so future tooling can detect changes.

## 0.3.0 Design Decision

`profile_callable()` adds opt-in resource metrics while `benchmark_callable()`
remains a compatibility-friendly latency entry point. CPU collection uses
process CPU time from the Python standard library. Memory collection uses
`tracemalloc`, which captures Python-traced allocations and intentionally avoids
claiming full process, native framework, or GPU memory coverage.

## 0.4.0 Design Decision

The CLI accepts targets in `module:function` format and limits execution to
no-argument callables. This keeps the first command-line release predictable and
aligned with the current Python API. Output formatting reuses the existing
report module, so CLI behavior stays consistent with library behavior.

## 0.5.0 Design Decision

Async profiling mirrors sync profiling instead of creating a separate result
shape. This keeps report formatting and downstream tooling stable. Endpoint
profiling is intentionally implemented as a small standard-library wrapper
around `profile_callable()`; richer clients should be represented as user-owned
callables so the core stays provider-neutral.

## 0.6.0 Design Decision

Comparison is modeled as a separate result type instead of overloading
`ProfileSummary`. This keeps single-run measurements stable while giving CI and
release workflows a structured representation for deltas, percentage changes,
and improvement/regression status.

## 0.7.0 Design Decision

Threshold evaluation is modeled separately from comparison generation. This lets
users create comparison reports without enforcing a policy, or apply a CI policy
with explicit metric filters and allowed regression percentages. CLI threshold
checks return exit code `1` only when `--fail-on-regression` is requested.
TOML is used for repeatable comparison configuration because it is readable,
matches the existing Python packaging ecosystem, and can be parsed with the
standard library.

## 0.8.0 Design Decision

CSV is added as a spreadsheet-oriented presentation format while JSON remains
the canonical machine-readable format. CSV output is intentionally simple and
uses the standard library so report generation remains dependency-free.

## 0.9.0 Design Decision

Benchmark history is stored as JSON Lines so each run can be appended without
rewriting the whole file. A history record stores timestamp, label, optional
source path, and normalized `ProfileSummary` metrics. The first history command
compares only the latest two records, keeping the workflow small while reusing
the existing comparison report and threshold logic.

## 0.10.0 Design Decision

History metadata is stored as a flat string dictionary so it remains easy to
inspect, diff, and extend without schema migrations. Environment metadata is
captured when appending from the CLI, while the history reader treats metadata
as optional so 0.9.0 JSONL files remain valid.

## 0.11.0 Design Decision

Targeted history comparison uses simple selectors instead of adding a query
language. Numeric selectors are 1-based indexes from `history list`; non-numeric
selectors match unique labels. Duplicate labels are rejected for label-based
selection so users do not accidentally compare the wrong records.

## 0.12.0 Design Decision

History filtering is intentionally exact-match only. Label filters match the
record label, metadata filters match flat `KEY=VALUE` pairs, and limit is applied
after filters so users get the latest matching records. `latest:LABEL` is added
as a small selector form instead of a broader query language.

## 0.13.0 Design Decision

History presets live under `[history_presets.<name>]` in the existing TOML config
file. This avoids adding another configuration file and keeps CI commands short.
CLI flags continue to override preset values so users can reuse a preset while
changing output format or destination for one run.

## Public API Principles

- Keep callable benchmarking simple and dependency-free.
- Add optional parameters only when defaults preserve existing behavior.
- Prefer typed dataclasses for benchmark results.
- Keep report formatters pure: summary in, string out.
- Add schema versions to machine-readable outputs.

## Future Design Documents

Create separate design documents for:

- CLI callable argument passing and richer target configuration.
- Async concurrency controls.
- Richer HTTP endpoint configuration.
- Per-metric threshold profiles and named policies.
- Native process, framework, and GPU memory adapters.
- Async benchmarking.
- Benchmark comparison schemas.
- Adapter APIs for local models and remote endpoints.
- Persistent benchmark history.

## Design Document Template

```markdown
# Design: <Feature Name>

## Problem

What user or maintainer problem are we solving?

## Goals

- Goal 1
- Goal 2

## Non-Goals

- Explicitly out of scope

## Proposed API

Code examples and expected output.

## Implementation Plan

Files, modules, and behavior changes.

## Testing Plan

Unit tests, integration tests, and manual checks.

## Risks

Compatibility, performance, and maintenance risks.

## Open Questions

Decisions still needed.
```
