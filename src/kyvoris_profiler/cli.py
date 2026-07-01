"""Command-line interface for Kyvoris Profiler."""

from __future__ import annotations

import argparse
import asyncio
import inspect
import importlib
import json
import os
import sys
import tomllib
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from kyvoris_profiler import (
    ThresholdEvaluation,
    __version__,
    append_history_from_report,
    compare_profiles,
    evaluate_thresholds,
    latest_pair,
    profile_async_callable,
    profile_callable,
)
from kyvoris_profiler.metrics import ProfileSummary
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

REPORT_FORMATTERS = {
    "text": format_text_report,
    "markdown": format_markdown_report,
    "json": format_json_report,
    "html": format_html_report,
    "csv": format_csv_report,
}

COMPARISON_FORMATTERS = {
    "text": format_comparison_text_report,
    "markdown": format_comparison_markdown_report,
    "json": format_comparison_json_report,
    "html": format_comparison_html_report,
    "csv": format_comparison_csv_report,
}


def load_callable(target: str) -> Callable[[], Any]:
    """Load a no-argument callable from a module path like package.module:function."""
    module_name, separator, function_name = target.partition(":")
    if not separator or not module_name or not function_name:
        raise ValueError("target must use the format module:function")

    cwd = os.getcwd()
    if cwd not in sys.path:
        sys.path.insert(0, cwd)

    module = importlib.import_module(module_name)
    callable_obj = getattr(module, function_name)
    if not callable(callable_obj):
        raise TypeError(f"{target} is not callable")
    return callable_obj


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="kyvoris-profiler",
        description="Benchmark a no-argument Python callable.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    add_run_arguments(parser)
    return parser


def build_compare_parser() -> argparse.ArgumentParser:
    """Build the comparison CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="kyvoris-profiler compare",
        description="Compare two JSON benchmark reports.",
    )
    parser.add_argument("baseline", nargs="?", type=Path, help="Baseline JSON report.")
    parser.add_argument("candidate", nargs="?", type=Path, help="Candidate JSON report.")
    parser.add_argument("--config", type=Path, help="TOML comparison config file.")
    parser.add_argument("--baseline-label")
    parser.add_argument("--candidate-label")
    parser.add_argument(
        "--format",
        choices=sorted(COMPARISON_FORMATTERS),
        help="Comparison report format. Default: text.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write comparison report to this path instead of stdout.",
    )
    parser.add_argument(
        "--title",
        help="Comparison report title. Default: Benchmark Comparison.",
    )
    parser.add_argument(
        "--max-regression-percent",
        type=float,
        help="Allowed regression percentage before threshold violation.",
    )
    parser.add_argument(
        "--threshold-metric",
        action="append",
        dest="threshold_metrics",
        help="Metric to evaluate against the threshold. Can be passed multiple times.",
    )
    parser.add_argument(
        "--fail-on-regression",
        action="store_true",
        help="Exit with code 1 when threshold violations are found.",
    )
    return parser


def build_history_parser() -> argparse.ArgumentParser:
    """Build the benchmark history CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="kyvoris-profiler history",
        description="Save and compare benchmark history records.",
    )
    subparsers = parser.add_subparsers(dest="history_command", required=True)

    append_parser = subparsers.add_parser(
        "append",
        help="Append a JSON benchmark report to a JSONL history file.",
    )
    append_parser.add_argument("report", type=Path, help="JSON benchmark report.")
    append_parser.add_argument(
        "--history",
        type=Path,
        default=Path("reports/history.jsonl"),
        help="History JSONL path. Default: reports/history.jsonl.",
    )
    append_parser.add_argument(
        "--label",
        required=True,
        help="Label for the saved history record.",
    )

    compare_parser = subparsers.add_parser(
        "compare-latest",
        help="Compare the latest two records in a history file.",
    )
    compare_parser.add_argument(
        "--history",
        type=Path,
        default=Path("reports/history.jsonl"),
        help="History JSONL path. Default: reports/history.jsonl.",
    )
    compare_parser.add_argument(
        "--format",
        choices=sorted(COMPARISON_FORMATTERS),
        default="text",
        help="Comparison report format. Default: text.",
    )
    compare_parser.add_argument(
        "--output",
        type=Path,
        help="Write comparison report to this path instead of stdout.",
    )
    compare_parser.add_argument(
        "--title",
        default="Benchmark History Comparison",
        help="Comparison report title. Default: Benchmark History Comparison.",
    )
    compare_parser.add_argument(
        "--max-regression-percent",
        type=float,
        help="Allowed regression percentage before threshold violation.",
    )
    compare_parser.add_argument(
        "--threshold-metric",
        action="append",
        dest="threshold_metrics",
        help="Metric to evaluate against the threshold. Can be passed multiple times.",
    )
    compare_parser.add_argument(
        "--fail-on-regression",
        action="store_true",
        help="Exit with code 1 when threshold violations are found.",
    )
    return parser


