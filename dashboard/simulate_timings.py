"""Writes dashboard/applications_simulated.csv: the real status table with SIMULATED timestamps.

    python dashboard/simulate_timings.py

Why: every document in this demo was really received on one day, so charts over time are a single
bar. This script spreads arrivals over three working weeks so the report layout can be built and
judged. Only the three time columns are invented. doc_id, status, confidence and document type are
the real pipeline output. The real timings stay in applications.csv and are never altered.

Every row is marked timing_basis = SIMULATED, and any report built on this file must say so.
"""
from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

SOURCE = Path("dashboard/applications.csv")
TARGET = Path("dashboard/applications_simulated.csv")
FORMAT = "%Y-%m-%d %H:%M"
FIRST_DAY = datetime(2026, 9, 21)   # a Monday
WORKING_DAYS = 15                   # three weeks, Monday to Friday


def main() -> int:
    rng = random.Random(42)
    rows = list(csv.DictReader(open(SOURCE, newline="", encoding="utf-8")))
    days = [FIRST_DAY + timedelta(days=offset) for offset in range(21) if (FIRST_DAY + timedelta(days=offset)).weekday() < 5]
    assert len(days) == WORKING_DAYS
    for row in rows:
        received = rng.choice(days) + timedelta(hours=rng.randint(8, 16), minutes=rng.randint(0, 59))
        if row["status"] == "extracted":      # no person involved: minutes
            done = received + timedelta(minutes=rng.randint(2, 20))
        elif row["status"] == "processed":    # waited for a reviewer: hours to two days
            done = received + timedelta(minutes=rng.randint(60, 48 * 60))
        else:                                 # still waiting for review
            done = None
        row["received_at"] = received.strftime(FORMAT)
        row["received_date"] = received.strftime("%Y-%m-%d")
        row["processed_at"] = done.strftime(FORMAT) if done else ""
        row["turnaround_minutes"] = int((done - received).total_seconds() // 60) if done else ""
        row["timing_basis"] = "SIMULATED"
    with open(TARGET, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {TARGET} (timestamps simulated, everything else real)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
