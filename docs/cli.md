# CLI

Version `0.4.0` adds a standard command-line entry point:

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

## Current Limits

- The callable must take no arguments.
- Async callable targets are detected automatically.
- Memory metrics are Python-traced allocations from `tracemalloc`, not GPU
  memory or full native framework memory.
- CPU metrics are process CPU time, not system-wide utilization.
