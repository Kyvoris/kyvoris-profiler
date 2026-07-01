"""Metric primitives for Kyvoris Profiler."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable


@dataclass(frozen=True)
class ProfileSummary:
    """Summary statistics for latency and optional resource measurements."""

    average_ms: float
    min_ms: float
    max_ms: float
    p50_ms: float
    p95_ms: float
    iterations: int
    warmup_iterations: int = 0
    failed_iterations: int = 0
    average_cpu_ms: float | None = None
    min_cpu_ms: float | None = None
    max_cpu_ms: float | None = None
    peak_memory_kb: float | None = None

    def as_dict(self) -> dict[str, float | int | None]:
        """Return the summary as a plain dictionary."""
        return asdict(self)


LatencySummary = ProfileSummary


def percentile(sorted_values: list[float], percentile_value: float) -> float:
    """Return a percentile from sorted values using linear interpolation."""
    if not sorted_values:
        raise ValueError("sorted_values cannot be empty")

    if not 0 <= percentile_value <= 100:
        raise ValueError("percentile_value must be between 0 and 100")

    if len(sorted_values) == 1:
        return sorted_values[0]

    rank = (len(sorted_values) - 1) * (percentile_value / 100.0)
    lower_index = int(rank)
    upper_index = min(lower_index + 1, len(sorted_values) - 1)
    weight = rank - lower_index

    return sorted_values[lower_index] + (
        sorted_values[upper_index] - sorted_values[lower_index]
    ) * weight


def summarize_latencies(
    latencies_ms: Iterable[float],
    warmup_iterations: int = 0,
) -> ProfileSummary:
    """Build a latency summary from millisecond measurements."""
    return summarize_profile(
        latencies_ms,
        warmup_iterations=warmup_iterations,
    )


def summarize_profile(
    latencies_ms: Iterable[float],
    warmup_iterations: int = 0,
    cpu_times_ms: Iterable[float] | None = None,
    peak_memory_kb: float | None = None,
    failed_iterations: int = 0,
) -> ProfileSummary:
    """Build a profile summary from latency and optional resource measurements."""
    if warmup_iterations < 0:
        raise ValueError("warmup_iterations must be greater than or equal to 0")
    if failed_iterations < 0:
        raise ValueError("failed_iterations must be greater than or equal to 0")
    if peak_memory_kb is not None and peak_memory_kb < 0:
        raise ValueError("peak_memory_kb must be greater than or equal to 0")

    sorted_latencies = sorted(latencies_ms)
    if not sorted_latencies:
        raise ValueError("latencies_ms cannot be empty")

    sorted_cpu_times: list[float] | None = None
    if cpu_times_ms is not None:
        sorted_cpu_times = sorted(cpu_times_ms)
        if len(sorted_cpu_times) != len(sorted_latencies):
            raise ValueError("cpu_times_ms must match latencies_ms length")

    return ProfileSummary(
        average_ms=sum(sorted_latencies) / len(sorted_latencies),
        min_ms=sorted_latencies[0],
        max_ms=sorted_latencies[-1],
        p50_ms=percentile(sorted_latencies, 50.0),
        p95_ms=percentile(sorted_latencies, 95.0),
        iterations=len(sorted_latencies),
        warmup_iterations=warmup_iterations,
        failed_iterations=failed_iterations,
        average_cpu_ms=(
            sum(sorted_cpu_times) / len(sorted_cpu_times)
            if sorted_cpu_times is not None
            else None
        ),
        min_cpu_ms=sorted_cpu_times[0] if sorted_cpu_times is not None else None,
        max_cpu_ms=sorted_cpu_times[-1] if sorted_cpu_times is not None else None,
        peak_memory_kb=peak_memory_kb,
    )
