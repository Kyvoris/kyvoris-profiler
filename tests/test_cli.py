import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kyvoris_profiler.cli import load_callable, run


def test_load_callable_imports_target() -> None:
    callable_obj = load_callable("tests.fixtures.cli_targets:target")

    assert callable(callable_obj)
    assert callable_obj() == "ok"


def test_load_callable_imports_target_from_current_directory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    monkeypatch.chdir(repo_root)
    monkeypatch.setattr(
        sys,
        "path",
        [path for path in sys.path if Path(path or os.getcwd()).resolve() != repo_root],
    )

    callable_obj = load_callable("examples.run_demo:simulated_inference")

    assert callable(callable_obj)


def test_load_callable_rejects_invalid_target() -> None:
    with pytest.raises(ValueError):
        load_callable("tests.fixtures.cli_targets.target")


def test_cli_writes_text_report_to_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = run(
        [
            "tests.fixtures.cli_targets:target",
            "--iterations",
            "2",
            "--warmup",
            "1",
            "--title",
            "CLI Smoke Test",
        ]
    )

    output = capsys.readouterr().out

    assert exit_code == 0
    assert "CLI Smoke Test" in output
    assert "Iterations: 2" in output
    assert "Warmup: 1" in output


def test_cli_writes_json_report_to_file(tmp_path: Path) -> None:
    output_path = tmp_path / "report.json"

    exit_code = run(
        [
            "tests.fixtures.cli_targets:target",
            "--iterations",
            "2",
            "--format",
            "json",
            "--output",
            str(output_path),
            "--collect-cpu",
            "--collect-memory",
        ]
    )

    payload = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert payload["schema_version"] == "1.0"
    assert payload["metrics"]["iterations"] == 2
    assert payload["metrics"]["average_cpu_ms"] is not None
    assert payload["metrics"]["peak_memory_kb"] is not None


def test_cli_compare_reads_json_reports(tmp_path: Path) -> None:
    baseline_path = tmp_path / "baseline.json"
    candidate_path = tmp_path / "candidate.json"
    output_path = tmp_path / "comparison.md"

    assert run(
        [
            "tests.fixtures.cli_targets:target",
            "--iterations",
            "2",
            "--format",
            "json",
            "--output",
            str(baseline_path),
        ]
    ) == 0
    assert run(
        [
            "tests.fixtures.cli_targets:target",
            "--iterations",
            "2",
            "--format",
            "json",
            "--output",
            str(candidate_path),
        ]
    ) == 0

    exit_code = run(
        [
            "compare",
            str(baseline_path),
            str(candidate_path),
            "--baseline-label",
            "before",
            "--candidate-label",
            "after",
            "--format",
            "markdown",
            "--output",
            str(output_path),
        ]
    )

    output = output_path.read_text(encoding="utf-8")

    assert exit_code == 0
    assert "Benchmark Comparison" in output
    assert "Baseline: `before`" in output
    assert "| average_ms |" in output


def test_cli_runs_async_target(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = run(
        [
            "tests.fixtures.cli_targets:async_target",
            "--iterations",
            "2",
            "--warmup",
            "1",
        ]
    )

    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Iterations: 2" in output
    assert "Warmup: 1" in output


def test_cli_returns_error_for_missing_target(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        run(["missing_target"])

    captured = capsys.readouterr()

    assert exc_info.value.code == 2
    assert "target must use the format module:function" in captured.err
