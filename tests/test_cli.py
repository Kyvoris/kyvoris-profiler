import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kyvoris_profiler.cli import (
    format_history_list,
    load_callable,
    load_history_preset_config,
    parse_metadata_args,
    run,
)


def test_hugging_face_demo_uses_three_default_models() -> None:
    from examples.run_model_demo import MODEL_NAMES

    assert len(MODEL_NAMES) == 3
    assert len(set(MODEL_NAMES)) == 3
    assert "cardiffnlp/twitter-roberta-base-sentiment-latest" in MODEL_NAMES


def test_parse_metadata_args_requires_key_value_pairs() -> None:
    assert parse_metadata_args(["model=distilbert", "version=0.10.0"]) == {
        "model": "distilbert",
        "version": "0.10.0",
    }

    with pytest.raises(ValueError):
        parse_metadata_args(["missing-separator"])


def test_load_history_preset_config_reads_named_preset(tmp_path: Path) -> None:
    config_path = tmp_path / "kyvoris-profiler.toml"
    config_path.write_text(
        "\n".join(
            [
                "[history_presets.main_vs_candidate]",
                'history = "reports/history.jsonl"',
                'baseline = "latest:baseline"',
                'candidate = "latest:candidate"',
                'metrics = ["average_ms"]',
            ]
        ),
        encoding="utf-8",
    )

    config = load_history_preset_config(config_path, "main_vs_candidate")

    assert config["baseline"] == "latest:baseline"
    assert config["metrics"] == ["average_ms"]


def write_json_report(path: Path, average_ms: float) -> None:
    path.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "metrics": {
                    "average_ms": average_ms,
                    "min_ms": average_ms,
                    "max_ms": average_ms,
                    "p50_ms": average_ms,
                    "p95_ms": average_ms,
                    "iterations": 1,
                    "warmup_iterations": 0,
                    "failed_iterations": 0,
                    "average_cpu_ms": None,
                    "min_cpu_ms": None,
                    "max_cpu_ms": None,
                    "peak_memory_kb": None,
                },
            }
        ),
        encoding="utf-8",
    )


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


def test_cli_writes_csv_report_to_file(tmp_path: Path) -> None:
    output_path = tmp_path / "report.csv"

    exit_code = run(
        [
            "tests.fixtures.cli_targets:target",
            "--iterations",
            "2",
            "--format",
            "csv",
            "--output",
            str(output_path),
        ]
    )

    output = output_path.read_text(encoding="utf-8")

    assert exit_code == 0
    assert "metric,value" in output
    assert "Iterations,2" in output


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


def test_cli_compare_writes_csv_report(tmp_path: Path) -> None:
    baseline_path = tmp_path / "baseline.json"
    candidate_path = tmp_path / "candidate.json"
    output_path = tmp_path / "comparison.csv"
    payload = {
        "schema_version": "1.0",
        "metrics": {
            "average_ms": 100.0,
            "min_ms": 100.0,
            "max_ms": 100.0,
            "p50_ms": 100.0,
            "p95_ms": 100.0,
            "iterations": 1,
            "warmup_iterations": 0,
            "failed_iterations": 0,
            "average_cpu_ms": None,
            "min_cpu_ms": None,
            "max_cpu_ms": None,
            "peak_memory_kb": None,
        },
    }
    baseline_path.write_text(json.dumps(payload), encoding="utf-8")
    candidate_path.write_text(json.dumps(payload), encoding="utf-8")

    exit_code = run(
        [
            "compare",
            str(baseline_path),
            str(candidate_path),
            "--format",
            "csv",
            "--output",
            str(output_path),
        ]
    )

    output = output_path.read_text(encoding="utf-8")

    assert exit_code == 0
    assert "metric,baseline,candidate,delta,percent_change,result" in output
    assert "average_ms" in output


