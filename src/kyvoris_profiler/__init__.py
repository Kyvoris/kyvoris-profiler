"""Public API for Kyvoris Profiler."""

from kyvoris_profiler.benchmark import (
    benchmark_async_callable,
    benchmark_callable,
    profile_async_callable,
    profile_callable,
)
from kyvoris_profiler.compare import (
    MetricComparison,
    ProfileComparison,
    ThresholdEvaluation,
    ThresholdViolation,
    compare_profiles,
    evaluate_thresholds,
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
    format_comparison_csv_report,
    format_comparison_html_report,
    format_comparison_json_report,
    format_comparison_markdown_report,
    format_comparison_text_report,
    format_csv_report,
    format_html_report,
    format_json_report,
    format_markdown_report,
    format_text_report,
)

__all__ = [
    "LatencySummary",
    "MetricComparison",
    "ProfileComparison",
    "ProfileSummary",
    "ThresholdEvaluation",
    "ThresholdViolation",
    "benchmark_async_callable",
    "benchmark_callable",
    "compare_profiles",
    "evaluate_thresholds",
    "format_comparison_html_report",
    "format_comparison_json_report",
    "format_comparison_markdown_report",
    "format_comparison_text_report",
    "format_comparison_csv_report",
    "format_csv_report",
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

__version__ = "0.8.0"
