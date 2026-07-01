# Kyvoris Profiler

Lightweight, dependency-free benchmarking utilities for AI inference workloads.

Kyvoris Profiler helps you answer a practical question: how long does this
inference path actually take when it runs repeatedly? Wrap a model call, HTTP
request, retrieval step, or any other no-argument Python callable, then get a
typed latency summary and readable reports.

> Project status: early alpha. Version `0.12.0` focuses on latency measurement,
> warmup-aware benchmarks, optional CPU and memory metrics, structured reports,
> async workloads, HTTP endpoints, comparison reports, benchmark history, and a
> command-line interface. See
> [docs/roadmap.md](docs/roadmap.md) for planned milestones.

## Why Kyvoris Profiler?

AI systems often feel fast in a single manual test, then behave differently when
called repeatedly. Kyvoris Profiler gives you a small, clear benchmark loop for
measuring that repeated behavior.

- Measure repeated inference latency in milliseconds.
- Capture average, minimum, maximum, p50, and p95 latency.
- Run warmup iterations before measured iterations.
- Optionally collect process CPU time and peak Python memory allocations.
- Profile async callables and simple HTTP endpoints.
- Count failed measured iterations when exception capture is enabled.
- Compare benchmark summaries across versions, branches, or implementations.
- Save benchmark history as JSONL and compare the latest two saved runs.
- Enforce comparison thresholds for CI regression checks.
- Return typed summaries instead of loosely shaped dictionaries.
- Generate plain-text, Markdown, JSON, HTML, or CSV reports.
- Run benchmarks from the command line with `kyvoris-profiler`.
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

from kyvoris_profiler import format_text_report, profile_callable


def run_inference() -> str:
    time.sleep(0.005)
    return "ok"


summary = profile_callable(
    run_inference,
    iterations=20,
    warmup=2,
    collect_cpu=True,
    collect_memory=True,
)
print(format_text_report(summary, title="Inference Benchmark"))
```

Example output:

```text
Inference Benchmark
-------------------
Iterations: 20
Warmup: 2
Failures: 0
Average: 5.100 ms
Minimum: 5.000 ms
Maximum: 5.400 ms
P50: 5.080 ms
P95: 5.320 ms
Average CPU: 0.120 ms
Minimum CPU: 0.090 ms
Maximum CPU: 0.180 ms
Peak Python Memory: 4.250 KB
```

## Real Model Example

Kyvoris Profiler includes an optional Hugging Face example that benchmarks real
sentiment-analysis inference across three curated Hugging Face models:

```text
distilbert/distilbert-base-uncased-finetuned-sst-2-english
cardiffnlp/twitter-roberta-base-sentiment-latest
lxyuan/distilbert-base-multilingual-cased-sentiments-student
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

Run a smaller smoke test:

```powershell
$env:PYTHONPATH="src"
python examples\run_model_demo.py --iterations 3 --warmup 1
```

Override the model list if you want to benchmark specific Hugging Face models:

```powershell
$env:PYTHONPATH="src"
python examples\run_model_demo.py --model cardiffnlp/twitter-roberta-base-sentiment-latest --iterations 3
```

Expected output shape:

```text
Real Model Inference Benchmark
------------------------------
Iterations: 10
Warmup: 1
Failures: 0
Average: 32.415 ms
Minimum: 29.880 ms
Maximum: 41.203 ms
P50: 31.702 ms
P95: 39.484 ms
Average CPU: 26.115 ms
Minimum CPU: 22.904 ms
Maximum CPU: 35.001 ms
Peak Python Memory: 85.250 KB

Model: distilbert/distilbert-base-uncased-finetuned-sst-2-english
Input: Kyvoris Profiler makes inference benchmarking simple.
Sample output: [{'label': 'POSITIVE', 'score': 0.999...}]
```

The exact latency values depend on hardware, installed backend, Python version,
power mode, and whether model files are already cached. The example loads the
model before benchmarking and uses one configured warmup iteration, so the measured results
represent repeated inference latency rather than setup time.

More details are available in [docs/examples.md](docs/examples.md).

## CLI Example

After installing locally with `python -m pip install -e ".[dev]"`, benchmark a
no-argument callable by passing `module:function`:

