"""Benchmarking utilities for measuring Python callables."""

from __future__ import annotations

import time
from typing import Callable, TypeVar

from kyvoris_profiler.metrics import LatencySummary, summarize_latencies

T = TypeVar("T")


def benchmark_callable(
    callable_obj: Callable[[], T],
    iterations: int = 10,
    warmup: int = 0,
) -> LatencySummary:
    """Measure the execution time of a no-argument callable."""
    if iterations <= 0:
        raise ValueError("iterations must be greater than 0")
    if warmup < 0:
        raise ValueError("warmup must be greater than or equal to 0")

    for _ in range(warmup):
        callable_obj()

    latencies_ms: list[float] = []
    for _ in range(iterations):
        start = time.perf_counter()
        callable_obj()
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        latencies_ms.append(elapsed_ms)

    return summarize_latencies(latencies_ms, warmup_iterations=warmup)
