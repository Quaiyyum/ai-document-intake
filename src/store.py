"""SQLite status store: one row per document, with status and real timestamps.

    python -m src.store init
    python -m src.store sync
"""
from __future__ import annotations

import glob
import sqlite3
import sys
from pathlib import Path

from .common import DB_PATH, load_records
from .manifest import load_manifest
from .schema import load_schema

DDL = """
CREATE TABLE IF NOT EXISTS applications (
  doc_id         TEXT PRIMARY KEY,
  source_file    TEXT NOT NULL,
  received_at    TEXT NOT NULL,
  status         TEXT NOT NULL CHECK (status IN ('extracted','needs_review','processed')),
  processed_at   TEXT,
  confidence_min REAL,
  schema_used    TEXT NOT NULL
);
"""


def connect(path: Path = DB_PATH) -> sqlite3.Connection:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(path))
    connection.row_factory = sqlite3.Row
    connection.execute(DDL)
    return connection


def thresholds(config_dir: str = "config") -> dict[str, float]:
    found = {}
    for name in glob.glob(f"{config_dir}/schema_*.yaml"):
        schema = load_schema(name)
        found[schema.schema_name] = schema.review_threshold
    return found


def sync(path: Path = DB_PATH) -> int:
    received = {row["doc_id"]: row["received_at"] for row in load_manifest()}
    limits = thresholds()
    connection = connect(path)
    count = 0
    with connection:
        for doc_id, record in load_records().items():
            existing = connection.execute("SELECT status FROM applications WHERE doc_id = ?", (doc_id,)).fetchone()
            if existing and existing["status"] == "processed":
                continue  # a reviewed document is never downgraded
            limit = limits.get(record["schema_used"], 0.7)
            clean = record["confidence_min"] >= limit
            status = "extracted" if clean else "needs_review"
            processed_at = record["extracted_at"] if clean else None
            connection.execute(
                """INSERT INTO applications VALUES (?,?,?,?,?,?,?)
                   ON CONFLICT(doc_id) DO UPDATE SET source_file=excluded.source_file,
                     status=excluded.status, processed_at=excluded.processed_at,
                     confidence_min=excluded.confidence_min, schema_used=excluded.schema_used""",
                (doc_id, Path(record["source_file"]).name, received.get(doc_id, record["extracted_at"]),
                 status, processed_at, record["confidence_min"], record["schema_used"]),
            )
            count += 1
    connection.close()
    return count


def mark_processed(doc_id: str, when: str, path: Path = DB_PATH) -> None:
    connection = connect(path)
    with connection:
        connection.execute(
            "UPDATE applications SET status='processed', processed_at=? WHERE doc_id=? AND status='needs_review'",
            (when, doc_id),
        )
    connection.close()


def status_counts(path: Path = DB_PATH) -> dict[str, int]:
    connection = connect(path)
    rows = connection.execute("SELECT status, COUNT(*) AS n FROM applications GROUP BY status").fetchall()
    connection.close()
    return {row["status"]: row["n"] for row in rows}


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "init":
        connect().close()
        print(f"ready: {DB_PATH}")
    elif command == "sync":
        print(f"synced {sync()} documents; statuses: {status_counts()}")
    else:
        sys.exit("usage: python -m src.store init|sync")
