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

## Public API Principles

- Keep callable benchmarking simple and dependency-free.
- Add optional parameters only when defaults preserve existing behavior.
- Prefer typed dataclasses for benchmark results.
- Keep report formatters pure: summary in, string out.
- Add schema versions to machine-readable outputs.

## Future Design Documents

Create separate design documents for:

- CLI command architecture.
- Memory, CPU, and GPU metrics.
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