def test_cli_compare_threshold_failure_returns_nonzero(tmp_path: Path) -> None:
    baseline_path = tmp_path / "baseline.json"
    candidate_path = tmp_path / "candidate.json"
    baseline_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "metrics": {
                    "average_ms": 10.0,
                    "min_ms": 10.0,
                    "max_ms": 10.0,
                    "p50_ms": 10.0,
                    "p95_ms": 10.0,
                    "iterations": 1,
                    "warmup_iterations": 0,
                    "failed_iterations": 0,
                    "average_cpu_ms": None,
                    "min_cpu_ms": None,
                    "max_cpu_ms": None,
                    "peak_memory_kb": None,
                },
            }
        ),
        encoding="utf-8",
    )
    candidate_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "metrics": {
                    "average_ms": 12.0,
                    "min_ms": 12.0,
                    "max_ms": 12.0,
                    "p50_ms": 12.0,
                    "p95_ms": 12.0,
                    "iterations": 1,
                    "warmup_iterations": 0,
                    "failed_iterations": 0,
                    "average_cpu_ms": None,
                    "min_cpu_ms": None,
                    "max_cpu_ms": None,
                    "peak_memory_kb": None,
                },
            }
        ),
        encoding="utf-8",
    )

    exit_code = run(
        [
            "compare",
            str(baseline_path),
            str(candidate_path),
            "--max-regression-percent",
            "5",
            "--threshold-metric",
            "average_ms",
            "--fail-on-regression",
        ]
    )

    assert exit_code == 1


def test_cli_compare_threshold_pass_returns_zero(tmp_path: Path) -> None:
    baseline_path = tmp_path / "baseline.json"
    candidate_path = tmp_path / "candidate.json"
    baseline_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "metrics": {
                    "average_ms": 100.0,
                    "min_ms": 100.0,
                    "max_ms": 100.0,
                    "p50_ms": 100.0,
                    "p95_ms": 100.0,
                    "iterations": 1,
                    "warmup_iterations": 0,
                    "failed_iterations": 0,
                    "average_cpu_ms": None,
                    "min_cpu_ms": None,
                    "max_cpu_ms": None,
                    "peak_memory_kb": None,
                },
            }
        ),
        encoding="utf-8",
    )
    candidate_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "metrics": {
                    "average_ms": 103.0,
                    "min_ms": 103.0,
                    "max_ms": 103.0,
                    "p50_ms": 103.0,
                    "p95_ms": 103.0,
                    "iterations": 1,
                    "warmup_iterations": 0,
                    "failed_iterations": 0,
                    "average_cpu_ms": None,
                    "min_cpu_ms": None,
                    "max_cpu_ms": None,
                    "peak_memory_kb": None,
                },
            }
        ),
        encoding="utf-8",
    )

    exit_code = run(
        [
            "compare",
            str(baseline_path),
            str(candidate_path),
            "--max-regression-percent",
            "5",
            "--threshold-metric",
            "average_ms",
            "--fail-on-regression",
        ]
    )

    assert exit_code == 0


def test_cli_compare_reads_toml_config(tmp_path: Path) -> None:
    baseline_path = tmp_path / "baseline.json"
    candidate_path = tmp_path / "candidate.json"
    output_path = tmp_path / "comparison.md"
    config_path = tmp_path / "kyvoris-profiler.toml"

    baseline_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "metrics": {
                    "average_ms": 100.0,
                    "min_ms": 100.0,
                    "max_ms": 100.0,
                    "p50_ms": 100.0,
                    "p95_ms": 100.0,
                    "iterations": 1,
                    "warmup_iterations": 0,
                    "failed_iterations": 0,
                    "average_cpu_ms": None,
                    "min_cpu_ms": None,
                    "max_cpu_ms": None,
                    "peak_memory_kb": None,
                },
            }
        ),
        encoding="utf-8",
    )
    candidate_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "metrics": {
                    "average_ms": 103.0,
                    "min_ms": 103.0,
                    "max_ms": 103.0,
                    "p50_ms": 103.0,
                    "p95_ms": 103.0,
                    "iterations": 1,
                    "warmup_iterations": 0,
                    "failed_iterations": 0,
                    "average_cpu_ms": None,
                    "min_cpu_ms": None,
                    "max_cpu_ms": None,
                    "peak_memory_kb": None,
                },
            }
        ),
        encoding="utf-8",
    )
    config_path.write_text(
        "\n".join(
            [
                "[compare]",
                f'baseline = "{baseline_path.as_posix()}"',
                f'candidate = "{candidate_path.as_posix()}"',
                'baseline_label = "before"',
                'candidate_label = "after"',
                'format = "markdown"',
                f'output = "{output_path.as_posix()}"',
                "",
                "[thresholds]",
                "max_regression_percent = 5",
                'metrics = ["average_ms"]',
                "fail_on_regression = true",
            ]
        ),
        encoding="utf-8",
    )

    exit_code = run(["compare", "--config", str(config_path)])

    output = output_path.read_text(encoding="utf-8")

    assert exit_code == 0
    assert "Baseline: `before`" in output
    assert "| average_ms |" in output


