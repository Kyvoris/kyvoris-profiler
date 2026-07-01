"""Reporting helpers for benchmark summaries."""

from __future__ import annotations

from kyvoris_profiler.metrics import LatencySummary


def format_text_report(summary: LatencySummary, title: str = "Benchmark Results") -> str:
    """Format a latency summary as a readable plain-text report."""
    lines = [
        title,
        "-" * len(title),
        f"Iterations: {summary.iterations}",
        f"Average:    {summary.average_ms:.3f} ms",
        f"Minimum:    {summary.min_ms:.3f} ms",
        f"Maximum:    {summary.max_ms:.3f} ms",
        f"P50:        {summary.p50_ms:.3f} ms",
        f"P95:        {summary.p95_ms:.3f} ms",
    ]
    return "\n".join(lines)


def format_markdown_report(
    summary: LatencySummary,
    title: str = "Benchmark Results",
) -> str:
    """Format a latency summary as a Markdown table."""
    return "\n".join(
        [
            f"## {title}",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            f"| Iterations | {summary.iterations} |",
            f"| Average | {summary.average_ms:.3f} ms |",
            f"| Minimum | {summary.min_ms:.3f} ms |",
            f"| Maximum | {summary.max_ms:.3f} ms |",
            f"| P50 | {summary.p50_ms:.3f} ms |",
            f"| P95 | {summary.p95_ms:.3f} ms |",
        ]
    )
