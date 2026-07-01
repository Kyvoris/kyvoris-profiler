"""Benchmark history helpers."""

from __future__ import annotations

import json
import platform
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from kyvoris_profiler.metrics import ProfileSummary


@dataclass(frozen=True)
class HistoryRecord:
    """A saved benchmark summary in a history file."""

    timestamp: str
    label: str
    summary: ProfileSummary
    source: str | None = None
    metadata: dict[str, str] | None = None

    def as_dict(self) -> dict[str, object]:
        """Return the history record as a JSON-serializable dictionary."""
        return {
            "timestamp": self.timestamp,
            "label": self.label,
            "source": self.source,
            "summary": self.summary.as_dict(),
            "metadata": self.metadata or {},
        }


def read_summary_report(path: Path) -> ProfileSummary:
    """Read a profile summary from a JSON report."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    metrics = payload.get("metrics")
    if not isinstance(metrics, dict):
        raise ValueError(f"{path} does not contain a metrics object")
    return ProfileSummary(**metrics)


def append_history_record(
    history_path: Path,
    summary: ProfileSummary,
    label: str,
    source: str | None = None,
    timestamp: str | None = None,
    metadata: dict[str, str] | None = None,
) -> HistoryRecord:
    """Append a profile summary to a JSONL history file."""
    record = HistoryRecord(
        timestamp=timestamp or datetime.now(UTC).isoformat(),
        label=label,
        summary=summary,
        source=source,
        metadata=metadata,
    )
    history_path.parent.mkdir(parents=True, exist_ok=True)
    with history_path.open("a", encoding="utf-8") as history_file:
        history_file.write(json.dumps(record.as_dict(), sort_keys=True) + "\n")
    return record


def append_history_from_report(
    history_path: Path,
    report_path: Path,
    label: str,
    metadata: dict[str, str] | None = None,
) -> HistoryRecord:
    """Append a JSON benchmark report to a JSONL history file."""
    summary = read_summary_report(report_path)
    return append_history_record(
        history_path,
        summary,
        label=label,
        source=str(report_path),
        metadata=metadata,
    )


def read_history(history_path: Path) -> list[HistoryRecord]:
    """Read benchmark history records from a JSONL file."""
    records: list[HistoryRecord] = []
    if not history_path.exists():
        return records

    for line_number, line in enumerate(
        history_path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        if not line.strip():
            continue
        payload = json.loads(line)
        summary_payload = payload.get("summary")
        if not isinstance(summary_payload, dict):
            raise ValueError(f"{history_path}:{line_number} missing summary object")
        metadata_payload = payload.get("metadata", {})
        if not isinstance(metadata_payload, dict):
            raise ValueError(f"{history_path}:{line_number} metadata must be an object")
        records.append(
            HistoryRecord(
                timestamp=str(payload["timestamp"]),
                label=str(payload["label"]),
                source=(
                    str(payload["source"])
                    if payload.get("source") is not None
                    else None
                ),
                summary=ProfileSummary(**summary_payload),
                metadata={
                    str(key): str(value)
                    for key, value in metadata_payload.items()
                    if value is not None
                },
            )
        )
    return records


def latest_pair(history_path: Path) -> tuple[HistoryRecord, HistoryRecord]:
    """Return the previous and latest history records."""
    records = read_history(history_path)
    if len(records) < 2:
        raise ValueError("history must contain at least two records")
    return records[-2], records[-1]


def select_history_record(
    records: list[HistoryRecord],
    selector: str,
) -> HistoryRecord:
    """Select a history record by 1-based index or label."""
    if not records:
        raise ValueError("history contains no records")

    try:
        index = int(selector)
    except ValueError:
        matches = [record for record in records if record.label == selector]
        if not matches:
            raise ValueError(f"history label not found: {selector}")
        if len(matches) > 1:
            raise ValueError(
                f"history label is ambiguous: {selector}; use an index instead"
            )
        return matches[0]

    if index < 1 or index > len(records):
        raise ValueError(
            f"history index out of range: {index}; expected 1..{len(records)}"
        )
    return records[index - 1]


def select_history_pair(
    history_path: Path,
    baseline_selector: str,
    candidate_selector: str,
) -> tuple[HistoryRecord, HistoryRecord]:
    """Return selected baseline and candidate records from a history file."""
    records = read_history(history_path)
    return (
        select_history_record(records, baseline_selector),
        select_history_record(records, candidate_selector),
    )


def collect_environment_metadata(cwd: Path | None = None) -> dict[str, str]:
    """Collect stable environment metadata for a benchmark history record."""
    metadata = {
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
    }
    git_commit = _git_commit(cwd)
    if git_commit is not None:
        metadata["git_commit"] = git_commit
    return metadata


def _git_commit(cwd: Path | None) -> str | None:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    commit = completed.stdout.strip()
    return commit or None
