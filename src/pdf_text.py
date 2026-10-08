"""PDF text extraction. No OCR: a file without a text layer goes to review."""
from __future__ import annotations

from pathlib import Path

import pdfplumber

MIN_CHARS = 200


def extract_text(path: str | Path, max_chars: int = 12000) -> str:
    parts: list[str] = []
    with pdfplumber.open(str(path)) as pdf:
        for number, page in enumerate(pdf.pages, start=1):
            parts.append(f"--- page {number} ---\n{page.extract_text() or ''}")
    return "\n".join(parts)[:max_chars]


def has_text_layer(text: str) -> bool:
    body = "\n".join(line for line in text.splitlines() if not line.startswith("--- page "))
    return len(body.strip()) >= MIN_CHARS
