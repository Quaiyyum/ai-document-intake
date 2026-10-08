"""Exports the status table to dashboard/applications.csv for Power BI.

    python -m src.export_bi
"""
from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

from . import store
from .common import TS_FORMAT

OUT = Path("dashboard/applications.csv")


def minutes_between(start: str, end: str | None):
    if not end:
        return ""
    delta = datetime.strptime(end, TS_FORMAT) - datetime.strptime(start, TS_FORMAT)
    return int(delta.total_seconds() // 60)


def main() -> int:
    connection = store.connect()
    rows = [dict(row) for row in connection.execute("SELECT * FROM applications ORDER BY doc_id")]
    connection.close()
    for row in rows:
        row["received_date"] = row["received_at"][:10]
        row["turnaround_minutes"] = minutes_between(row["received_at"], row["processed_at"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    columns = ["doc_id", "source_file", "received_at", "status", "processed_at", "confidence_min",
               "schema_used", "received_date", "turnaround_minutes"]
    with open(OUT, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
