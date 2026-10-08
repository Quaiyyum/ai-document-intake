"""Human review queue for low-confidence fields.

    python -m src.review build    # write output/review_queue.csv
    python -m src.review apply    # apply the reviewer's decisions

reviewer_action is one of: accept (extracted value is right), correct (use reviewed_value), blank (no value).
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

from . import store
from .common import REVIEW_QUEUE, load_records, now_nz, save_records

COLUMNS = ["doc_id", "source_file", "field", "extracted_value", "evidence", "confidence", "issue",
           "reviewer_action", "reviewed_value", "reviewed_at"]
ACTIONS = {"accept", "correct", "blank"}


def load_queue(path: Path = REVIEW_QUEUE) -> list[dict]:
    if not Path(path).exists():
        return []
    with open(path, newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def save_queue(rows: list[dict], path: Path = REVIEW_QUEUE) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def build(path: Path = REVIEW_QUEUE) -> int:
    limits = store.thresholds()
    kept = {(row["doc_id"], row["field"]): row for row in load_queue(path)}
    rows = []
    for doc_id, record in sorted(load_records().items()):
        limit = limits.get(record["schema_used"], 0.7)
        for name, item in record["fields"].items():
            if item["confidence"] >= limit:
                continue
            old = kept.get((doc_id, name), {})
            same = old.get("extracted_value", "") == (item["value"] or "")
            rows.append({
                "doc_id": doc_id,
                "source_file": Path(record["source_file"]).name,
                "field": name,
                "extracted_value": item["value"] or "",
                "evidence": item["evidence"] or "",
                "confidence": item["confidence"],
                "issue": "; ".join(item["issues"]),
                "reviewer_action": old.get("reviewer_action", "") if same else "",
                "reviewed_value": old.get("reviewed_value", "") if same else "",
                "reviewed_at": old.get("reviewed_at", "") if same else "",
            })
    save_queue(rows, path)
    return len(rows)


def apply(path: Path = REVIEW_QUEUE) -> list[str]:
    rows = load_queue(path)
    records = load_records()
    by_doc: dict[str, list[dict]] = {}
    for row in rows:
        row["reviewer_action"] = (row.get("reviewer_action") or "").strip().lower()
        by_doc.setdefault(row["doc_id"], []).append(row)
    bad = sorted({row["reviewer_action"] for row in rows if row["reviewer_action"]} - ACTIONS)
    if bad:
        raise SystemExit(f"unknown reviewer_action values: {bad}; use accept, correct or blank")
    done = []
    when = now_nz()
    for doc_id, doc_rows in by_doc.items():
        if doc_id not in records or not all(row["reviewer_action"] for row in doc_rows):
            continue  # partly reviewed documents stay in the queue
        if all(row.get("reviewed_at") for row in doc_rows):
            continue  # already applied
        for row in doc_rows:
            item = records[doc_id]["fields"][row["field"]]
            action = row["reviewer_action"]
            if action == "accept":
                item["final_value"] = item["value"]
            elif action == "correct":
                item["final_value"] = (row.get("reviewed_value") or "").strip() or None
            else:
                item["final_value"] = None
            item["reviewed"] = action
            row["reviewed_at"] = when
        store.mark_processed(doc_id, when)
        done.append(doc_id)
    save_records(records)
    save_queue(rows, path)
    return done


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "build":
        print(f"{build()} fields queued in {REVIEW_QUEUE}")
    elif command == "apply":
        finished = apply()
        print(f"processed {len(finished)} documents: {', '.join(finished) or 'none'}")
    else:
        sys.exit("usage: python -m src.review build|apply")
