import json
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


def test_cli_returns_error_for_missing_target(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        run(["missing_target"])

    captured = capsys.readouterr()

    assert exc_info.value.code == 2
    assert "target must use the format module:function" in captured.err
