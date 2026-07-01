# CLI

Version `0.10.0` includes benchmark, comparison, threshold, TOML config, and
history workflows:

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
| `--format csv` | CSV report |
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

Version `0.7.1` adds TOML config support:

```powershell
kyvoris-profiler compare --config kyvoris-profiler.toml
```

CLI arguments override config values:

```powershell
kyvoris-profiler compare --config kyvoris-profiler.toml --format html --output reports\comparison.html
```

Append saved JSON reports to a history file, list saved records, and compare the
latest two entries:

```powershell
kyvoris-profiler history append reports\baseline.json --history reports\history.jsonl --label baseline --metadata model=distilbert
kyvoris-profiler history append reports\candidate.json --history reports\history.jsonl --label candidate --metadata model=roberta
kyvoris-profiler history list --history reports\history.jsonl
kyvoris-profiler history compare-latest --history reports\history.jsonl --format markdown --output reports\history-comparison.md
```

## Compare Command

```powershell
kyvoris-profiler compare <baseline.json> <candidate.json> [options]
```

| Option | Meaning |
| --- | --- |
| `--baseline-label TEXT` | Label for the baseline report |
| `--candidate-label TEXT` | Label for the candidate report |
| `--config PATH` | TOML comparison config file |
| `--format text` | Plain text comparison |
| `--format markdown` | Markdown comparison |
| `--format json` | JSON comparison |
| `--format html` | HTML comparison |
| `--format csv` | CSV comparison |
| `--output PATH` | Write the comparison to a file |
| `--title TEXT` | Set the comparison title |
| `--max-regression-percent N` | Allowed regression percentage |
| `--threshold-metric NAME` | Metric to evaluate; can be passed multiple times |
| `--fail-on-regression` | Exit with code 1 when threshold violations are found |

## History Command

Append a summary JSON report:

```powershell
kyvoris-profiler history append <report.json> --history <history.jsonl> --label <label>
```

By default, appended records include Python, platform, and git commit metadata
when available. Add custom metadata with `--metadata KEY=VALUE`, or use
`--no-environment-metadata` to store only explicit values.

List records:

```powershell
kyvoris-profiler history list --history <history.jsonl>
```

Compare the latest two history records:

```powershell
kyvoris-profiler history compare-latest --history <history.jsonl> [options]
```

| Option | Meaning |
| --- | --- |
| `--history PATH` | History JSONL file. Default: `reports/history.jsonl` |
| `--label TEXT` | Label used when appending a record |
| `--metadata KEY=VALUE` | Metadata stored on append; can be passed multiple times |
| `--no-environment-metadata` | Skip automatic Python, platform, and git metadata |
| `--format text` | Plain text comparison |
| `--format markdown` | Markdown comparison |
| `--format json` | JSON comparison |
| `--format html` | HTML comparison |
| `--format csv` | CSV comparison |
| `--output PATH` | Write the comparison to a file |
| `--title TEXT` | Set the comparison title |
| `--max-regression-percent N` | Allowed regression percentage |
| `--threshold-metric NAME` | Metric to evaluate; can be passed multiple times |
| `--fail-on-regression` | Exit with code 1 when threshold violations are found |

## TOML Config

Use `kyvoris-profiler.toml` for repeatable comparison settings:

```toml
[compare]
baseline = "reports/baseline.json"
candidate = "reports/candidate.json"
baseline_label = "baseline"
candidate_label = "candidate"
format = "markdown"
output = "reports/comparison.md"
title = "Benchmark Comparison"

[thresholds]
max_regression_percent = 5
metrics = ["average_ms", "p95_ms", "failed_iterations"]
fail_on_regression = true
```

## Current Limits

- The callable must take no arguments.
- Async callable targets are detected automatically.
- Memory metrics are Python-traced allocations from `tracemalloc`, not GPU
  memory or full native framework memory.
- CPU metrics are process CPU time, not system-wide utilization.
