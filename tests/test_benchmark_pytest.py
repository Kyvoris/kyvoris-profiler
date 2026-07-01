import asyncio
import json
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from kyvoris_profiler import (
    LatencySummary,
    ProfileSummary,
    benchmark_callable,
    compare_profiles,
    evaluate_thresholds,
    format_comparison_html_report,
    format_comparison_json_report,
    format_comparison_markdown_report,
    format_comparison_text_report,
    format_html_report,
    format_json_report,
    format_markdown_report,
    format_text_report,
    percentile,
    profile_async_callable,
    profile_callable,
    profile_http_endpoint,
    summarize_latencies,
    summarize_profile,
)


def test_benchmark_callable_reports_summary_stats() -> None:
    def target() -> None:
        time.sleep(0.001)

    stats = benchmark_callable(target, iterations=5)

    assert isinstance(stats, LatencySummary)
    assert isinstance(stats, ProfileSummary)
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


def test_profile_callable_can_collect_resource_metrics() -> None:
    def target() -> list[int]:
        return [index for index in range(100)]

    stats = profile_callable(
        target,
        iterations=3,
        collect_cpu=True,
        collect_memory=True,
    )

    assert stats.iterations == 3
    assert stats.average_cpu_ms is not None
    assert stats.min_cpu_ms is not None
    assert stats.max_cpu_ms is not None
    assert stats.peak_memory_kb is not None
    assert stats.peak_memory_kb >= 0.0


def test_profile_callable_can_continue_after_failures() -> None:
    calls = 0

    def target() -> str:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise RuntimeError("temporary failure")
        return "ok"

    stats = profile_callable(target, iterations=3, continue_on_error=True)

    assert stats.iterations == 2
    assert stats.failed_iterations == 1


def test_profile_async_callable_reports_summary_stats() -> None:
    async def target() -> str:
        await asyncio.sleep(0.001)
        return "ok"

    stats = asyncio.run(
        profile_async_callable(
            target,
            iterations=3,
            warmup=1,
            collect_cpu=True,
            collect_memory=True,
        )
    )

    assert stats.iterations == 3
    assert stats.warmup_iterations == 1
    assert stats.average_ms > 0.0
    assert stats.average_cpu_ms is not None
    assert stats.peak_memory_kb is not None


def test_profile_async_callable_can_continue_after_failures() -> None:
    calls = 0

    async def target() -> str:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise RuntimeError("temporary failure")
        return "ok"

    stats = asyncio.run(
        profile_async_callable(target, iterations=3, continue_on_error=True)
    )

    assert stats.iterations == 2
    assert stats.failed_iterations == 1


def test_summarize_latencies_reports_expected_values() -> None:
    stats = summarize_latencies([1.0, 2.0, 3.0, 4.0], warmup_iterations=2)

    assert stats.average_ms == 2.5
    assert stats.min_ms == 1.0
    assert stats.max_ms == 4.0
    assert stats.p50_ms == 2.5
    assert stats.p95_ms == pytest.approx(3.85)
    assert stats.iterations == 4
    assert stats.warmup_iterations == 2
    assert stats.failed_iterations == 0


def test_summarize_profile_validates_resource_metrics() -> None:
    with pytest.raises(ValueError):
        summarize_profile([1.0, 2.0], cpu_times_ms=[1.0])

    with pytest.raises(ValueError):
        summarize_profile([1.0], peak_memory_kb=-1.0)

    with pytest.raises(ValueError):
        summarize_profile([1.0], failed_iterations=-1)


def test_percentile_validates_inputs() -> None:
    with pytest.raises(ValueError):
        percentile([], 50.0)

    with pytest.raises(ValueError):
        percentile([1.0], 101.0)


