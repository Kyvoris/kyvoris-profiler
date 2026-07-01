# Metrics Explained

Kyvoris Profiler reports latency, optional resource metrics, and run metadata.
This guide explains what each field means, how to interpret it, and what it does
not measure.

## Timing Units

All latency and CPU timing values are reported in milliseconds.

```text
1 second = 1,000 milliseconds
```

Memory values are reported in kilobytes.

## Latency Metrics

Latency metrics answer this question:

```text
How long did the measured callable take from start to finish?
```

Kyvoris Profiler measures latency using wall-clock time. Wall-clock time is the
real elapsed time a user or caller experiences.

### `average_ms`

The average wall-clock latency across all successful measured iterations.

Example:

```json
"average_ms": 5.075
```

This means the measured callable took about 5.075 milliseconds on average.

Use this for a quick overall performance signal, but do not rely on it alone.
One very slow run can pull the average upward, and one very fast run can make a
small sample look better than it really is.

### `min_ms`

The fastest successful measured iteration.

Example:

```json
"min_ms": 5.037
```

This is useful for understanding the best observed case, but it is usually not
representative of real user experience. Treat it as a lower bound, not a promise.

### `max_ms`

The slowest successful measured iteration.

Example:

```json
"max_ms": 5.134
```

This helps reveal occasional slow runs. With enough iterations, a high maximum
can point to cold caches, garbage collection, network jitter, throttling, or
contention with other processes.

### `p50_ms`

The 50th percentile latency, also called the median.

Example:

```json
"p50_ms": 5.055
```

Half of successful measured runs were faster than this value, and half were
slower. P50 is often more stable than the average when there are occasional
outliers.

### `p95_ms`

The 95th percentile latency.

Example:

```json
"p95_ms": 5.126
```

P95 estimates the slower-end experience. In user-facing systems, p95 is often
more important than the average because users notice slow responses.

With very small iteration counts, such as 3 or 5, p95 is only a rough signal.
Use more iterations when you need stronger confidence.

## Run Metadata

Run metadata explains how the benchmark was executed.

### `iterations`

The number of successful measured runs included in the latency summary.

Example:

```json
"iterations": 3
```

This means three successful measured runs were used for the summary.

If `continue_on_error=True` is enabled and some measured runs fail, failed runs
are not included in latency statistics.

### `warmup_iterations`

The number of untimed calls made before measurement starts.

Example:

```json
"warmup_iterations": 1
```

Warmup runs are useful for model and endpoint workloads because the first call
can include one-time setup, such as:

- model loading
- tokenizer setup
- backend initialization
- connection setup
- cache population

Warmup calls are not included in latency statistics.

### `failed_iterations`

The number of measured iterations that failed when error capture is enabled.

Example:

```json
"failed_iterations": 0
```

If this value is greater than zero, some measured calls failed. Successful calls
are still summarized, but you should treat the result carefully because failures
are part of the workload behavior.

Failed iterations are counted only when profiling is run with
`continue_on_error=True`. Without that option, the first exception is raised and
the benchmark stops.

## CPU Metrics

CPU metrics answer this question:

```text
How much CPU time did this Python process spend during the measured callable?
```

CPU time is different from wall-clock time.

### `average_cpu_ms`

The average process CPU time used by successful measured iterations.

Example:

```json
"average_cpu_ms": 0.120
```

This means the Python process used about 0.120 milliseconds of CPU time per
successful measured iteration on average.

### `min_cpu_ms`

The lowest process CPU time observed across successful measured iterations.

### `max_cpu_ms`

The highest process CPU time observed across successful measured iterations.

### Why CPU Can Be `null`

CPU fields are `null` when CPU collection was not enabled.

CLI:

```powershell
python -m kyvoris_profiler examples.run_demo:simulated_inference --collect-cpu
```

Python:

```python
summary = profile_callable(run_inference, collect_cpu=True)
```

### `average_ms` vs `average_cpu_ms`

`average_ms` is wall-clock time: how long the caller waited.

`average_cpu_ms` is process CPU time: how much CPU work the Python process used.

Example:

```python
time.sleep(0.005)
```

This can produce:

```text
average_ms: 5.0 ms
average_cpu_ms: 0.0 ms
```

The program waited for about 5 milliseconds, but it did not use much CPU while
sleeping.

For local CPU-heavy inference, CPU time may be close to wall-clock latency. For
remote API calls, wall-clock latency can be high while CPU time stays low. For
GPU workloads, CPU time does not fully describe GPU work.

## Memory Metrics

Memory metrics answer this question:

```text
What was the peak Python-traced memory allocation during measured iterations?
```

### `peak_memory_kb`

The highest peak memory allocation observed by Python's `tracemalloc` during
successful measured iterations.

Example:

```json
"peak_memory_kb": 42.5
```

This means the highest Python-traced allocation peak was about 42.5 KB.

### Why Memory Can Be `null`

Memory is `null` when memory collection was not enabled.

CLI:

```powershell
python -m kyvoris_profiler examples.run_demo:simulated_inference --collect-memory
```

Python:

```python
summary = profile_callable(run_inference, collect_memory=True)
```

### What `peak_memory_kb` Does Not Measure

`peak_memory_kb` uses Python's `tracemalloc`, so it tracks Python-level
allocations. It does not fully measure:

- GPU memory
- full process memory
- native framework allocations outside Python tracing
- operating system memory pressure

This makes it useful for Python-heavy preprocessing, postprocessing, and wrapper
logic. It is not a complete memory profiler for large model runtimes.

## Interpreting Results by Workload Type

### Simulated or Sleep-Based Workloads

If a function mostly waits, such as `time.sleep()`, wall-clock latency can be
much higher than CPU time.

Expected shape:

```text
average_ms: high relative to CPU
average_cpu_ms: near zero
```

### Local CPU Model

If inference runs mostly on CPU, wall-clock latency and CPU time may be closer.

Expected shape:

```text
average_ms: meaningful user wait time
average_cpu_ms: meaningful CPU usage
```

### Remote API or HTTP Endpoint

For remote endpoints, wall-clock latency includes network time and server
response time. CPU time often stays low because the local process is waiting.

Expected shape:

```text
average_ms: includes network and remote processing
average_cpu_ms: often much lower
```

### GPU Model

For GPU workloads, wall-clock latency includes time spent waiting for GPU work,
but process CPU time does not fully reflect GPU utilization.

Expected shape:

```text
average_ms: useful end-to-end latency
average_cpu_ms: incomplete view of total compute
peak_memory_kb: not GPU memory
```

## Practical Guidance

- Use at least 10 to 30 iterations for quick local checks.
- Use more iterations for noisy endpoints or release comparisons.
- Use warmup for model workloads.
- Prefer p50 and p95 when user experience matters.
- Use CPU and memory metrics as supporting signals, not the only decision point.
- Compare runs on the same machine, power mode, Python version, and dependency
  set whenever possible.
- Keep threshold settings in `kyvoris-profiler.toml` when the same regression
  policy should run repeatedly in CI.