def test_cli_compare_command_line_overrides_toml_config(tmp_path: Path) -> None:
    baseline_path = tmp_path / "baseline.json"
    candidate_path = tmp_path / "candidate.json"
    configured_output_path = tmp_path / "configured.md"
    override_output_path = tmp_path / "override.json"
    config_path = tmp_path / "kyvoris-profiler.toml"
    payload = {
        "schema_version": "1.0",
        "metrics": {
            "average_ms": 100.0,
            "min_ms": 100.0,
            "max_ms": 100.0,
            "p50_ms": 100.0,
            "p95_ms": 100.0,
            "iterations": 1,
            "warmup_iterations": 0,
            "failed_iterations": 0,
            "average_cpu_ms": None,
            "min_cpu_ms": None,
            "max_cpu_ms": None,
            "peak_memory_kb": None,
        },
    }
    baseline_path.write_text(json.dumps(payload), encoding="utf-8")
    candidate_path.write_text(json.dumps(payload), encoding="utf-8")
    config_path.write_text(
        "\n".join(
            [
                "[compare]",
                f'baseline = "{baseline_path.as_posix()}"',
                f'candidate = "{candidate_path.as_posix()}"',
                'format = "markdown"',
                f'output = "{configured_output_path.as_posix()}"',
            ]
        ),
        encoding="utf-8",
    )

    exit_code = run(
        [
            "compare",
            "--config",
            str(config_path),
            "--format",
            "json",
            "--output",
            str(override_output_path),
        ]
    )

    assert exit_code == 0
    assert not configured_output_path.exists()
    assert json.loads(override_output_path.read_text(encoding="utf-8"))[
        "schema_version"
    ] == "1.0"


def test_cli_history_appends_and_compares_latest_records(tmp_path: Path) -> None:
    baseline_path = tmp_path / "baseline.json"
    candidate_path = tmp_path / "candidate.json"
    history_path = tmp_path / "history.jsonl"
    output_path = tmp_path / "history-comparison.md"
    write_json_report(baseline_path, 10.0)
    write_json_report(candidate_path, 9.0)

    assert (
        run(
            [
                "history",
                "append",
                str(baseline_path),
                "--history",
                str(history_path),
                "--label",
                "before",
                "--metadata",
                "model=old-model",
                "--no-environment-metadata",
            ]
        )
        == 0
    )
    assert (
        run(
            [
                "history",
                "append",
                str(candidate_path),
                "--history",
                str(history_path),
                "--label",
                "after",
                "--metadata",
                "model=new-model",
                "--no-environment-metadata",
            ]
        )
        == 0
    )

    exit_code = run(
        [
            "history",
            "compare-latest",
            "--history",
            str(history_path),
            "--format",
            "markdown",
            "--output",
            str(output_path),
        ]
    )

    output = output_path.read_text(encoding="utf-8")

    assert exit_code == 0
    assert "Benchmark History Comparison" in output
    assert "Baseline: `before`" in output
    assert "Candidate: `after`" in output
    assert "| average_ms |" in output


def test_cli_history_lists_saved_records(tmp_path: Path) -> None:
    report_path = tmp_path / "report.json"
    history_path = tmp_path / "history.jsonl"
    write_json_report(report_path, 10.0)
    assert (
        run(
            [
                "history",
                "append",
                str(report_path),
                "--history",
                str(history_path),
                "--label",
                "main",
                "--metadata",
                "model=demo",
                "--no-environment-metadata",
            ]
        )
        == 0
    )

    exit_code = run(["history", "list", "--history", str(history_path)])

    assert exit_code == 0


def test_cli_history_list_filters_records(tmp_path: Path) -> None:
    first_path = tmp_path / "first.json"
    second_path = tmp_path / "second.json"
    third_path = tmp_path / "third.json"
    history_path = tmp_path / "history.jsonl"
    write_json_report(first_path, 10.0)
    write_json_report(second_path, 11.0)
    write_json_report(third_path, 12.0)

    for report_path, label, model in [
        (first_path, "main", "a"),
        (second_path, "main", "b"),
        (third_path, "branch", "b"),
    ]:
        assert (
            run(
                [
                    "history",
                    "append",
                    str(report_path),
                    "--history",
                    str(history_path),
                    "--label",
                    label,
                    "--metadata",
                    f"model={model}",
                    "--no-environment-metadata",
                ]
            )
            == 0
        )

    exit_code = run(
        [
            "history",
            "list",
            "--history",
            str(history_path),
            "--metadata",
            "model=b",
            "--limit",
            "1",
        ]
    )

    assert exit_code == 0


