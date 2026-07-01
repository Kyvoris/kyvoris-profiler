import json
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from kyvoris_profiler import (
    LatencySummary,
    benchmark_callable,
    format_html_report,
    format_json_report,
    format_markdown_report,
    format_text_report,
    percentile,
    summarize_latencies,
)


def test_benchmark_callable_reports_summary_stats() -> None:
    def target() -> None:
        time.sleep(0.001)

    stats = benchmark_callable(target, iterations=5)

    assert isinstance(stats, LatencySummary)
    assert stats.iterations == 5
    assert stats.warmup_iterations == 0
    assert stats.average_ms > 0.0
    assert stats.max_ms >= stats.min_ms
    assert stats.p50_ms >= stats.min_ms
    assert stats.p95_ms <= stats.max_ms
    assert stats.as_dict()["iterations"] == 5


def test_benchmark_callable_rejects_non_positive_iterations() -> None:
    with pytest.raises(ValueError):
        benchmark_callable(lambda: None, iterations=0)


def test_benchmark_callable_runs_warmup_before_measured_iterations() -> None:
    calls = 0

    def target() -> None:
        nonlocal calls
        calls += 1

    stats = benchmark_callable(target, iterations=3, warmup=2)

    assert calls == 5
    assert stats.iterations == 3
    assert stats.warmup_iterations == 2


def test_benchmark_callable_rejects_negative_warmup() -> None:
    with pytest.raises(ValueError):
        benchmark_callable(lambda: None, warmup=-1)


def test_summarize_latencies_reports_expected_values() -> None:
    stats = summarize_latencies([1.0, 2.0, 3.0, 4.0], warmup_iterations=2)

    assert stats.average_ms == 2.5
    assert stats.min_ms == 1.0
    assert stats.max_ms == 4.0
    assert stats.p50_ms == 2.5
    assert stats.p95_ms == pytest.approx(3.85)
    assert stats.iterations == 4
    assert stats.warmup_iterations == 2


def test_percentile_validates_inputs() -> None:
    with pytest.raises(ValueError):
        percentile([], 50.0)

    with pytest.raises(ValueError):
        percentile([1.0], 101.0)


def test_report_formatters_include_key_metrics() -> None:
    stats = summarize_latencies([1.0, 2.0, 3.0], warmup_iterations=1)

    text_report = format_text_report(stats)
    markdown_report = format_markdown_report(stats)
    json_report = format_json_report(stats)
    html_report = format_html_report(stats)

    assert "Benchmark Results" in text_report
    assert "Iterations: 3" in text_report
    assert "Warmup:     1" in text_report
    assert "| Average | 2.000 ms |" in markdown_report
    assert json.loads(json_report)["metrics"]["warmup_iterations"] == 1
    assert "<!doctype html>" in html_report
    assert "<th>Warmup</th><td>1</td>" in html_report
