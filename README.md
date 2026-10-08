# AI Document Intake & Workflow Visibility

Semi-structured documents arrive as PDFs. An LLM extracts the fields defined in a YAML schema,
low-confidence fields go to a human review queue, and every document is logged in SQLite with a
status and real timestamps. Swapping the YAML file re-points the whole pipeline at a different
document type with no code change.

**Status: work in progress.** The accuracy table, re-point demo, dashboard and data statement
are added once the real runs are done. See `PROGRESS.md`.

## How to run

```bash
python3 -m venv .venv && source .venv/bin/activate     # Python 3.11+
pip install -r requirements.txt
cp .env.example .env                                   # then fill in provider, model, key
python -m pytest -q                                    # offline, no key needed

python -m src.fetch_docs                               # verify tender PDFs, write the manifest
python -m src.extract --schema config/schema_tender.yaml
python -m src.store sync
python -m src.review build                             # then fill reviewer_action in the CSV
python -m src.review apply
python -m src.evaluate --schema config/schema_tender.yaml
python -m src.export_bi
```
