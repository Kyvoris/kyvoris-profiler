"""Compare two Kyvoris Profiler benchmark summaries."""

from __future__ import annotations

import time

from kyvoris_profiler import (
    compare_profiles,
    format_comparison_text_report,
    profile_callable,
)


def baseline_inference() -> str:
    """Stand in for the slower implementation."""
    time.sleep(0.006)
    return "ok"


def candidate_inference() -> str:
    """Stand in for the optimized implementation."""
    time.sleep(0.004)
    return "ok"


if __name__ == "__main__":
    baseline = profile_callable(baseline_inference, iterations=5, warmup=1)
    candidate = profile_callable(candidate_inference, iterations=5, warmup=1)
    comparison = compare_profiles(
        baseline,
        candidate,
        baseline_label="baseline",
        candidate_label="candidate",
    )
    print(format_comparison_text_report(comparison))
