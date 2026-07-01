"""Public API for Kyvoris Profiler."""

from kyvoris_profiler.benchmark import benchmark_callable, profile_callable
from kyvoris_profiler.metrics import (
    LatencySummary,
    ProfileSummary,
    percentile,
    summarize_latencies,
    summarize_profile,
)
from kyvoris_profiler.report import (
    format_html_report,
    format_json_report,
    format_markdown_report,
    format_text_report,
)

__all__ = [
    "LatencySummary",
    "ProfileSummary",
    "benchmark_callable",
    "format_html_report",
    "format_json_report",
    "format_markdown_report",
    "format_text_report",
    "percentile",
    "profile_callable",
    "summarize_latencies",
    "summarize_profile",
]

__version__ = "0.3.0"
