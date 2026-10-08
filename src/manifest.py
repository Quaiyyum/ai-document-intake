"""data/raw/manifest.csv: one row per file received, with the real time it landed on disk.

received_at feeds the turnaround figure, so an existing row is never rewritten.
"""
from __future__ import annotations

import csv
import glob
from pathlib import Path

from .common import MANIFEST, mtime_nz, sha256_file

COLUMNS = ["doc_id", "source_file", "received_at", "bytes", "sha256"]


def load_manifest(path: Path = MANIFEST) -> list[dict]:
    if not Path(path).exists():
        return []
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def save_manifest(rows: list[dict], path: Path = MANIFEST) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda row: row["doc_id"]))


def make_row(doc_id: str, file_path: Path) -> dict:
    return {
        "doc_id": doc_id,
        "source_file": file_path.as_posix(),
        "received_at": mtime_nz(file_path),
        "bytes": file_path.stat().st_size,
        "sha256": sha256_file(file_path),
    }


def register_files(prefix: str, pattern: str, path: Path = MANIFEST) -> dict[str, str]:
    """Give every file matching `pattern` a doc_id. Returns {source_file: doc_id}."""
    rows = load_manifest(path)
    known = {row["source_file"]: row["doc_id"] for row in rows}
    changed = False
    for name in sorted(glob.glob(pattern)):
        file_path = Path(name)
        if file_path.as_posix() in known:
            continue
        year = mtime_nz(file_path)[:4]
        stem = f"{prefix}-{year}-"
        taken = [int(r["doc_id"][len(stem):]) for r in rows if r["doc_id"].startswith(stem)]
        doc_id = f"{stem}{max(taken, default=0) + 1:04d}"
        rows.append(make_row(doc_id, file_path))
        known[file_path.as_posix()] = doc_id
        changed = True
    if changed:
        save_manifest(rows, path)
    return {name: doc_id for name, doc_id in known.items() if name in {Path(p).as_posix() for p in glob.glob(pattern)}}
