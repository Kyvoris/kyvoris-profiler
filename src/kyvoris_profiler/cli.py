"""Command-line interface for Kyvoris Profiler."""

from __future__ import annotations

import argparse
import asyncio
import inspect
import importlib
import json
import os
import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from kyvoris_profiler import (
    __version__,
    compare_profiles,
    profile_async_callable,
    profile_callable,
)
from kyvoris_profiler.metrics import ProfileSummary
from kyvoris_profiler.report import (
    format_comparison_html_report,
    format_comparison_json_report,
    format_comparison_markdown_report,
    format_comparison_text_report,
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
}

COMPARISON_FORMATTERS = {
    "text": format_comparison_text_report,
    "markdown": format_comparison_markdown_report,
    "json": format_comparison_json_report,
    "html": format_comparison_html_report,
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
    parser.add_argument("baseline", type=Path, help="Baseline JSON report.")
    parser.add_argument("candidate", type=Path, help="Candidate JSON report.")
    parser.add_argument("--baseline-label", default="Baseline")
    parser.add_argument("--candidate-label", default="Candidate")
    parser.add_argument(
        "--format",
        choices=sorted(COMPARISON_FORMATTERS),
        default="text",
        help="Comparison report format. Default: text.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write comparison report to this path instead of stdout.",
    )
    parser.add_argument(
        "--title",
        default="Benchmark Comparison",
        help="Comparison report title. Default: Benchmark Comparison.",
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
        baseline = read_profile_summary(args.baseline)
        candidate = read_profile_summary(args.candidate)
        comparison = compare_profiles(
            baseline,
            candidate,
            baseline_label=args.baseline_label,
            candidate_label=args.candidate_label,
        )
    except Exception as exc:
        parser.exit(2, f"kyvoris-profiler: error: {exc}\n")

    formatter = COMPARISON_FORMATTERS[args.format]
    report = formatter(comparison, title=args.title)

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report + "\n", encoding="utf-8")
    else:
        print(report)

    return 0


def main() -> None:
    """Console script entry point."""
    raise SystemExit(run(sys.argv[1:]))


if __name__ == "__main__":
    main()
