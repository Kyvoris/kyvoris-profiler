"""Comparison helpers for benchmark summaries."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from kyvoris_profiler.metrics import ProfileSummary


@dataclass(frozen=True)
class MetricComparison:
    """Comparison for a single numeric metric."""

    metric: str
    baseline: float
    candidate: float
    delta: float
    percent_change: float | None
    improved: bool
    result: str

    def as_dict(self) -> dict[str, float | str | bool | None]:
        """Return the comparison as a plain dictionary."""
        return asdict(self)


@dataclass(frozen=True)
class ProfileComparison:
    """Comparison between two profile summaries."""

    baseline_label: str
    candidate_label: str
    metrics: tuple[MetricComparison, ...]

    def as_dict(self) -> dict[str, object]:
        """Return the comparison as a plain dictionary."""
        return {
            "baseline_label": self.baseline_label,
            "candidate_label": self.candidate_label,
            "metrics": [metric.as_dict() for metric in self.metrics],
        }


LOWER_IS_BETTER_METRICS = {
    "average_ms",
    "min_ms",
    "max_ms",
    "p50_ms",
    "p95_ms",
    "average_cpu_ms",
    "min_cpu_ms",
    "max_cpu_ms",
    "peak_memory_kb",
    "failed_iterations",
}


def compare_profiles(
    baseline: ProfileSummary,
    candidate: ProfileSummary,
    baseline_label: str = "Baseline",
    candidate_label: str = "Candidate",
) -> ProfileComparison:
    """Compare two profile summaries."""
    metric_names = [
        "average_ms",
        "min_ms",
        "max_ms",
        "p50_ms",
        "p95_ms",
        "average_cpu_ms",
        "min_cpu_ms",
        "max_cpu_ms",
        "peak_memory_kb",
        "failed_iterations",
    ]
    comparisons: list[MetricComparison] = []

    for metric_name in metric_names:
        baseline_value = getattr(baseline, metric_name)
        candidate_value = getattr(candidate, metric_name)
        if baseline_value is None or candidate_value is None:
            continue

        baseline_float = float(baseline_value)
        candidate_float = float(candidate_value)
        delta = candidate_float - baseline_float
        percent_change = (
            (delta / baseline_float) * 100.0 if baseline_float != 0.0 else None
        )
        if candidate_float == baseline_float:
            improved = False
            result = "unchanged"
        elif metric_name in LOWER_IS_BETTER_METRICS:
            improved = candidate_float < baseline_float
            result = "improved" if improved else "regressed"
        else:
            improved = candidate_float > baseline_float
            result = "improved" if improved else "regressed"
        comparisons.append(
            MetricComparison(
                metric=metric_name,
                baseline=baseline_float,
                candidate=candidate_float,
                delta=delta,
                percent_change=percent_change,
                improved=improved,
                result=result,
            )
        )

    return ProfileComparison(
        baseline_label=baseline_label,
        candidate_label=candidate_label,
        metrics=tuple(comparisons),
    )
