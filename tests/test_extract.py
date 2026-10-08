"""All tests run offline: the LLM is always replaced by a fixed function."""
from __future__ import annotations

import glob
import re
import shutil
import sqlite3
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError
from reportlab.pdfgen import canvas

from src import evaluate, extract, llm, review, store
from src.common import load_records
from src.extract import build_prompt, process_document, score_field
from src.schema import FieldSpec, load_schema
from src.validate import normalise

REPO = Path(__file__).resolve().parents[1]
TENDER = REPO / "config" / "schema_tender.yaml"

TOY_YAML = """
schema_name: schema_toy
doc_type: Toy note
doc_id_prefix: TOY
input_glob: data/raw/toy/*.pdf
review_threshold: 0.7
system_prompt: Return JSON only.
fields:
  - name: colour
    type: string
    required: true
    description: The colour named in the note.
    keywords: [colour]
  - name: due
    type: date
    required: false
    description: The due date.
    keywords: [due]
"""

TOY_TEXT = (
    "This is a toy note written only for the test suite. The chosen colour is green. "
    "It is due on 7 October 2026. The rest of this sentence is padding so the page has "
    "well over two hundred characters of text and counts as having a text layer."
)


def make_pdf(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(path))
    y = 800
    for start in range(0, len(text), 80):
        page.drawString(40, y, text[start:start + 80])
        y -= 16
    page.save()


