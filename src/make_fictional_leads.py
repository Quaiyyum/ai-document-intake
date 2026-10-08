"""Writes three obviously fictional buyer-enquiry emails as PDFs into data/raw/lead/.

    python -m src.make_fictional_leads

Every person, address, number and domain here is made up on purpose. The three files differ in
layout and completeness so the review queue has something to catch.
"""
from __future__ import annotations

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

OUT_DIR = Path("data/raw/lead")
BANNER = "FICTIONAL SAMPLE - not a real person or enquiry"

EMAILS = [
    {
        "file": "lead_0001.pdf",
        "style": "header_block",
        "lines": [
            "From: Jane Example <jane@example.com>",
            "To: sales@example.org",
            "Date: 6 October 2026",
            "Subject: Enquiry about 12 Nowhere Street, Exampleton",
            "",
            "Hello,",
            "",
            "I saw the listing for 12 Nowhere Street, Exampleton and would like to arrange a viewing.",
            "We can go up to $900,000 and are hoping to buy within three months.",
            "The best way to reach me is by phone on 000 000 0000.",
            "",
            "Kind regards,",
            "Jane Example",
        ],
    },
    {
        "file": "lead_0002.pdf",
        "style": "plain_note",
        "lines": [
            "hi there - John Sample here. is 4 Placeholder Lane (Sampleville) still available??",
            "",
            "not sure on price range yet, need to talk to the bank first. no rush on timing.",
            "",
            "just email me back: john@example.com",
            "",
            "cheers",
        ],
    },
    {
        "file": "lead_0003.pdf",
        "style": "web_form",
        "lines": [
            "WEBSITE ENQUIRY FORM",
            "",
            "Your name ........... Pat Placeholder",
            "Email ............... pat(at)example.com",
            "Phone ............... 000 111",
            "Property ............ Unit 7, 99 Madeup Road, Exampleton",
            "Budget .............. 1.2m",
            "When are you buying . before Christmas 2026",
            "Contact me by ....... carrier pigeon",
            "",
            "Message: Please send the LIM report if you have one.",
        ],
    },
]


def draw(target: Path, style: str, lines: list[str]) -> None:
    page = canvas.Canvas(str(target), pagesize=A4)
    width, height = A4
    page.setFont("Helvetica-Bold", 9)
    page.drawString(20 * mm, height - 12 * mm, BANNER)
    font, size, left, gap = {
        "header_block": ("Helvetica", 11, 20 * mm, 16),
        "plain_note": ("Courier", 10, 30 * mm, 14),
        "web_form": ("Times-Roman", 12, 25 * mm, 20),
    }[style]
    page.setFont(font, size)
    y = height - 30 * mm
    for line in lines:
        page.drawString(left, y, line)
        y -= gap
    page.save()


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for email in EMAILS:
        target = OUT_DIR / email["file"]
        if target.exists():
            print(f"exists, left alone: {target}")
            continue
        draw(target, email["style"], email["lines"])
        print(f"wrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
