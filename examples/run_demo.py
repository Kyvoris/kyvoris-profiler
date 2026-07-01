"""Run a small Kyvoris Profiler benchmark demo."""

from __future__ import annotations

import time

from kyvoris_profiler import benchmark_callable, format_text_report


def simulated_inference() -> str:
    """Stand in for a local or remote model inference call."""
    time.sleep(0.005)
    return "ok"


if __name__ == "__main__":
    result = benchmark_callable(simulated_inference, iterations=5)
    print(format_text_report(result, title="Simulated Inference Benchmark"))
