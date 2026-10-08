"""Fills a real blank loan application form with three obviously fictional applicants.

    python -m src.make_fictional_loans

Input:  data/raw/loan/blank.pdf  (a lender's own blank form; see data/sources.md; never committed)
Output: data/raw/loan/loan_0001.pdf ... loan_0003.pdf

The layout is the lender's real form. Every person, address, employer and number typed into it is
made up on purpose, and each page is stamped as a fictional sample. The three copies differ so the
review queue has something to catch: one complete, one with gaps, one with awkward formats.
The values are typed onto the page (not stored as form data), as if the form had been printed.
"""
from __future__ import annotations

import io
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject
from reportlab.pdfgen import canvas

FOLDER = Path("data/raw/loan")
BLANK = FOLDER / "blank.pdf"
BANNER = "FICTIONAL SAMPLE - Example applicant, not a real person or application"

# Which box on the blank form each made-up value is typed into (the form's own box names).
BOXES = {
    "first": "Text Field 2", "last": "Text Field 3", "born": "Text Field 5",
    "job": "Text Field 19", "works_at": "Text Field 20", "works_where": "Text Field 21",
    "street": "Text Field 28", "town": "Text Field 29", "postcode": "Text Field 31",
    "mobile": "Text Field 39", "mail": "Text Field 41", "yearly_pay": "Text Field 88",
    "why": "Text Field 169", "price": "Text Field 170", "saved": "Text Field 171",
    "borrow": "Text Field 172", "buying": "Text Field 173", "settle": "Text Field 174",
}

APPLICANTS = [
    {   # complete and tidy
        "file": "loan_0001.pdf",
        "first": "Jane", "last": "Example", "born": "14/02/1990",
        "job": "Widget Tester", "works_at": "Example Widgets Ltd", "works_where": "1 Sample Road, Exampleton",
        "street": "12 Nowhere Street", "town": "Exampleton", "postcode": "0000",
        "mobile": "000 000 0000", "mail": "jane@example.com", "yearly_pay": "80,000",
        "why": "Buy a first home", "price": "500,000", "saved": "100,000", "borrow": "400,000",
        "buying": "7 Madeup Road, Exampleton", "settle": "15/12/2026",
    },
    {   # three boxes left empty: employer, yearly pay, settlement date
        "file": "loan_0002.pdf",
        "first": "John", "last": "Sample", "born": "03/09/1985",
        "job": "Self employed",
        "street": "4 Placeholder Lane", "town": "Sampleville", "postcode": "0000",
        "mobile": "000 000 0000", "mail": "john@example.com",
        "why": "Refinance existing home loan", "price": "600,000", "saved": "300,000", "borrow": "300,000",
        "buying": "4 Placeholder Lane, Sampleville",
    },
    {   # awkward formats: written-out date, two-digit year, "k" amounts, a range
        "file": "loan_0003.pdf",
        "first": "Pat", "last": "Placeholder", "born": "1st March 1978",
        "job": "Sample Baker", "works_at": "The Example Bakery", "works_where": "99 Madeup Road, Exampleton",
        "street": "Unit 7, 99 Madeup Road", "town": "Exampleton", "postcode": "0000",
        "mobile": "000 000 0000", "mail": "pat@example.com", "yearly_pay": "about 65k",
        "why": "Build a rental", "price": "450k", "saved": "90k", "borrow": "350-360k",
        "buying": "Lot 2, Nowhere Street, Exampleton", "settle": "01/02/27",
    },
]


def box_positions(reader: PdfReader) -> dict[str, tuple[int, list[float]]]:
    found = {}
    for number, page in enumerate(reader.pages):
        for item in page.get("/Annots") or []:
            widget = item.get_object()
            if widget.get("/T") and widget.get("/Rect"):
                found[str(widget["/T"])] = (number, [float(v) for v in widget["/Rect"]])
    return found


def fill(applicant: dict, target: Path) -> None:
    reader = PdfReader(str(BLANK))
    where = box_positions(reader)
    writer = PdfWriter()
    for number, page in enumerate(reader.pages):
        width, height = float(page.mediabox.width), float(page.mediabox.height)
        buffer = io.BytesIO()
        layer = canvas.Canvas(buffer, pagesize=(width, height))
        layer.setFont("Helvetica-Bold", 8)
        layer.setFillColorRGB(0.8, 0, 0)
        layer.drawString(40, 14, BANNER)
        layer.setFillColorRGB(0, 0, 0.5)
        layer.setFont("Courier", 9)
        for key, box in BOXES.items():
            if key not in applicant:
                continue
            if box not in where:
                raise SystemExit(f"the blank form has no box called '{box}'; is this a different form?")
            on_page, (x0, y0, x1, y1) = where[box]
            if on_page == number:
                layer.drawString(x0 + 3, y0 + (y1 - y0 - 9) / 2 + 2, applicant[key])
        layer.save()
        buffer.seek(0)
        page.merge_page(PdfReader(buffer).pages[0])
        if "/Annots" in page:  # drop the interactive boxes so the result is a flat, typed page
            del page[NameObject("/Annots")]
        writer.add_page(page)
    with open(target, "wb") as handle:
        writer.write(handle)


def main() -> int:
    if not BLANK.exists():
        raise SystemExit(f"missing {BLANK}: download the blank form listed in data/sources.md first")
    for applicant in APPLICANTS:
        target = FOLDER / applicant["file"]
        if target.exists():
            print(f"exists, left alone: {target}")
            continue
        fill(applicant, target)
        print(f"wrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
