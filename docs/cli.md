# CLI

Version `0.7.0` includes benchmark, comparison, and threshold command-line
workflows:

```powershell
kyvoris-profiler <module:function> [options]
```

The target must be a no-argument Python callable.

## Install for Local Use

```powershell
python -m pip install -e ".[dev]"
```

Then run:

```powershell
kyvoris-profiler examples.run_demo:simulated_inference --iterations 5
```

Without installing the console script, run:

```powershell
$env:PYTHONPATH="src"
python -m kyvoris_profiler examples.run_demo:simulated_inference --iterations 5
```

## Options

| Option | Meaning |
| --- | --- |
| `--iterations N` | Number of measured iterations |
| `--warmup N` | Number of untimed warmup calls |
| `--format text` | Plain text report |
| `--format markdown` | Markdown report |
| `--format json` | JSON report |
| `--format html` | HTML report |
| `--output PATH` | Write the report to a file |
| `--title TEXT` | Set the report title |
| `--collect-cpu` | Collect process CPU time |
| `--collect-memory` | Collect peak Python-traced memory |

## Examples

Plain text to stdout:

```powershell
kyvoris-profiler examples.run_demo:simulated_inference --iterations 5 --warmup 1
```

JSON artifact:

```powershell
kyvoris-profiler examples.run_demo:simulated_inference --format json --output reports/demo.json
```

HTML artifact with resource metrics:

```powershell
kyvoris-profiler examples.run_demo:simulated_inference --format html --output reports/demo.html --collect-cpu --collect-memory
```

Async callable target:

```powershell
kyvoris-profiler examples.run_async_demo:simulated_async_inference --iterations 3 --warmup 1
```

Compare two JSON reports:

```powershell
kyvoris-profiler compare reports\baseline.json reports\candidate.json --format markdown --output reports\comparison.md
```

Fail when selected metrics regress beyond 5%:

```powershell
kyvoris-profiler compare reports\baseline.json reports\candidate.json --max-regression-percent 5 --threshold-metric average_ms --threshold-metric p95_ms --fail-on-regression
```

## Compare Command

```powershell
kyvoris-profiler compare <baseline.json> <candidate.json> [options]
```

| Option | Meaning |
| --- | --- |
| `--baseline-label TEXT` | Label for the baseline report |
| `--candidate-label TEXT` | Label for the candidate report |
| `--format text` | Plain text comparison |
| `--format markdown` | Markdown comparison |
| `--format json` | JSON comparison |
| `--format html` | HTML comparison |
| `--output PATH` | Write the comparison to a file |
| `--title TEXT` | Set the comparison title |
| `--max-regression-percent N` | Allowed regression percentage |
| `--threshold-metric NAME` | Metric to evaluate; can be passed multiple times |
| `--fail-on-regression` | Exit with code 1 when threshold violations are found |

## Current Limits

- The callable must take no arguments.
- Async callable targets are detected automatically.
- Memory metrics are Python-traced allocations from `tracemalloc`, not GPU
  memory or full native framework memory.
- CPU metrics are process CPU time, not system-wide utilization.