@pytest.fixture
def workdir(tmp_path, monkeypatch):
    """An empty project folder with one toy schema and two toy PDFs."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("LLM_MODEL", "mock-model")
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "schema_toy.yaml").write_text(TOY_YAML)
    make_pdf(tmp_path / "data/raw/toy/a.pdf", TOY_TEXT)
    make_pdf(tmp_path / "data/raw/toy/b.pdf", TOY_TEXT)
    return tmp_path


def good_answer(system, user):
    return {"fields": {"colour": {"value": "green", "evidence": "The chosen colour is green"},
                       "due": {"value": "7 October 2026", "evidence": "due on 7 October 2026"}}}


def shaky_answer(system, user):
    # evidence that is not in the document -> 0.6 -> below the 0.7 threshold
    return {"fields": {"colour": {"value": "green", "evidence": "the walls were painted green"},
                       "due": {"value": "7 October 2026", "evidence": "due on 7 October 2026"}}}


# T9.1 schema loads
def test_tender_schema_has_seven_fields():
    assert len(load_schema(TENDER).fields) == 7


def test_unknown_type_is_rejected(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text(TOY_YAML.replace("type: string", "type: colour"))
    with pytest.raises(ValidationError):
        load_schema(bad)


def test_unknown_key_is_rejected(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text(TOY_YAML + "surprise: true\n")
    with pytest.raises(ValidationError):
        load_schema(bad)


# T9.2 prompt is schema-driven
def test_prompt_lists_every_schema_field(workdir):
    tender = load_schema(TENDER)
    prompt = build_prompt(tender, "some text")
    assert all(f"- {name} (" in prompt for name in tender.field_names)
    toy_prompt = build_prompt(load_schema("config/schema_toy.yaml"), "some text")
    assert re.findall(r"^- (\w+) \(", toy_prompt, re.M) == ["colour", "due"]


def test_no_schema_field_name_is_hard_coded_in_src():
    """The core claim of the project: the code knows nothing about any document type."""
    source = {path: Path(path).read_text() for path in glob.glob(str(REPO / "src" / "*.py"))}
    hits = []
    for config in glob.glob(str(REPO / "config" / "schema_*.yaml")):
        for spec in yaml.safe_load(Path(config).read_text())["fields"]:
            pattern = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(spec['name'])}(?![A-Za-z0-9_])")
            hits += [f"{spec['name']} in {Path(p).name}" for p, text in source.items() if pattern.search(text)]
    assert hits == []


# T9.3 date normalisation
@pytest.mark.parametrize("raw", ["7 October 2026", "07/10/2026", "2026-10-07", "Wednesday, 7 October 2026, 2:00 PM"])
def test_dates_normalise_day_first(raw):
    spec = FieldSpec(name="d", type="date", description="x")
    assert normalise(spec, raw) == ("2026-10-07", [])


def test_bad_date_fails_validation():
    spec = FieldSpec(name="d", type="date", description="x")
    assert normalise(spec, "tomorrow")[1] == ["invalid_date"]


def test_number_enum_email_and_regex():
    assert normalise(FieldSpec(name="n", type="number", description="x"), "$900,000") == ("900000", [])
    enum = FieldSpec(name="e", type="enum", description="x", enum_values=["email", "phone"])
    assert normalise(enum, "Phone") == ("phone", [])
    assert normalise(enum, "carrier pigeon")[1] == ["not_in_enum"]
    assert normalise(FieldSpec(name="m", type="email", description="x"), "pat(at)example.com")[1] == ["invalid_email"]
    ref = FieldSpec(name="r", type="string", description="x", validate_regex="^[A-Z0-9-]{3,10}$")
    assert normalise(ref, "has spaces!")[1] == ["regex_mismatch"]


# T9.4 confidence rules, one case per row of the table
def test_confidence_rules():
    text = "The chosen colour is green. Nothing else is said."
    required = FieldSpec(name="a", type="string", required=True, description="x", keywords=["colour"])
    optional_seen = FieldSpec(name="b", type="string", description="x", keywords=["colour"])
    optional_unseen = FieldSpec(name="c", type="string", description="x", keywords=["deadline"])
    assert score_field(required, "green", [], "the chosen  COLOUR is green", text) == 1.0
    assert score_field(required, "green", [], "painted green", text) == 0.6
    assert score_field(required, "green", ["regex_mismatch"], "The chosen colour is green", text) == 0.3
    assert score_field(required, None, ["missing_required"], None, text) == 0.0
    assert score_field(optional_unseen, None, [], None, text) == 1.0
    assert score_field(optional_seen, None, [], None, text) == 0.5


# T9.5 review routing
def test_low_confidence_field_goes_to_review(workdir, monkeypatch):
    monkeypatch.setattr(llm, "complete_json", shaky_answer)
    extract.run("config/schema_toy.yaml")
    store.sync()
    assert store.status_counts() == {"needs_review": 2}
    assert review.build() == 2
    queue = review.load_queue()
    assert {(row["doc_id"][:3], row["field"], row["confidence"]) for row in queue} == {("TOY", "colour", "0.6")}


def test_review_apply_marks_processed_and_keeps_model_value(workdir, monkeypatch):
    monkeypatch.setattr(llm, "complete_json", shaky_answer)
    extract.run("config/schema_toy.yaml")
    store.sync()
    review.build()
    rows = review.load_queue()
    rows[0]["reviewer_action"], rows[0]["reviewed_value"] = "correct", "teal"
    review.save_queue(rows)  # the second document is left unreviewed
    done = review.apply()
    assert done == [rows[0]["doc_id"]]
    assert store.status_counts() == {"needs_review": 1, "processed": 1}
    item = load_records()[done[0]]["fields"]["colour"]
    assert (item["value"], item["final_value"]) == ("green", "teal")
    review.build()  # a rebuild keeps the reviewer's columns
    assert review.load_queue()[0]["reviewer_action"] == "correct"
    assert review.apply() == []  # and applying twice does nothing


# T9.6 re-point: same code, different schema, different keys
def test_repoint_returns_the_toy_schema_fields(workdir):
    record = process_document(load_schema("config/schema_toy.yaml"), Path("data/raw/toy/a.pdf"), "TOY-1", good_answer)
    assert list(record["fields"]) == ["colour", "due"]
    assert record["fields"]["due"]["value"] == "2026-10-07"
    assert record["confidence_min"] == 1.0 and record["error"] is None


def test_one_bad_file_does_not_stop_the_batch(workdir, monkeypatch):
    Path("data/raw/toy/c.pdf").write_bytes(b"not a pdf")
    monkeypatch.setattr(llm, "complete_json", good_answer)
    records = extract.run("config/schema_toy.yaml")
    assert len(records) == 3
    broken = [r for r in records.values() if r["error"]]
    assert len(broken) == 1 and broken[0]["confidence_min"] == 0.0


# T9.7 store is idempotent and never downgrades
def test_store_sync_is_idempotent(workdir, monkeypatch):
    monkeypatch.setattr(llm, "complete_json", good_answer)
    extract.run("config/schema_toy.yaml")
    assert store.sync() == 2 and store.sync() == 2
    assert store.status_counts() == {"extracted": 2}
    connection = sqlite3.connect("output/intake.db")
    assert connection.execute("SELECT COUNT(*) FROM applications WHERE processed_at IS NOT NULL").fetchone()[0] == 2
    connection.execute("UPDATE applications SET status='processed'")
    connection.commit()
    connection.close()
    monkeypatch.setattr(llm, "complete_json", shaky_answer)
    extract.run("config/schema_toy.yaml")
    store.sync()
    assert store.status_counts() == {"processed": 2}


# T9.8 evaluation rules
def test_comparison_rules():
    assert evaluate.same("  Waikato  District ", "waikato district")
    assert evaluate.same("", None)
    assert evaluate.same("2026-10-07", "2026-10-07")
    assert not evaluate.same("Waikato District Council", "Waikato District")
    assert not evaluate.same("", "something")


def test_accuracy_report_is_deterministic(workdir, monkeypatch):
    monkeypatch.setattr(llm, "complete_json", shaky_answer)
    extract.run("config/schema_toy.yaml")
    Path("gold").mkdir()
    Path("gold/labels_toy.csv").write_text(
        "doc_id,colour,due\nTOY-2026-0001,green,2026-10-07\nTOY-2026-0002,blue,\n".replace("2026-0", f"{load_year()}-0", 2))
    evaluate.main(["--schema", "config/schema_toy.yaml"])
    first = Path("output/accuracy_report_toy.md").read_text()
    evaluate.main(["--schema", "config/schema_toy.yaml"])
    assert Path("output/accuracy_report_toy.md").read_text() == first
    assert "| colour | 1 | 2 | 50% | weakest |" in first
    assert "| **overall** | 2 | 4 | 50% | |" in first
    assert "flagged: 1 of 2" in first


def load_year() -> str:
    return next(iter(load_records()))[4:8]


def test_cache_means_second_call_is_free(workdir, monkeypatch):
    calls = []
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("LLM_API_KEY", "test")
    monkeypatch.setitem(llm.PROVIDERS, "openai", lambda s, system, user: calls.append(1) or '{"fields": {}}')
    assert llm.complete_json("s", "u") == llm.complete_json("s", "u") == {"fields": {}}
    assert len(calls) == 1 and llm.calls_made() == 1


def test_budget_cap_stops_calls(workdir, monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("LLM_API_KEY", "test")
    monkeypatch.setenv("LLM_MAX_CALLS", "1")
    monkeypatch.setitem(llm.PROVIDERS, "openai", lambda s, system, user: '{"fields": {}}')
    llm.complete_json("s", "one")
    with pytest.raises(llm.BudgetExceeded):
        llm.complete_json("s", "two")
