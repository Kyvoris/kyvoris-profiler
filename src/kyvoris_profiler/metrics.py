"""Metric primitives for Kyvoris Profiler."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable


@dataclass(frozen=True)
class LatencySummary:
    """Summary statistics for latency measurements in milliseconds."""

    average_ms: float
    min_ms: float
    max_ms: float
    p50_ms: float
    p95_ms: float
    iterations: int

    def as_dict(self) -> dict[str, float]:
        """Return the summary as a plain dictionary."""
        return asdict(self)


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


def summarize_latencies(latencies_ms: Iterable[float]) -> LatencySummary:
    """Build a latency summary from millisecond measurements."""
    sorted_latencies = sorted(latencies_ms)
    if not sorted_latencies:
        raise ValueError("latencies_ms cannot be empty")

    return LatencySummary(
        average_ms=sum(sorted_latencies) / len(sorted_latencies),
        min_ms=sorted_latencies[0],
        max_ms=sorted_latencies[-1],
        p50_ms=percentile(sorted_latencies, 50.0),
        p95_ms=percentile(sorted_latencies, 95.0),
        iterations=len(sorted_latencies),
    )
