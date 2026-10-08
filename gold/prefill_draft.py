"""Rule-based draft of the gold labels, for a person to verify against each PDF.

    python gold/prefill_draft.py            # writes gold/prefill_draft.csv for the gold test set
    python gold/prefill_draft.py --dev      # prints the draft for the dev set instead (to test the rules)

This reads the labelled lines of a GETS notice with fixed rules. It does not use an LLM, so the
draft is independent of the model whose accuracy the gold set measures. It is specific to GETS
notices on purpose and is not part of the pipeline in src/.
"""
from __future__ import annotations

import csv
import logging
import re
import sys
from pathlib import Path

import pdfplumber
from dateutil import parser as date_parser

logging.getLogger("pdfminer").setLevel(logging.ERROR)
COLUMNS = ["doc_id", "agency", "title", "reference", "close_date", "category", "region", "contact_name"]
LABELS = ["RFx ID", "Tender Name", "Reference #", "Open Date", "Close Date", "Business Unit", "Tender Type", "Tender Coverage",
          "Categories", "Regions", "Exemption Reason", "Required Pre-qualifications", "Contact",
          "Alternate Physical Delivery Address", "Alternate Physical Fax Number", "Overview"]


def one_line(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def read_notice(path: Path) -> tuple[str, str]:
    """Return (whole first page text, details column text without the left-hand site menu)."""
    with pdfplumber.open(str(path)) as pdf:
        page = pdf.pages[0]
        full = page.extract_text() or ""
        # Labels are right-aligned, so the longest one ("Alternate Physical ...") marks the column's left edge.
        words = page.extract_words()
        edges = [w["x0"] for w in words if w["text"] in ("Alternate", "Required")]
        left = max(min(edges) - 4, 0) if edges else 0
        parts = [page.crop((left, 0, page.width, page.height)).extract_text() or ""]
        parts += [(p.crop((left, 0, p.width, p.height)).extract_text() or "") for p in pdf.pages[1:]]
    return full, "\n".join(parts)


def sections(details: str) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    current = None
    pattern = re.compile(r"^(" + "|".join(re.escape(label) for label in LABELS) + r")\s*:?\s*(.*)$")
    for line in details.splitlines():
        match = pattern.match(line.strip())
        if match and match.group(1) not in found:
            current = match.group(1)
            found[current] = [match.group(2)] if match.group(2) else []
        elif current:
            found[current].append(line.strip())
    return found


def draft(path: Path) -> dict[str, str]:
    full, details = read_notice(path)
    part = sections(details)
    crumb = re.search(r"GETS > (.+?) > ", one_line(full))
    close = one_line(" ".join(part.get("Close Date", [])))
    close = re.sub(r"\(.*$", "", close)
    categories, entry = [], ""
    for line in part.get("Categories", []):
        if re.match(r"^\d{8} - ", line):
            if entry:
                categories.append(entry)
            entry = line
        elif entry and line:
            entry += " " + line
    if entry:
        categories.append(entry)
    regions = [one_line(r) for r in " ".join(part.get("Regions", [])).split(",") if one_line(r)]
    contact = part.get("Contact", [])
    return {
        "agency": crumb.group(1) if crumb else "",
        "title": one_line(" ".join(part.get("Tender Name", []))),
        "reference": one_line(" ".join(part.get("RFx ID", []))),
        "close_date": date_parser.parse(close, dayfirst=True).strftime("%Y-%m-%d") if close else "",
        "category": "; ".join(sorted(one_line(c) for c in categories)),
        "region": "; ".join(sorted(regions)),
        "contact_name": one_line(contact[0]) if contact else "",
    }


def ids_in(heading: str) -> list[str]:
    text = Path("gold/split.md").read_text()
    block = text.split(f"## {heading}")[1].split("##")[0]
    return re.findall(r"GETS-\d{4}-\d{4}", block)


def main() -> int:
    files = {row["doc_id"]: Path(row["source_file"]) for row in csv.DictReader(open("data/raw/manifest.csv"))}
    dev = "--dev" in sys.argv
    rows = [{"doc_id": doc_id, **draft(files[doc_id])} for doc_id in ids_in("Dev set" if dev else "Gold test set")]
    if dev:
        for row in rows:
            print("\n".join(f"{key:13} {value}" for key, value in row.items()), end="\n\n")
        return 0
    with open("gold/prefill_draft.csv", "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote gold/prefill_draft.csv ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
