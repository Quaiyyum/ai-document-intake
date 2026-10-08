"""Type-driven normalisation and validation. Behaviour depends only on the field's declared type."""
from __future__ import annotations

import re
from datetime import datetime

from dateutil import parser as date_parser

from .schema import FieldSpec

ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _clean(raw) -> str | None:
    if raw is None:
        return None
    text = re.sub(r"\s+", " ", str(raw)).strip()
    return text or None


def _to_date(text: str) -> str:
    if ISO_DATE.match(text):
        return datetime.strptime(text, "%Y-%m-%d").strftime("%Y-%m-%d")
    # NZ documents are day-first: 07/10/2026 is 7 October.
    return date_parser.parse(text, dayfirst=True).strftime("%Y-%m-%d")


def _to_number(text: str) -> str:
    stripped = re.sub(r"(?i)nzd|[$,\s]", "", text)
    number = float(stripped)
    return str(int(number)) if number == int(number) else str(number)


def normalise(spec: FieldSpec, raw) -> tuple[str | None, list[str]]:
    """Return (value, issues). An empty issues list means the value passed validation."""
    text = _clean(raw)
    if text is None:
        return None, []
    issues: list[str] = []
    value = text
    try:
        if spec.type == "date":
            value = _to_date(text)
        elif spec.type == "number":
            value = _to_number(text)
        elif spec.type == "email":
            value = text.lower()
            if not EMAIL.match(value):
                issues.append("invalid_email")
        elif spec.type == "phone":
            if len(re.sub(r"\D", "", text)) < 7 or re.search(r"[^\d+()\-\s]", text):
                issues.append("invalid_phone")
        elif spec.type == "enum":
            lookup = {option.lower(): option for option in spec.enum_values or []}
            if text.lower() in lookup:
                value = lookup[text.lower()]
            else:
                issues.append("not_in_enum")
    except (ValueError, OverflowError):
        issues.append(f"invalid_{spec.type}")
        value = text
    if spec.validate_regex and not issues and not re.search(spec.validate_regex, value):
        issues.append("regex_mismatch")
    return value, issues
