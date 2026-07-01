"""Reporting helpers for benchmark summaries."""

from __future__ import annotations

import json
from html import escape

from kyvoris_profiler.metrics import LatencySummary


def format_text_report(summary: LatencySummary, title: str = "Benchmark Results") -> str:
    """Format a latency summary as a readable plain-text report."""
    lines = [
        title,
        "-" * len(title),
        f"Iterations: {summary.iterations}",
        f"Warmup:     {summary.warmup_iterations}",
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
            f"| Warmup | {summary.warmup_iterations} |",
            f"| Average | {summary.average_ms:.3f} ms |",
            f"| Minimum | {summary.min_ms:.3f} ms |",
            f"| Maximum | {summary.max_ms:.3f} ms |",
            f"| P50 | {summary.p50_ms:.3f} ms |",
            f"| P95 | {summary.p95_ms:.3f} ms |",
        ]
    )


def format_json_report(
    summary: LatencySummary,
    title: str = "Benchmark Results",
) -> str:
    """Format a latency summary as a stable JSON document."""
    payload = {
        "title": title,
        "schema_version": "1.0",
        "metrics": summary.as_dict(),
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def format_html_report(
    summary: LatencySummary,
    title: str = "Benchmark Results",
) -> str:
    """Format a latency summary as a standalone HTML report."""
    safe_title = escape(title)
    rows = [
        ("Iterations", str(summary.iterations)),
        ("Warmup", str(summary.warmup_iterations)),
        ("Average", f"{summary.average_ms:.3f} ms"),
        ("Minimum", f"{summary.min_ms:.3f} ms"),
        ("Maximum", f"{summary.max_ms:.3f} ms"),
        ("P50", f"{summary.p50_ms:.3f} ms"),
        ("P95", f"{summary.p95_ms:.3f} ms"),
    ]
    table_rows = "\n".join(
        f"        <tr><th>{escape(metric)}</th><td>{escape(value)}</td></tr>"
        for metric, value in rows
    )
    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="en">',
            "<head>",
            '  <meta charset="utf-8">',
            '  <meta name="viewport" content="width=device-width, initial-scale=1">',
            f"  <title>{safe_title}</title>",
            "  <style>",
            "    body { font-family: Arial, sans-serif; margin: 2rem; color: #1f2933; }",
            "    table { border-collapse: collapse; min-width: 20rem; }",
            "    th, td { border-bottom: 1px solid #d9e2ec; padding: 0.6rem 0.8rem; }",
            "    th { text-align: left; }",
            "    td { text-align: right; font-variant-numeric: tabular-nums; }",
            "  </style>",
            "</head>",
            "<body>",
            f"  <h1>{safe_title}</h1>",
            "  <table>",
            "    <tbody>",
            table_rows,
            "    </tbody>",
            "  </table>",
            "</body>",
            "</html>",
        ]
    )