```powershell
kyvoris-profiler examples.run_demo:simulated_inference --iterations 5 --warmup 1 --collect-cpu --collect-memory
```

Write JSON or HTML artifacts with `--format` and `--output`:

```powershell
kyvoris-profiler examples.run_demo:simulated_inference --iterations 5 --format json --output reports/demo.json
```

Without installation, run the same CLI through Python:

```powershell
$env:PYTHONPATH="src"
python -m kyvoris_profiler examples.run_demo:simulated_inference --iterations 5
```

More CLI details are available in [docs/cli.md](docs/cli.md).

## Async and Endpoint Examples

Profile an async callable:

```python
import asyncio

from kyvoris_profiler import format_text_report, profile_async_callable


async def run_async_inference() -> str:
    await asyncio.sleep(0.005)
    return "ok"


summary = asyncio.run(profile_async_callable(run_async_inference, iterations=10, warmup=1))
print(format_text_report(summary, title="Async Benchmark"))
```

Profile a simple HTTP endpoint:

```python
from kyvoris_profiler import format_text_report, profile_http_endpoint

summary = profile_http_endpoint("https://example.com", iterations=3, warmup=1)
print(format_text_report(summary, title="Endpoint Benchmark"))
```

## Comparison Example

Compare two benchmark summaries:

```python
from kyvoris_profiler import (
    compare_profiles,
    format_comparison_text_report,
    profile_callable,
)

baseline = profile_callable(run_inference_before, iterations=10, warmup=1)
candidate = profile_callable(run_inference_after, iterations=10, warmup=1)
comparison = compare_profiles(baseline, candidate, "before", "after")
print(format_comparison_text_report(comparison))
```

Compare two JSON reports from the CLI:

```powershell
python -m kyvoris_profiler compare reports\baseline.json reports\candidate.json --format markdown --output reports\comparison.md
```

Fail CI when selected metrics regress beyond a threshold:

```powershell
python -m kyvoris_profiler compare reports\baseline.json reports\candidate.json --max-regression-percent 5 --threshold-metric average_ms --threshold-metric p95_ms --fail-on-regression
```

Version `0.7.1` adds TOML config support for repeatable comparison settings:

```powershell
python -m kyvoris_profiler compare --config kyvoris-profiler.toml
```

Command-line arguments override values from the config file.

## Benchmark History Example

Version `0.12.0` includes a lightweight JSONL history workflow for saved JSON
summary reports with environment and custom metadata:

```powershell
python -m kyvoris_profiler history append reports\baseline.json --history reports\history.jsonl --label baseline --metadata model=distilbert
python -m kyvoris_profiler history append reports\candidate.json --history reports\history.jsonl --label candidate --metadata model=roberta
python -m kyvoris_profiler history list --history reports\history.jsonl --metadata model=roberta --limit 5
python -m kyvoris_profiler history compare --history reports\history.jsonl --baseline latest:baseline --candidate latest:candidate --format markdown --output reports\history-selected-comparison.md
python -m kyvoris_profiler history compare-latest --history reports\history.jsonl --format markdown --output reports\history-comparison.md
```

History comparison supports the same threshold flags as direct comparison:

```powershell
python -m kyvoris_profiler history compare-latest --history reports\history.jsonl --max-regression-percent 5 --threshold-metric average_ms --fail-on-regression
```

## API Overview

### `benchmark_callable(callable_obj, iterations=10, warmup=0)`

Runs a no-argument callable multiple times and returns a `LatencySummary`.
Warmup calls run before timing starts.

```python
summary = benchmark_callable(run_inference, iterations=10, warmup=1)
```

### `profile_callable(callable_obj, iterations=10, warmup=0, collect_memory=False, collect_cpu=False, continue_on_error=False)`

Runs the same benchmark loop as `benchmark_callable()`, with optional resource
metrics:

```python
summary = profile_callable(
    run_inference,
    iterations=10,
    warmup=1,
    collect_memory=True,
    collect_cpu=True,
)
```

`collect_memory=True` records peak Python allocations observed by `tracemalloc`.
It does not include GPU memory or every native allocation made by model
frameworks. `collect_cpu=True` records process CPU time consumed by the callable.
Use `continue_on_error=True` to keep measuring after failed iterations. Failed
iterations are counted but excluded from latency and resource statistics.