def test_report_formatters_include_key_metrics() -> None:
    stats = summarize_profile(
        [1.0, 2.0, 3.0],
        warmup_iterations=1,
        cpu_times_ms=[0.1, 0.2, 0.3],
        peak_memory_kb=42.5,
    )

    text_report = format_text_report(stats)
    markdown_report = format_markdown_report(stats)
    json_report = format_json_report(stats)
    html_report = format_html_report(stats)

    assert "Benchmark Results" in text_report
    assert "Iterations: 3" in text_report
    assert "Warmup: 1" in text_report
    assert "Failures: 0" in text_report
    assert "Peak Python Memory: 42.500 KB" in text_report
    assert "| Average | 2.000 ms |" in markdown_report
    metrics = json.loads(json_report)["metrics"]
    assert metrics["warmup_iterations"] == 1
    assert metrics["peak_memory_kb"] == 42.5
    assert "<!doctype html>" in html_report
    assert "<th>Warmup</th><td>1</td>" in html_report


def test_profile_http_endpoint_against_local_server() -> None:
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from threading import Thread

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")

        def log_message(self, format: str, *args: object) -> None:
            return None

    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        host, port = server.server_address
        stats = profile_http_endpoint(
            f"http://{host}:{port}",
            iterations=2,
            warmup=1,
            collect_cpu=True,
            collect_memory=True,
        )
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    assert stats.iterations == 2
    assert stats.warmup_iterations == 1
    assert stats.average_ms > 0.0
    assert stats.average_cpu_ms is not None
    assert stats.peak_memory_kb is not None


def test_compare_profiles_reports_metric_changes() -> None:
    baseline = summarize_profile(
        [10.0, 12.0, 14.0],
        cpu_times_ms=[5.0, 6.0, 7.0],
        peak_memory_kb=100.0,
    )
    candidate = summarize_profile(
        [8.0, 9.0, 10.0],
        cpu_times_ms=[4.0, 5.0, 6.0],
        peak_memory_kb=80.0,
    )

    comparison = compare_profiles(
        baseline,
        candidate,
        baseline_label="main",
        candidate_label="optimized",
    )

    average = next(metric for metric in comparison.metrics if metric.metric == "average_ms")

    assert comparison.baseline_label == "main"
    assert comparison.candidate_label == "optimized"
    assert average.baseline == 12.0
    assert average.candidate == 9.0
    assert average.delta == -3.0
    assert average.percent_change == pytest.approx(-25.0)
    assert average.improved is True
    assert average.result == "improved"


def test_comparison_report_formatters_include_key_metrics() -> None:
    comparison = compare_profiles(
        summarize_profile([10.0, 12.0, 14.0]),
        summarize_profile([11.0, 13.0, 15.0]),
        baseline_label="before",
        candidate_label="after",
    )

    text_report = format_comparison_text_report(comparison)
    markdown_report = format_comparison_markdown_report(comparison)
    json_report = format_comparison_json_report(comparison)
    html_report = format_comparison_html_report(comparison)

    assert "Benchmark Comparison" in text_report
    assert "average_ms" in text_report
    assert "| average_ms |" in markdown_report
    assert json.loads(json_report)["comparison"]["baseline_label"] == "before"
    assert "<!doctype html>" in html_report
    assert "<th>average_ms</th>" in html_report


def test_evaluate_thresholds_reports_regression_violations() -> None:
    comparison = compare_profiles(
        summarize_profile([10.0, 10.0, 10.0], failed_iterations=0),
        summarize_profile([12.0, 12.0, 12.0], failed_iterations=1),
    )

    evaluation = evaluate_thresholds(
        comparison,
        max_regression_percent=5.0,
        metrics={"average_ms", "failed_iterations"},
    )

    assert evaluation.passed is False
    assert {violation.metric for violation in evaluation.violations} == {
        "average_ms",
        "failed_iterations",
    }


def test_evaluate_thresholds_passes_allowed_regressions() -> None:
    comparison = compare_profiles(
        summarize_profile([100.0, 100.0, 100.0]),
        summarize_profile([103.0, 103.0, 103.0]),
    )

    evaluation = evaluate_thresholds(comparison, max_regression_percent=5.0)

    assert evaluation.passed is True
    assert evaluation.violations == ()


def test_evaluate_thresholds_rejects_negative_threshold() -> None:
    comparison = compare_profiles(
        summarize_profile([1.0]),
        summarize_profile([2.0]),
    )

    with pytest.raises(ValueError):
        evaluate_thresholds(comparison, max_regression_percent=-1.0)