def add_run_arguments(parser: argparse.ArgumentParser) -> None:
    """Add benchmark execution arguments to a parser."""
    parser.add_argument(
        "target",
        help="Callable target in module:function format.",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=10,
        help="Number of measured iterations. Default: 10.",
    )
    parser.add_argument(
        "--warmup",
        type=int,
        default=0,
        help="Number of untimed warmup calls. Default: 0.",
    )
    parser.add_argument(
        "--format",
        choices=sorted(REPORT_FORMATTERS),
        default="text",
        help="Report format. Default: text.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write report to this path instead of stdout.",
    )
    parser.add_argument(
        "--title",
        default="Benchmark Results",
        help="Report title. Default: Benchmark Results.",
    )
    parser.add_argument(
        "--collect-cpu",
        action="store_true",
        help="Collect process CPU time metrics.",
    )
    parser.add_argument(
        "--collect-memory",
        action="store_true",
        help="Collect peak Python-traced memory metrics.",
    )


def run(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""
    if argv and argv[0] == "compare":
        parser = build_compare_parser()
        args = parser.parse_args(argv[1:])
        return run_compare(args, parser)
    if argv and argv[0] == "history":
        parser = build_history_parser()
        args = parser.parse_args(argv[1:])
        return run_history(args, parser)

    parser = build_parser()
    args = parser.parse_args(argv)
    return run_benchmark(args, parser)


def run_benchmark(args: argparse.Namespace, parser: argparse.ArgumentParser) -> int:
    """Run a benchmark command."""
    try:
        callable_obj = load_callable(args.target)
        profile_kwargs = {
            "iterations": args.iterations,
            "warmup": args.warmup,
            "collect_cpu": args.collect_cpu,
            "collect_memory": args.collect_memory,
        }
        if inspect.iscoroutinefunction(callable_obj):
            summary = asyncio.run(profile_async_callable(callable_obj, **profile_kwargs))
        else:
            summary = profile_callable(callable_obj, **profile_kwargs)
    except Exception as exc:
        parser.exit(2, f"kyvoris-profiler: error: {exc}\n")

    formatter = REPORT_FORMATTERS[args.format]
    report = formatter(summary, title=args.title)

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report + "\n", encoding="utf-8")
    else:
        print(report)

    return 0