### `profile_async_callable(callable_obj, iterations=10, warmup=0, collect_memory=False, collect_cpu=False, continue_on_error=False)`

Profiles a no-argument async callable and returns a `ProfileSummary`:

```python
summary = await profile_async_callable(run_async_inference, iterations=10, warmup=1)
```

### `profile_http_endpoint(url, iterations=10, warmup=0, method="GET", ...)`

Profiles a simple HTTP endpoint using Python's standard library:

```python
summary = profile_http_endpoint("https://example.com", iterations=3, warmup=1)
```

### `compare_profiles(baseline, candidate, baseline_label="Baseline", candidate_label="Candidate")`

Compares two `ProfileSummary` objects and returns a `ProfileComparison`:

```python
comparison = compare_profiles(baseline, candidate, "main", "optimized")
```

### `evaluate_thresholds(comparison, max_regression_percent, metrics=None)`

Evaluates comparison regressions against a percentage threshold:

```python
evaluation = evaluate_thresholds(
    comparison,
    max_regression_percent=5.0,
    metrics={"average_ms", "p95_ms"},
)
```

Use this for CI gates where a pull request should fail if latency regresses more
than an allowed percentage.

The callable can wrap:

- a local model inference call
- a remote HTTP inference request
- a retrieval or reranking step
- a preprocessing or postprocessing function
- any other repeatable unit of work

### `ProfileSummary`

Immutable dataclass containing:

| Field | Meaning |
| --- | --- |
| `average_ms` | Mean latency across all measured runs |
| `min_ms` | Fastest measured run |
| `max_ms` | Slowest measured run |
| `p50_ms` | Median latency |
| `p95_ms` | Slower-end latency often useful for user-facing performance |
| `iterations` | Number of measured runs |
| `warmup_iterations` | Number of untimed warmup runs before measurement |
| `failed_iterations` | Failed measured iterations captured with `continue_on_error=True` |
| `average_cpu_ms` | Average process CPU time when CPU collection is enabled |
| `min_cpu_ms` | Minimum process CPU time when CPU collection is enabled |
| `max_cpu_ms` | Maximum process CPU time when CPU collection is enabled |
| `peak_memory_kb` | Peak Python-traced memory allocation when memory collection is enabled |

Use `summary.as_dict()` when you need a plain dictionary for serialization or
custom reporting.

For a deeper explanation of every field, see [docs/metrics.md](docs/metrics.md).

### Reporting

```python
from kyvoris_profiler import (
    format_csv_report,
    format_html_report,
    format_json_report,
    format_markdown_report,
    format_text_report,
)

print(format_text_report(summary))
print(format_markdown_report(summary))
print(format_json_report(summary))
print(format_html_report(summary))
print(format_csv_report(summary))
```

`format_text_report()` is useful for terminal output. `format_markdown_report()`
is useful for README snippets, CI comments, and benchmark artifacts.
`format_json_report()` is useful for automation and storage. `format_html_report()`
is useful for standalone benchmark artifacts. `format_csv_report()` is useful
for spreadsheets and table-based analysis.

For machine-readable formats, see [docs/report-schema.md](docs/report-schema.md).

## Project Layout

```text
kyvoris-profiler/
|-- docs/
|   |-- design/
|   |   `-- technical-design.md
|   |-- cli.md
|   |-- examples.md
|   |-- github-issues.md
|   |-- metrics.md
|   |-- pull-request-descriptions.md
|   |-- report-schema.md
|   |-- weekly-milestones.md
|   `-- roadmap.md
|-- examples/
|   |-- run_async_demo.py
|   |-- run_comparison_demo.py
|   |-- run_demo.py
|   |-- run_endpoint_demo.py
|   `-- run_model_demo.py
|-- src/
|   `-- kyvoris_profiler/
|       |-- benchmark.py
|       |-- cli.py
|       |-- compare.py
|       |-- endpoint.py
|       |-- history.py
|       |-- metrics.py
|       |-- report.py
|       `-- __init__.py
|-- tests/
|   |-- fixtures/
|   |-- test_benchmark.py
|   |-- test_benchmark_pytest.py
|   `-- test_cli.py
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

Run the project test runner:

```powershell
.\scripts\test-all.ps1
```

If PowerShell blocks local scripts on your machine, use a one-time bypass:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\test-all.ps1
```

