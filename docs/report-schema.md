# Report Schema

Kyvoris Profiler supports human-readable and machine-readable report formats.
JSON is the canonical machine-readable format. CSV is intended for spreadsheets,
quick analysis, and table-based exports. JSONL is used for benchmark history.

## Summary JSON

Summary JSON is produced with:

```powershell
python -m kyvoris_profiler examples.run_demo:simulated_inference --format json --output reports/summary.json
```

Shape:

```json
{
  "schema_version": "1.0",
  "title": "Benchmark Results",
  "metrics": {
    "average_ms": 5.1,
    "min_ms": 5.0,
    "max_ms": 5.4,
    "p50_ms": 5.1,
    "p95_ms": 5.3,
    "iterations": 10,
    "warmup_iterations": 1,
    "failed_iterations": 0,
    "average_cpu_ms": null,
    "min_cpu_ms": null,
    "max_cpu_ms": null,
    "peak_memory_kb": null
  }
}
```

`schema_version` is included so downstream tooling can detect future schema
changes.

## Summary CSV

Summary CSV is produced with:

```powershell
python -m kyvoris_profiler examples.run_demo:simulated_inference --format csv --output reports/summary.csv
```

Shape:

```csv
title,Benchmark Results
metric,value
Iterations,10
Warmup,1
Failures,0
Average,5.100 ms
```

CSV values are formatted for readability and spreadsheet use.

## Comparison JSON

Comparison JSON is produced with:

```powershell
python -m kyvoris_profiler compare reports/baseline.json reports/candidate.json --format json --output reports/comparison.json
```

Shape:

```json
{
  "schema_version": "1.0",
  "title": "Benchmark Comparison",
  "comparison": {
    "baseline_label": "Baseline",
    "candidate_label": "Candidate",
    "metrics": [
      {
        "metric": "average_ms",
        "baseline": 10.0,
        "candidate": 12.0,
        "delta": 2.0,
        "percent_change": 20.0,
        "improved": false,
        "result": "regressed"
      }
    ]
  }
}
```

## Comparison CSV

Comparison CSV is produced with:

```powershell
python -m kyvoris_profiler compare reports/baseline.json reports/candidate.json --format csv --output reports/comparison.csv
```

Shape:

```csv
title,Benchmark Comparison
baseline_label,Baseline
candidate_label,Candidate

metric,baseline,candidate,delta,percent_change,result
average_ms,10.000,12.000,+2.000,+20.00%,regressed
```

Use comparison CSV when you want to inspect deltas in Excel or another
spreadsheet tool.

## History JSONL

History JSONL is produced by appending summary JSON reports:

```powershell
python -m kyvoris_profiler history append reports/summary.json --history reports/history.jsonl --label main
```

Each line is a standalone JSON object:

```json
{
  "label": "main",
  "source": "reports/summary.json",
  "metadata": {
    "git_commit": "38e6845",
    "model": "distilbert",
    "platform": "Windows-11-10.0.26100-SP0",
    "python_implementation": "CPython",
    "python_version": "3.13.14"
  },
  "summary": {
    "average_ms": 5.1,
    "min_ms": 5.0,
    "max_ms": 5.4,
    "p50_ms": 5.1,
    "p95_ms": 5.3,
    "iterations": 10,
    "warmup_iterations": 1,
    "failed_iterations": 0,
    "average_cpu_ms": null,
    "min_cpu_ms": null,
    "max_cpu_ms": null,
    "peak_memory_kb": null
  },
  "timestamp": "2026-07-01T12:00:00+00:00"
}
```

History records intentionally store the normalized `ProfileSummary` metrics, not
the original report title. Use `label` to identify the branch, model, version,
or run being compared. `metadata` is an object of string key/value pairs. New
records include environment metadata by default; older history records without
metadata are still valid.
