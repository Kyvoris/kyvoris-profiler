# Roadmap

This roadmap tracks the planned direction for Kyvoris Profiler. The project is
currently focused on a small, dependable core before adding heavier integrations.

## Current Foundation

- Callable latency benchmarking.
- Latency summaries with average, minimum, maximum, p50, and p95 values.
- Plain-text and Markdown report formatting.
- Demo scripts for simulated inference and optional Hugging Face model inference.
- Example documentation for simulated and real-model benchmark runs.
- Minimal dependency footprint.
- Pytest and unittest coverage for the public benchmark behavior.

## Near-Term Milestones

### 1. Structured Output

- JSON export for benchmark summaries.
- Optional CSV export for repeated benchmark runs.
- Stable schema documentation for downstream tooling.

### 2. Benchmark Controls

- Warmup iterations.
- Configurable run labels and metadata.
- Optional exception capture for failed iterations.
- Support for benchmarking callables with arguments.

### 3. Inference-Oriented Metrics

- Tokens per second.
- Input and output token counts.
- Time to first token for streaming workloads.
- Request success and failure counts.

### 4. Reporting

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
