"""Public API for Kyvoris Profiler."""

from kyvoris_profiler.benchmark import benchmark_callable
from kyvoris_profiler.metrics import LatencySummary, percentile, summarize_latencies
from kyvoris_profiler.report import (
    format_html_report,
    format_json_report,
    format_markdown_report,
    format_text_report,
)

__all__ = [
    "LatencySummary",
    "benchmark_callable",
    "format_html_report",
    "format_json_report",
    "format_markdown_report",
    "format_text_report",
    "percentile",
    "summarize_latencies",
]

__version__ = "0.2.0"
