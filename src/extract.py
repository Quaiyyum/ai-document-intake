"""Schema-driven extraction: PDF text -> LLM -> validated, scored JSON record.

    python -m src.extract --schema config/<schema>.yaml [--only DOC_ID ...]

The field list, prompt wording, validation and review threshold all come from the YAML file.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import llm
from .common import load_records, now_nz, save_records, squash
from .manifest import register_files
from .pdf_text import extract_text, has_text_layer
from .schema import FieldSpec, Schema, load_schema
from .validate import normalise


def build_prompt(schema: Schema, text: str) -> str:
    lines = [f"Document type: {schema.doc_type}", "", "Fields to extract:"]
    for spec in schema.fields:
        detail = f"- {spec.name} ({spec.type}, {'required' if spec.required else 'optional'}): {spec.description.strip()}"
        if spec.enum_values:
            detail += f" Allowed values: {', '.join(spec.enum_values)}."
        lines.append(detail)
    lines += [
        "",
        "Return one JSON object in exactly this shape, with every field listed above as a key:",
        '{"fields": {"<field name>": {"value": "<string or null>", "evidence": "<verbatim quote from the document, 20 words or fewer, or null>"}}}',
        "",
        "Document text:",
        '"""',
        text,
        '"""',
    ]
    return "\n".join(lines)


def score_field(spec: FieldSpec, value, issues: list[str], evidence, text: str) -> float:
    """Rule-based confidence. See the table in the README."""
    haystack = squash(text)
    if value is None:
        if spec.required:
            return 0.0
        mentioned = any(squash(word) in haystack for word in spec.keywords)
        return 0.5 if mentioned else 1.0
    if issues:
        return 0.3
    return 1.0 if grounded(evidence, haystack) or grounded(value, haystack) else 0.6


def grounded(quote, haystack: str) -> bool:
    """True when the quote is in the document word for word.

    A list value is often written on separate lines in the document and joined with ";" in the
    answer, so each ";"-separated part is checked on its own and all of them must be present.
    """
    parts = [squash(part).strip("\"'") for part in str(quote or "").split(";")]
    parts = [part for part in parts if part]
    return bool(parts) and all(part in haystack for part in parts)


def _empty_fields(schema: Schema, issue: str) -> dict:
    return {
        spec.name: {"value": None, "evidence": None, "confidence": 0.0, "issues": [issue], "final_value": None}
        for spec in schema.fields
    }


def process_document(schema: Schema, pdf_path: Path, doc_id: str, complete=None) -> dict:
    complete = complete or llm.complete_json
    record = {
        "doc_id": doc_id,
        "source_file": Path(pdf_path).as_posix(),
        "schema_used": schema.schema_name,
        "model": llm.model_name(),
        "extracted_at": None,
        "confidence_min": 0.0,
        "error": None,
        "fields": {},
    }
    try:
        text = extract_text(pdf_path, schema.max_chars)
        if not has_text_layer(text):
            record["fields"] = _empty_fields(schema, "no_text_layer")
        else:
            answer = (complete(schema.system_prompt, build_prompt(schema, text)) or {}).get("fields") or {}
            for spec in schema.fields:
                item = answer.get(spec.name)
                if not isinstance(item, dict):
                    item = {"value": item, "evidence": None}
                value, issues = normalise(spec, item.get("value"))
                issues = list(issues)
                if value is None and spec.required:
                    issues.append("missing_required")
                confidence = score_field(spec, value, issues, item.get("evidence"), text)
                if value is not None and not issues and confidence < 1.0:
                    issues.append("evidence_not_found")
                if value is None and not spec.required and confidence < 1.0:
                    issues.append("keyword_present_but_empty")
                record["fields"][spec.name] = {
                    "value": value,
                    "evidence": item.get("evidence"),
                    "confidence": confidence,
                    "issues": issues,
                    "final_value": None,
                }
    except (llm.BudgetExceeded, llm.ConfigError):
        raise
    except Exception as error:  # one bad file must not stop the batch
        record["error"] = f"{type(error).__name__}: {error}"
        record["fields"] = _empty_fields(schema, "extraction_error")
    record["confidence_min"] = min(item["confidence"] for item in record["fields"].values())
    record["extracted_at"] = now_nz()
    return record


def run(schema_path: str, only: list[str] | None = None) -> dict[str, dict]:
    schema = load_schema(schema_path)
    files = register_files(schema.doc_id_prefix, schema.input_glob)
    records = load_records()
    for source_file, doc_id in sorted(files.items(), key=lambda pair: pair[1]):
        if only and doc_id not in only:
            continue
        previous = records.get(doc_id)
        record = process_document(schema, Path(source_file), doc_id)
        if previous:  # keep the first extraction time and any review already applied
            record["extracted_at"] = previous.get("extracted_at") or record["extracted_at"]
            for name, item in record["fields"].items():
                old = previous.get("fields", {}).get(name, {})
                if old.get("value") == item["value"]:
                    item["final_value"] = old.get("final_value")
                    if "reviewed" in old:
                        item["reviewed"] = old["reviewed"]
        records[doc_id] = record
        flag = "ERROR" if record["error"] else f"min confidence {record['confidence_min']:.1f}"
        print(f"{doc_id}  {Path(source_file).name}  {flag}")
        save_records(records)
    save_records(records)
    return records


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--schema", required=True)
    parser.add_argument("--only", nargs="*", help="doc_ids to process (default: all files the schema matches)")
    args = parser.parse_args(argv)
    try:
        run(args.schema, args.only)
    except (llm.BudgetExceeded, llm.ConfigError) as error:
        print(f"STOPPED: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
