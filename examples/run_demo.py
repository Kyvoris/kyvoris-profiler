"""Run a small Kyvoris Profiler benchmark demo."""

from __future__ import annotations

import time

from kyvoris_profiler import format_text_report, profile_callable


def simulated_inference() -> str:
    """Stand in for a local or remote model inference call."""
    time.sleep(0.005)
    return "ok"


if __name__ == "__main__":
    result = profile_callable(
        simulated_inference,
        iterations=5,
        warmup=1,
        collect_cpu=True,
        collect_memory=True,
    )
    print(format_text_report(result, title="Simulated Inference Benchmark"))
