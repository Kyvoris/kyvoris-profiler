"""Benchmark history helpers."""

from __future__ import annotations

import json
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

    def as_dict(self) -> dict[str, object]:
        """Return the history record as a JSON-serializable dictionary."""
        return {
            "timestamp": self.timestamp,
            "label": self.label,
            "source": self.source,
            "summary": self.summary.as_dict(),
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
) -> HistoryRecord:
    """Append a profile summary to a JSONL history file."""
    record = HistoryRecord(
        timestamp=timestamp or datetime.now(UTC).isoformat(),
        label=label,
        summary=summary,
        source=source,
    )
    history_path.parent.mkdir(parents=True, exist_ok=True)
    with history_path.open("a", encoding="utf-8") as history_file:
        history_file.write(json.dumps(record.as_dict(), sort_keys=True) + "\n")
    return record


def append_history_from_report(
    history_path: Path,
    report_path: Path,
    label: str,
) -> HistoryRecord:
    """Append a JSON benchmark report to a JSONL history file."""
    summary = read_summary_report(report_path)
    return append_history_record(
        history_path,
        summary,
        label=label,
        source=str(report_path),
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
            )
        )
    return records


def latest_pair(history_path: Path) -> tuple[HistoryRecord, HistoryRecord]:
    """Return the previous and latest history records."""
    records = read_history(history_path)
    if len(records) < 2:
        raise ValueError("history must contain at least two records")
    return records[-2], records[-1]