def test_cli_history_compares_selected_records_by_index(tmp_path: Path) -> None:
    first_path = tmp_path / "first.json"
    second_path = tmp_path / "second.json"
    third_path = tmp_path / "third.json"
    history_path = tmp_path / "history.jsonl"
    output_path = tmp_path / "selected-comparison.md"
    write_json_report(first_path, 10.0)
    write_json_report(second_path, 11.0)
    write_json_report(third_path, 8.0)

    for report_path, label in [
        (first_path, "first"),
        (second_path, "second"),
        (third_path, "third"),
    ]:
        assert (
            run(
                [
                    "history",
                    "append",
                    str(report_path),
                    "--history",
                    str(history_path),
                    "--label",
                    label,
                    "--no-environment-metadata",
                ]
            )
            == 0
        )

    exit_code = run(
        [
            "history",
            "compare",
            "--history",
            str(history_path),
            "--baseline",
            "1",
            "--candidate",
            "3",
            "--format",
            "markdown",
            "--output",
            str(output_path),
        ]
    )

    output = output_path.read_text(encoding="utf-8")

    assert exit_code == 0
    assert "Baseline: `first`" in output
    assert "Candidate: `third`" in output


def test_cli_history_compares_selected_records_by_label(tmp_path: Path) -> None:
    baseline_path = tmp_path / "baseline.json"
    candidate_path = tmp_path / "candidate.json"
    history_path = tmp_path / "history.jsonl"
    write_json_report(baseline_path, 10.0)
    write_json_report(candidate_path, 12.0)

    assert (
        run(
            [
                "history",
                "append",
                str(baseline_path),
                "--history",
                str(history_path),
                "--label",
                "baseline",
                "--no-environment-metadata",
            ]
        )
        == 0
    )
    assert (
        run(
            [
                "history",
                "append",
                str(candidate_path),
                "--history",
                str(history_path),
                "--label",
                "candidate",
                "--no-environment-metadata",
            ]
        )
        == 0
    )

    exit_code = run(
        [
            "history",
            "compare",
            "--history",
            str(history_path),
            "--baseline",
            "baseline",
            "--candidate",
            "candidate",
            "--max-regression-percent",
            "5",
            "--threshold-metric",
            "average_ms",
            "--fail-on-regression",
        ]
    )

    assert exit_code == 1


def test_cli_history_compares_latest_label_selectors(tmp_path: Path) -> None:
    first_path = tmp_path / "first.json"
    second_path = tmp_path / "second.json"
    third_path = tmp_path / "third.json"
    history_path = tmp_path / "history.jsonl"
    output_path = tmp_path / "latest-label-comparison.md"
    write_json_report(first_path, 10.0)
    write_json_report(second_path, 11.0)
    write_json_report(third_path, 8.0)

    for report_path, label in [
        (first_path, "main"),
        (second_path, "branch"),
        (third_path, "main"),
    ]:
        assert (
            run(
                [
                    "history",
                    "append",
                    str(report_path),
                    "--history",
                    str(history_path),
                    "--label",
                    label,
                    "--no-environment-metadata",
                ]
            )
            == 0
        )

    exit_code = run(
        [
            "history",
            "compare",
            "--history",
            str(history_path),
            "--baseline",
            "latest:branch",
            "--candidate",
            "latest:main",
            "--format",
            "markdown",
            "--output",
            str(output_path),
        ]
    )

    output = output_path.read_text(encoding="utf-8")

    assert exit_code == 0
    assert "Baseline: `branch`" in output
    assert "Candidate: `main`" in output