def read_profile_summary(path: Path) -> ProfileSummary:
    """Read a profile summary from a JSON report."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    metrics = payload.get("metrics")
    if not isinstance(metrics, dict):
        raise ValueError(f"{path} does not contain a metrics object")
    return ProfileSummary(**metrics)


def run_compare(args: argparse.Namespace, parser: argparse.ArgumentParser) -> int:
    """Run a comparison command."""
    try:
        compare_config = load_compare_config(args.config) if args.config else {}
        thresholds_config = load_thresholds_config(args.config) if args.config else {}

        baseline_path = args.baseline or _optional_path(compare_config.get("baseline"))
        candidate_path = args.candidate or _optional_path(compare_config.get("candidate"))
        if baseline_path is None or candidate_path is None:
            raise ValueError("baseline and candidate reports are required")

        baseline_label = args.baseline_label or str(
            compare_config.get("baseline_label", "Baseline")
        )
        candidate_label = args.candidate_label or str(
            compare_config.get("candidate_label", "Candidate")
        )
        output_format = args.format or str(compare_config.get("format", "text"))
        if output_format not in COMPARISON_FORMATTERS:
            raise ValueError(
                "format must be one of "
                + ", ".join(sorted(COMPARISON_FORMATTERS))
            )
        output_path = args.output or _optional_path(compare_config.get("output"))
        title = args.title or str(compare_config.get("title", "Benchmark Comparison"))
        max_regression_percent = (
            args.max_regression_percent
            if args.max_regression_percent is not None
            else thresholds_config.get("max_regression_percent")
        )
        threshold_metrics = (
            args.threshold_metrics
            if args.threshold_metrics is not None
            else thresholds_config.get("metrics")
        )
        fail_on_regression = (
            args.fail_on_regression
            if args.fail_on_regression
            else bool(thresholds_config.get("fail_on_regression", False))
        )

        baseline = read_profile_summary(baseline_path)
        candidate = read_profile_summary(candidate_path)
        comparison = compare_profiles(
            baseline,
            candidate,
            baseline_label=baseline_label,
            candidate_label=candidate_label,
        )
        threshold_evaluation = None
        if max_regression_percent is not None:
            threshold_evaluation = evaluate_thresholds(
                comparison,
                max_regression_percent=float(max_regression_percent),
                metrics=set(threshold_metrics) if threshold_metrics else None,
            )
    except Exception as exc:
        parser.exit(2, f"kyvoris-profiler: error: {exc}\n")

    formatter = COMPARISON_FORMATTERS[output_format]
    report = formatter(comparison, title=title)

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report + "\n", encoding="utf-8")
    else:
        print(report)

    if threshold_evaluation is not None:
        threshold_exit_code = print_threshold_evaluation(
            threshold_evaluation,
            fail_on_regression=fail_on_regression,
        )
        if threshold_exit_code != 0:
            return threshold_exit_code

    return 0


def run_history(args: argparse.Namespace, parser: argparse.ArgumentParser) -> int:
    """Run a benchmark history command."""
    try:
        if args.history_command == "append":
            record = append_history_from_report(
                args.history,
                args.report,
                label=args.label,
            )
            print(
                f"Appended history record: {record.label} "
                f"({record.timestamp}) -> {args.history}"
            )
            return 0

        if args.history_command == "compare-latest":
            baseline_record, candidate_record = latest_pair(args.history)
            comparison = compare_profiles(
                baseline_record.summary,
                candidate_record.summary,
                baseline_label=baseline_record.label,
                candidate_label=candidate_record.label,
            )
            threshold_evaluation = None
            if args.max_regression_percent is not None:
                threshold_evaluation = evaluate_thresholds(
                    comparison,
                    max_regression_percent=args.max_regression_percent,
                    metrics=set(args.threshold_metrics) if args.threshold_metrics else None,
                )
        else:
            raise ValueError(f"unsupported history command: {args.history_command}")
    except Exception as exc:
        parser.exit(2, f"kyvoris-profiler: error: {exc}\n")

    formatter = COMPARISON_FORMATTERS[args.format]
    report = formatter(comparison, title=args.title)

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report + "\n", encoding="utf-8")
    else:
        print(report)

    if threshold_evaluation is not None:
        threshold_exit_code = print_threshold_evaluation(
            threshold_evaluation,
            fail_on_regression=args.fail_on_regression,
        )
        if threshold_exit_code != 0:
            return threshold_exit_code

    return 0


def print_threshold_evaluation(
    threshold_evaluation: ThresholdEvaluation,
    *,
    fail_on_regression: bool,
) -> int:
    """Print threshold evaluation details and return the appropriate exit code."""
    if threshold_evaluation.passed:
        print("Threshold check: passed", file=sys.stderr)
        return 0

    print("Threshold check: failed", file=sys.stderr)
    for violation in threshold_evaluation.violations:
        change = (
            "n/a"
            if violation.percent_change is None
            else f"{violation.percent_change:+.2f}%"
        )
        print(
            f"- {violation.metric}: {change} "
            f"(allowed {violation.allowed_regression_percent:.2f}%)",
            file=sys.stderr,
        )
    if fail_on_regression:
        return 1
    return 0


def _optional_path(value: object) -> Path | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("path values in config must be strings")
    return Path(value)


def load_toml_config(path: Path) -> dict[str, object]:
    """Load a TOML config file."""
    return tomllib.loads(path.read_text(encoding="utf-8"))


def load_compare_config(path: Path) -> dict[str, object]:
    """Load compare settings from a TOML config file."""
    config = load_toml_config(path)
    compare_config = config.get("compare", {})
    if not isinstance(compare_config, dict):
        raise ValueError("[compare] config must be a table")
    return compare_config


def load_thresholds_config(path: Path) -> dict[str, object]:
    """Load threshold settings from a TOML config file."""
    config = load_toml_config(path)
    thresholds_config = config.get("thresholds", {})
    if not isinstance(thresholds_config, dict):
        raise ValueError("[thresholds] config must be a table")
    metrics = thresholds_config.get("metrics")
    if metrics is not None and not (
        isinstance(metrics, list)
        and all(isinstance(metric, str) for metric in metrics)
    ):
        raise ValueError("thresholds.metrics must be a list of strings")
    return thresholds_config


def main() -> None:
    """Console script entry point."""
    raise SystemExit(run(sys.argv[1:]))


if __name__ == "__main__":
    main()
