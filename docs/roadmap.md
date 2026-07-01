# Roadmap

This roadmap tracks the planned direction for Kyvoris Profiler. The project is
currently focused on a small, dependable core before adding heavier integrations.

## Current Foundation

- Callable latency benchmarking.
- Latency summaries with average, minimum, maximum, p50, and p95 values.
- Plain-text, Markdown, JSON, and HTML report formatting.
- Warmup iterations before measurement.
- Optional process CPU time metrics.
- Optional peak Python-traced memory metrics.
- CLI entry point for no-argument `module:function` targets.
- Demo scripts for simulated inference and optional Hugging Face model inference.
- Example documentation for simulated and real-model benchmark runs.
- Minimal dependency footprint.
- Pytest and unittest coverage for the public benchmark behavior.

## Near-Term Milestones

### 1. Release Operations

- Weekly milestones.
- GitHub issue templates.
- Pull request descriptions.
- Release notes.
- Technical design documents for major changes.

### 2. Structured Output

- Optional CSV export for repeated benchmark runs.
- Stable schema documentation for downstream tooling.

### 3. Benchmark Controls

- Configurable run labels and metadata.
- Optional exception capture for failed iterations.
- Support for benchmarking callables with arguments.
- CLI support for callable arguments and richer target configuration.

### 4. Inference-Oriented Metrics

- Tokens per second.
- Input and output token counts.
- Time to first token for streaming workloads.
- Request success and failure counts.
- Native process, GPU, and framework-specific memory adapters.

### 5. Reporting

- Multi-run comparison reports.
- Markdown report files for CI artifacts.
- Console table formatting.

## Longer-Term Ideas

- Adapters for local inference engines.
- Adapters for remote HTTP inference endpoints.
- Memory and device utilization snapshots.
- CI-friendly regression thresholds.
- Lightweight dashboard output for benchmark history.

## Guiding Principles

- Keep the core package small and easy to understand.
- Prefer explicit, typed data structures over loosely shaped results.
- Make every metric clear about units and measurement scope.
- Avoid tying the core package to one model provider or serving stack.
