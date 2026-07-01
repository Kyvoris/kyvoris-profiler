"""Reporting helpers for benchmark summaries."""

from __future__ import annotations

import json
from csv import writer
from html import escape
from io import StringIO

from kyvoris_profiler.compare import ProfileComparison
from kyvoris_profiler.metrics import ProfileSummary


def _metric_rows(summary: ProfileSummary) -> list[tuple[str, str]]:
    rows = [
        ("Iterations", str(summary.iterations)),
        ("Warmup", str(summary.warmup_iterations)),
        ("Failures", str(summary.failed_iterations)),
        ("Average", f"{summary.average_ms:.3f} ms"),
        ("Minimum", f"{summary.min_ms:.3f} ms"),
        ("Maximum", f"{summary.max_ms:.3f} ms"),
        ("P50", f"{summary.p50_ms:.3f} ms"),
        ("P95", f"{summary.p95_ms:.3f} ms"),
    ]
    if summary.average_cpu_ms is not None:
        rows.extend(
            [
                ("Average CPU", f"{summary.average_cpu_ms:.3f} ms"),
                ("Minimum CPU", f"{summary.min_cpu_ms:.3f} ms"),
                ("Maximum CPU", f"{summary.max_cpu_ms:.3f} ms"),
            ]
        )
    if summary.peak_memory_kb is not None:
        rows.append(("Peak Python Memory", f"{summary.peak_memory_kb:.3f} KB"))
    return rows


def format_text_report(summary: ProfileSummary, title: str = "Benchmark Results") -> str:
    """Format a latency summary as a readable plain-text report."""
    lines = [
        title,
        "-" * len(title),
    ]
    lines.extend(f"{metric}: {value}" for metric, value in _metric_rows(summary))
    return "\n".join(lines)


def format_markdown_report(
    summary: ProfileSummary,
    title: str = "Benchmark Results",
) -> str:
    """Format a latency summary as a Markdown table."""
    return "\n".join(
        [
            f"## {title}",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            *[f"| {metric} | {value} |" for metric, value in _metric_rows(summary)],
        ]
    )


def format_json_report(
    summary: ProfileSummary,
    title: str = "Benchmark Results",
) -> str:
    """Format a latency summary as a stable JSON document."""
    payload = {
        "title": title,
        "schema_version": "1.0",
        "metrics": summary.as_dict(),
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def format_csv_report(
    summary: ProfileSummary,
    title: str = "Benchmark Results",
) -> str:
    """Format a latency summary as CSV."""
    output = StringIO()
    csv_writer = writer(output, lineterminator="\n")
    csv_writer.writerow(["title", title])
    csv_writer.writerow(["metric", "value"])
    for metric, value in _metric_rows(summary):
        csv_writer.writerow([metric, value])
    return output.getvalue().rstrip("\n")


def format_html_report(
    summary: ProfileSummary,
    title: str = "Benchmark Results",
) -> str:
    """Format a latency summary as a standalone HTML report."""
    safe_title = escape(title)
    rows = _metric_rows(summary)
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


def _format_percent_change(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:+.2f}%"


def format_comparison_text_report(
    comparison: ProfileComparison,
    title: str = "Benchmark Comparison",
) -> str:
    """Format a profile comparison as a readable plain-text report."""
    lines = [
        title,
        "-" * len(title),
        f"Baseline:  {comparison.baseline_label}",
        f"Candidate: {comparison.candidate_label}",
        "",
        "Metric | Baseline | Candidate | Delta | Change | Result",
    ]
    for metric in comparison.metrics:
        lines.append(
            " | ".join(
                [
                    metric.metric,
                    f"{metric.baseline:.3f}",
                    f"{metric.candidate:.3f}",
                    f"{metric.delta:+.3f}",
                    _format_percent_change(metric.percent_change),
                    metric.result,
                ]
            )
        )
    return "\n".join(lines)


def format_comparison_markdown_report(
    comparison: ProfileComparison,
    title: str = "Benchmark Comparison",
) -> str:
    """Format a profile comparison as a Markdown table."""
    lines = [
        f"## {title}",
        "",
        f"Baseline: `{comparison.baseline_label}`",
        f"Candidate: `{comparison.candidate_label}`",
        "",
        "| Metric | Baseline | Candidate | Delta | Change | Result |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for metric in comparison.metrics:
        lines.append(
            "| "
            + " | ".join(
                [
                    metric.metric,
                    f"{metric.baseline:.3f}",
                    f"{metric.candidate:.3f}",
                    f"{metric.delta:+.3f}",
                    _format_percent_change(metric.percent_change),
                    metric.result,
                ]
            )
            + " |"
        )
    return "\n".join(lines)


def format_comparison_json_report(
    comparison: ProfileComparison,
    title: str = "Benchmark Comparison",
) -> str:
    """Format a profile comparison as a stable JSON document."""
    payload = {
        "title": title,
        "schema_version": "1.0",
        "comparison": comparison.as_dict(),
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def format_comparison_csv_report(
    comparison: ProfileComparison,
    title: str = "Benchmark Comparison",
) -> str:
    """Format a profile comparison as CSV."""
    output = StringIO()
    csv_writer = writer(output, lineterminator="\n")
    csv_writer.writerow(["title", title])
    csv_writer.writerow(["baseline_label", comparison.baseline_label])
    csv_writer.writerow(["candidate_label", comparison.candidate_label])
    csv_writer.writerow([])
    csv_writer.writerow(
        [
            "metric",
            "baseline",
            "candidate",
            "delta",
            "percent_change",
            "result",
        ]
    )
    for metric in comparison.metrics:
        csv_writer.writerow(
            [
                metric.metric,
                f"{metric.baseline:.3f}",
                f"{metric.candidate:.3f}",
                f"{metric.delta:+.3f}",
                _format_percent_change(metric.percent_change),
                metric.result,
            ]
        )
    return output.getvalue().rstrip("\n")


def format_comparison_html_report(
    comparison: ProfileComparison,
    title: str = "Benchmark Comparison",
) -> str:
    """Format a profile comparison as a standalone HTML report."""
    safe_title = escape(title)
    rows = "\n".join(
        "        <tr>"
        f"<th>{escape(metric.metric)}</th>"
        f"<td>{metric.baseline:.3f}</td>"
        f"<td>{metric.candidate:.3f}</td>"
        f"<td>{metric.delta:+.3f}</td>"
        f"<td>{escape(_format_percent_change(metric.percent_change))}</td>"
        f"<td>{escape(metric.result)}</td>"
        "</tr>"
        for metric in comparison.metrics
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
            "    table { border-collapse: collapse; min-width: 32rem; }",
            "    th, td { border-bottom: 1px solid #d9e2ec; padding: 0.6rem 0.8rem; }",
            "    th { text-align: left; }",
            "    td { text-align: right; font-variant-numeric: tabular-nums; }",
            "  </style>",
            "</head>",
            "<body>",
            f"  <h1>{safe_title}</h1>",
            f"  <p>Baseline: {escape(comparison.baseline_label)}</p>",
            f"  <p>Candidate: {escape(comparison.candidate_label)}</p>",
            "  <table>",
            "    <thead>",
            "      <tr><th>Metric</th><th>Baseline</th><th>Candidate</th><th>Delta</th><th>Change</th><th>Result</th></tr>",
            "    </thead>",
            "    <tbody>",
            rows,
            "    </tbody>",
            "  </table>",
            "</body>",
            "</html>",
        ]
    )
