"""Public API for Kyvoris Profiler."""

from kyvoris_profiler.benchmark import (
    benchmark_async_callable,
    benchmark_callable,
    profile_async_callable,
    profile_callable,
)
from kyvoris_profiler.endpoint import profile_http_endpoint
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
    "benchmark_async_callable",
    "benchmark_callable",
    "format_html_report",
    "format_json_report",
    "format_markdown_report",
    "format_text_report",
    "percentile",
    "profile_async_callable",
    "profile_callable",
    "profile_http_endpoint",
    "summarize_latencies",
    "summarize_profile",
]

__version__ = "0.5.0"
