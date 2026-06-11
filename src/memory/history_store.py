"""Append-only JSONL history for recent research tasks.

This is a lightweight task history for demo observability. It is not a vector
database, semantic memory, or long-term personalization layer.
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from config import PROJECT_ROOT


HISTORY_PATH = PROJECT_ROOT / "src" / "outputs" / "history.jsonl"


def append_history(record: dict[str, Any]) -> None:
    """Append one history record, swallowing write errors to protect the flow."""
    try:
        HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
        safe_record = dict(record)
        safe_record.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
        with HISTORY_PATH.open("a", encoding="utf-8") as file:
            file.write(json.dumps(safe_record, ensure_ascii=False) + "\n")
    except OSError as exc:
        print(f"历史记录写入失败：{exc.__class__.__name__}")


def load_recent_history(limit: int = 10) -> list[dict[str, Any]]:
    """Load the most recent task history records, newest first."""
    if not HISTORY_PATH.exists():
        return []

    try:
        lines = HISTORY_PATH.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        print(f"历史记录读取失败：{exc.__class__.__name__}")
        return []

    records: list[dict[str, Any]] = []
    for line in reversed(lines[-max(1, limit) :]):
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records