def test_cli_history_compare_reads_preset(tmp_path: Path) -> None:
    baseline_path = tmp_path / "baseline.json"
    candidate_path = tmp_path / "candidate.json"
    history_path = tmp_path / "history.jsonl"
    output_path = tmp_path / "preset-comparison.md"
    config_path = tmp_path / "kyvoris-profiler.toml"
    write_json_report(baseline_path, 10.0)
    write_json_report(candidate_path, 9.0)

    for report_path, label in [
        (baseline_path, "baseline"),
        (candidate_path, "candidate"),
    ]:
        assert (
            run(
                [
                    "history",
                    "append",
                    str(report_path),
                    "--history",
                    str(history_path),
                    "--label",
                    label,
                    "--no-environment-metadata",
                ]
            )
            == 0
        )

    config_path.write_text(
        "\n".join(
            [
                "[history_presets.main_vs_candidate]",
                f'history = "{history_path.as_posix()}"',
                'baseline = "latest:baseline"',
                'candidate = "latest:candidate"',
                'format = "markdown"',
                f'output = "{output_path.as_posix()}"',
                'max_regression_percent = 5',
                'metrics = ["average_ms"]',
                "fail_on_regression = true",
            ]
        ),
        encoding="utf-8",
    )

    exit_code = run(
        [
            "history",
            "compare",
            "--config",
            str(config_path),
            "--preset",
            "main_vs_candidate",
        ]
    )

    output = output_path.read_text(encoding="utf-8")

    assert exit_code == 0
    assert "Baseline: `baseline`" in output
    assert "Candidate: `candidate`" in output


def test_cli_history_compare_flags_override_preset(tmp_path: Path) -> None:
    baseline_path = tmp_path / "baseline.json"
    candidate_path = tmp_path / "candidate.json"
    history_path = tmp_path / "history.jsonl"
    configured_output_path = tmp_path / "configured.md"
    override_output_path = tmp_path / "override.json"
    config_path = tmp_path / "kyvoris-profiler.toml"
    write_json_report(baseline_path, 10.0)
    write_json_report(candidate_path, 9.0)

    for report_path, label in [
        (baseline_path, "baseline"),
        (candidate_path, "candidate"),
    ]:
        assert (
            run(
                [
                    "history",
                    "append",
                    str(report_path),
                    "--history",
                    str(history_path),
                    "--label",
                    label,
                    "--no-environment-metadata",
                ]
            )
            == 0
        )

    config_path.write_text(
        "\n".join(
            [
                "[history_presets.main_vs_candidate]",
                f'history = "{history_path.as_posix()}"',
                'baseline = "latest:baseline"',
                'candidate = "latest:candidate"',
                'format = "markdown"',
                f'output = "{configured_output_path.as_posix()}"',
            ]
        ),
        encoding="utf-8",
    )

    exit_code = run(
        [
            "history",
            "compare",
            "--config",
            str(config_path),
            "--preset",
            "main_vs_candidate",
            "--format",
            "json",
            "--output",
            str(override_output_path),
        ]
    )

    assert exit_code == 0
    assert not configured_output_path.exists()
    assert json.loads(override_output_path.read_text(encoding="utf-8"))[
        "schema_version"
    ] == "1.0"


def test_format_history_list_includes_key_metadata(tmp_path: Path) -> None:
    from kyvoris_profiler import append_history_record, read_history, summarize_profile

    history_path = tmp_path / "history.jsonl"
    append_history_record(
        history_path,
        summarize_profile([10.0]),
        label="main",
        metadata={"model": "demo", "ignored": "value"},
    )

    output = format_history_list(read_history(history_path))

    assert "Index | Timestamp | Label | Average | P95 | Metadata" in output
    assert "main" in output
    assert "model=demo" in output
    assert "ignored=value" not in output


def test_cli_history_threshold_failure_returns_nonzero(tmp_path: Path) -> None:
    baseline_path = tmp_path / "baseline.json"
    candidate_path = tmp_path / "candidate.json"
    history_path = tmp_path / "history.jsonl"
    write_json_report(baseline_path, 10.0)
    write_json_report(candidate_path, 12.0)

    assert (
        run(
            [
                "history",
                "append",
                str(baseline_path),
                "--history",
                str(history_path),
                "--label",
                "baseline",
            ]
        )
        == 0
    )
    assert (
        run(
            [
                "history",
                "append",
                str(candidate_path),
                "--history",
                str(history_path),
                "--label",
                "candidate",
            ]
        )
        == 0
    )

    exit_code = run(
        [
            "history",
            "compare-latest",
            "--history",
            str(history_path),
            "--max-regression-percent",
            "5",
            "--threshold-metric",
            "average_ms",
            "--fail-on-regression",
        ]
    )

    assert exit_code == 1


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
