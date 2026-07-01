# Examples

Kyvoris Profiler includes two runnable examples:

- `examples/run_demo.py` benchmarks a simulated inference function.
- `examples/run_model_demo.py` benchmarks a real Hugging Face model inference
  call.

## Simulated Inference Demo

Run from the project root:

```powershell
$env:PYTHONPATH="src"
python examples\run_demo.py
```

This example uses `time.sleep(0.005)` as a stand-in for an inference call. It is
useful for verifying that the package, benchmark loop, and report formatting are
working locally.

## Real Model Inference Demo

Install the optional model dependencies:

```powershell
python -m pip install "transformers[torch]"
```

Then run:

```powershell
$env:PYTHONPATH="src"
python examples\run_model_demo.py
```

The script uses the Hugging Face `pipeline` API with:

```text
distilbert-base-uncased-finetuned-sst-2-english
```

It benchmarks sentiment analysis for this input:

```text
Kyvoris Profiler makes inference benchmarking simple.
```

## What the Real Model Demo Measures

The measured function is only the inference call:

```python
def run_inference() -> list[dict[str, float | str]]:
    return classifier(TEXT)
```

The model is loaded before the benchmark starts:

```python
classifier = pipeline("sentiment-analysis", model=MODEL_NAME)
```

The script also performs one warmup call before timing:

```python
sample_output = run_inference()
```

This matters because model loading, tokenization setup, backend initialization,
and first-run caches can make the first call much slower than normal inference.
The benchmark is intended to measure repeated inference latency, not setup time.

## Reading the Output

Example output:

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

- `Average` is the mean latency across all measured inference calls.
- `Minimum` is the fastest measured call.
- `Maximum` is the slowest measured call.
- `P50` is the median latency.
- `P95` represents slower-end normal latency and is often useful when checking
  user-facing responsiveness.

Your numbers will vary depending on hardware, installed backend, Python version,
power mode, and whether the model files are already cached.
