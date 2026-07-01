"""Benchmarking utilities for measuring Python callables."""

from __future__ import annotations

import time
import tracemalloc
from typing import Callable, TypeVar

from kyvoris_profiler.metrics import ProfileSummary, summarize_profile

T = TypeVar("T")


def benchmark_callable(
    callable_obj: Callable[[], T],
    iterations: int = 10,
    warmup: int = 0,
) -> ProfileSummary:
    """Measure the execution time of a no-argument callable."""
    return profile_callable(
        callable_obj,
        iterations=iterations,
        warmup=warmup,
    )


def profile_callable(
    callable_obj: Callable[[], T],
    iterations: int = 10,
    warmup: int = 0,
    collect_memory: bool = False,
    collect_cpu: bool = False,
) -> ProfileSummary:
    """Profile a no-argument callable with optional resource metrics."""
    if iterations <= 0:
        raise ValueError("iterations must be greater than 0")
    if warmup < 0:
        raise ValueError("warmup must be greater than or equal to 0")

    for _ in range(warmup):
        callable_obj()

    latencies_ms: list[float] = []
    cpu_times_ms: list[float] = []
    peak_memory_kb: float | None = None

    for _ in range(iterations):
        if collect_memory:
            tracemalloc.start()

        cpu_start = time.process_time() if collect_cpu else None
        start = time.perf_counter()
        callable_obj()
        elapsed_ms = (time.perf_counter() - start) * 1000.0

        if collect_cpu and cpu_start is not None:
            cpu_times_ms.append((time.process_time() - cpu_start) * 1000.0)

        if collect_memory:
            _, peak_bytes = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            iteration_peak_kb = peak_bytes / 1024.0
            if peak_memory_kb is None or iteration_peak_kb > peak_memory_kb:
                peak_memory_kb = iteration_peak_kb

        latencies_ms.append(elapsed_ms)

    return summarize_profile(
        latencies_ms,
        warmup_iterations=warmup,
        cpu_times_ms=cpu_times_ms if collect_cpu else None,
        peak_memory_kb=peak_memory_kb,
    )
