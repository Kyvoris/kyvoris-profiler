# Kyvoris Profiler

Lightweight, dependency-free benchmarking utilities for AI inference workloads.

Kyvoris Profiler helps you answer a practical question: how long does this
inference path actually take when it runs repeatedly? Wrap a model call, HTTP
request, retrieval step, or any other no-argument Python callable, then get a
typed latency summary and readable reports.

> Project status: early alpha. The current package focuses on latency
> measurement, metric summaries, and report formatting. See
> [docs/roadmap.md](docs/roadmap.md) for planned milestones.

## Why Kyvoris Profiler?

AI systems often feel fast in a single manual test, then behave differently when
called repeatedly. Kyvoris Profiler gives you a small, clear benchmark loop for
measuring that repeated behavior.

- Measure repeated inference latency in milliseconds.
- Capture average, minimum, maximum, p50, and p95 latency.
- Return typed summaries instead of loosely shaped dictionaries.
- Generate plain-text or Markdown reports.
- Keep the core package free of runtime dependencies.
- Use the same API for simulated workloads, local models, remote endpoints, and
  custom inference wrappers.

## Installation

### Local Development

```powershell
git clone <your-repo-url>
cd kyvoris-profiler
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

The core package has no runtime dependencies. The `dev` extra installs pytest
for running the test suite.

### Use Without Installing

From the repository root, you can also run examples by setting `PYTHONPATH`:

```powershell
$env:PYTHONPATH="src"
python examples\run_demo.py
```

## Quick Start

```python
import time

from kyvoris_profiler import benchmark_callable, format_text_report


def run_inference() -> str:
    time.sleep(0.005)
    return "ok"


summary = benchmark_callable(run_inference, iterations=20)
print(format_text_report(summary, title="Inference Benchmark"))
```

Example output:

```text
Inference Benchmark
-------------------
Iterations: 20
Average:    5.100 ms
Minimum:    5.000 ms
Maximum:    5.400 ms
P50:        5.080 ms
P95:        5.320 ms
```

## Real Model Example

Kyvoris Profiler includes an optional Hugging Face example that benchmarks real
sentiment-analysis inference with:

```text
distilbert-base-uncased-finetuned-sst-2-english
```

Install the optional model dependencies:

```powershell
python -m pip install "transformers[torch]"
```

Run the example:

```powershell
$env:PYTHONPATH="src"
python examples\run_model_demo.py
```

Expected output shape:

```text
Real Model Inference Benchmark
------------------------------
Iterations: 10
Average:    32.415 ms
Minimum:    29.880 ms
Maximum:    41.203 ms
P50:        31.702 ms
P95:        39.484 ms

Model: distilbert-base-uncased-finetuned-sst-2-english
Input: Kyvoris Profiler makes inference benchmarking simple.
Sample output: [{'label': 'POSITIVE', 'score': 0.999...}]
```

The exact latency values depend on hardware, installed backend, Python version,
power mode, and whether model files are already cached. The example loads the
model before benchmarking and performs one warmup call, so the measured results
represent repeated inference latency rather than setup time.

More details are available in [docs/examples.md](docs/examples.md).

## API Overview

### `benchmark_callable(callable_obj, iterations=10)`

Runs a no-argument callable multiple times and returns a `LatencySummary`.

```python
summary = benchmark_callable(run_inference, iterations=10)
```

The callable can wrap:

- a local model inference call
- a remote HTTP inference request
- a retrieval or reranking step
- a preprocessing or postprocessing function
- any other repeatable unit of work

### `LatencySummary`

Immutable dataclass containing:

| Field | Meaning |
| --- | --- |
| `average_ms` | Mean latency across all measured runs |
| `min_ms` | Fastest measured run |
| `max_ms` | Slowest measured run |
| `p50_ms` | Median latency |
| `p95_ms` | Slower-end latency often useful for user-facing performance |
| `iterations` | Number of measured runs |

Use `summary.as_dict()` when you need a plain dictionary for serialization or
custom reporting.

### Reporting

```python
from kyvoris_profiler import format_markdown_report, format_text_report

print(format_text_report(summary))
print(format_markdown_report(summary))
```

`format_text_report()` is useful for terminal output. `format_markdown_report()`
is useful for README snippets, CI comments, and benchmark artifacts.

## Project Layout

```text
kyvoris-profiler/
|-- docs/
|   |-- examples.md
|   `-- roadmap.md
|-- examples/
|   |-- run_demo.py
|   `-- run_model_demo.py
|-- src/
|   `-- kyvoris_profiler/
|       |-- benchmark.py
|       |-- metrics.py
|       |-- report.py
|       `-- __init__.py
|-- tests/
|   |-- test_benchmark.py
|   `-- test_benchmark_pytest.py
|-- pyproject.toml
`-- README.md
```

## Running Tests

Run the full pytest suite:

```powershell
python -m pytest
```

Run the standard-library unittest checks:

```powershell
python -m unittest discover -s tests
```

## Design Principles

- Keep the benchmark core small, explicit, and easy to audit.
- Make units obvious: latency values are reported in milliseconds.
- Separate measurement, metric calculation, and report formatting.
- Avoid provider lock-in; the callable wrapper decides what is being measured.
- Keep optional model dependencies out of the core package.

## Roadmap

Planned areas include:

- warmup iterations as a first-class benchmark option
- JSON and CSV exports
- benchmark labels and metadata
- exception capture for failed iterations
- support for callables with arguments
- inference-specific metrics such as tokens per second and time to first token
- comparison reports for multiple benchmark runs

See [docs/roadmap.md](docs/roadmap.md) for the full roadmap.

## Contributing

Contributions are welcome while the project foundation is still small.

Good first areas:

- improve examples
- add export formats
- expand tests around edge cases
- add documentation for benchmark interpretation
- prototype inference-specific metrics

Before opening a change, run:

```powershell
python -m pytest
python -m unittest discover -s tests
```

## License

This project is licensed under the terms of the [MIT License](LICENSE).