The test runner includes CLI coverage, but you can also run the CLI checks
directly:

```powershell
$env:PYTHONPATH="src"
python -m kyvoris_profiler examples.run_demo:simulated_inference --iterations 3 --warmup 1 --collect-cpu --collect-memory
python -m kyvoris_profiler examples.run_demo:simulated_inference --iterations 3 --format json --output reports\cli-smoke.json
python -m kyvoris_profiler examples.run_demo:simulated_inference --iterations 3 --format html --output reports\cli-smoke.html
python -m kyvoris_profiler examples.run_demo:simulated_inference --iterations 3 --format csv --output reports\cli-smoke.csv
python -m kyvoris_profiler examples.run_async_demo:simulated_async_inference --iterations 3 --warmup 1
python -m kyvoris_profiler compare reports\baseline-smoke.json reports\candidate-smoke.json --format markdown --output reports\comparison-smoke.md
python -m kyvoris_profiler compare reports\baseline-smoke.json reports\candidate-smoke.json --format html --output reports\comparison-smoke.html
python -m kyvoris_profiler compare reports\baseline-smoke.json reports\candidate-smoke.json --format csv --output reports\comparison-smoke.csv
python -m kyvoris_profiler compare reports\baseline-smoke.json reports\candidate-smoke.json --max-regression-percent 100 --threshold-metric average_ms --fail-on-regression
python -m kyvoris_profiler compare --config kyvoris-profiler.toml --format markdown --output reports\config-comparison-smoke.md --max-regression-percent 100 --threshold-metric average_ms
python -m kyvoris_profiler history append reports\baseline-smoke.json --history reports\history-smoke.jsonl --label baseline
python -m kyvoris_profiler history append reports\candidate-smoke.json --history reports\history-smoke.jsonl --label candidate
python -m kyvoris_profiler history list --history reports\history-smoke.jsonl
python -m kyvoris_profiler history list --history reports\history-smoke.jsonl --metadata model=candidate-demo --limit 1
python -m kyvoris_profiler history compare --history reports\history-smoke.jsonl --baseline 1 --candidate 2 --format markdown --output reports\history-selected-comparison-smoke.md
python -m kyvoris_profiler history compare --history reports\history-smoke.jsonl --baseline latest:baseline --candidate latest:candidate --format markdown --output reports\history-latest-label-comparison-smoke.md
python -m kyvoris_profiler history compare-latest --history reports\history-smoke.jsonl --format markdown --output reports\history-comparison-smoke.md
```

After installing the package locally, test the console script:

```powershell
python -m pip install -e .
kyvoris-profiler examples.run_demo:simulated_inference --iterations 3 --warmup 1 --collect-cpu --collect-memory
```

Include the optional Hugging Face model example:

```powershell
.\scripts\test-all.ps1 -IncludeHuggingFace
```

Install Hugging Face dependencies before running the model example:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\test-all.ps1 -InstallHuggingFace -IncludeHuggingFace
```

## Design Principles

- Keep the benchmark core small, explicit, and easy to audit.
- Make units obvious: latency values are reported in milliseconds.
- Make resource metric scope explicit: memory is Python-traced allocation, CPU
  is process CPU time.
- Separate measurement, metric calculation, and report formatting.
- Avoid provider lock-in; the callable wrapper decides what is being measured.
- Keep optional model dependencies out of the core package.

## Development Transparency

Parts of this project were developed with assistance from AI coding tools. All
changes are reviewed, tested, and accepted by the human maintainer before being
committed.

## Roadmap

Planned areas include:

- CSV exports
- benchmark labels and metadata
- benchmark history workflows
- support for callables with arguments
- inference-specific metrics such as tokens per second and time to first token
- native process, GPU, and framework-specific memory adapters
- comparison reports for multiple benchmark runs

See [docs/roadmap.md](docs/roadmap.md) for the full roadmap, and
[RELEASE_NOTES.md](RELEASE_NOTES.md) for release history.

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
