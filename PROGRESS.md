# Progress log

Plan: "Project A - Agent Execution Plan". One line per task: status, the check, its output.

| Task | Status | Check | Output |
| --- | --- | --- | --- |
| T0.1 | done | folder tree exists | config, data/raw/{tender,loan,lead}, src, gold, output, dashboard, tests, docs |
| T0.2 | done | `git check-ignore data/raw/x.pdf .env` | both paths printed |
| T0.3 | partly | imports succeed | verified in the build sandbox only; the laptop `.venv` is not created yet (Saleh: see README) |
| T0.4 | done | one `==` per line | 10 pinned packages (pandas dropped: nothing uses it) |
| T0.5 | WAITING H1 | `.env` has LLM_PROVIDER, LLM_MODEL, LLM_API_KEY | `.env.example` written; Saleh creates `.env` |
| T0.6 | done | files exist | PROGRESS.md, README.md |
| T1.1 | done | route chosen | Notice pages on gets.govt.nz are public and carry all 7 fields. The site says registration is needed to download detailed documents. robots.txt only blocks SEMrush bots. Neither the build sandbox nor the laptop's sandboxed shell can reach gets.govt.nz, so the route is **C**: Saleh saves each public notice page as a PDF. |
| T1.2 | WAITING H2 | 15 rows in data/sources.md | shortlist of 15 notices proposed to Saleh; table header ready |
| T1.3 | done (code) | manifest rows equal PDF count | `src/fetch_docs.py` written; not yet run on real files |
| T2.2 | partly | guide exists | `gold/LABELLING_GUIDE.md` written; CSV is created after H2 fixes the doc_ids |
| T3.1 | done | `python -m src.schema config/schema_tender.yaml` | prints 7 fields |
| T3.2 | done | loader prints 7 fields | all 7 defined explicitly |
| T3.3 | done | no schema field name in `src/` | enforced by `test_no_schema_field_name_is_hard_coded_in_src` |
| T4.1-T4.6 | done (code) | unit tests | pdf_text, llm, validate, extract written; no real LLM call made yet (0 of 80 used) |
| T4.7-T4.8 | blocked | | needs H1, H2, H3 |
| T5.1-T5.3, T5.5 | done (code) | unit tests | store, review written and tested with a mocked LLM |
| T6.2-T6.3 | done (code) | unit tests | evaluate written; report is byte-identical on rerun in tests |
| T7.4 | done | loader accepts the YAML; 3 PDFs have a text layer | `config/schema_realestate_lead.yaml`, `src/make_fictional_leads.py` |
| T7.1-T7.3 | WAITING H4 | | loan form not chosen yet |
| T8.1 | done (code) | | `src/export_bi.py` |
| T9.1-T9.9 | done | `python -m pytest -q` | 21 passed, no network, no key |
| T0.5 / H1 | done | `.env` has provider, model, key | openai, gpt-6-luna, LLM_REASONING_EFFORT=none, LLM_MAX_CALLS=120 |
| T1.2-T1.4 / H2 | done | 50 PDFs, all with a text layer | 50 notice pages printed to PDF on 2026-10-09; 1255 to 4261 characters each; sources.md stamped with date and sha256 |
| T2.1 | done | sets do not overlap | Random(42): 10 gold, 5 dev, 35 volume; see gold/split.md |
| T2.2-T2.3 / H3 | done | 0 format errors | rule-based draft (no LLM) verified by Saleh; 0 of 70 cells corrected |
| T2.4 | done | gold commit hash | 763817110e47346ca2702b2d128db0a489e10e5b |

Deviations from the plan
- `src/schema.py` names the field model `FieldSpec` (not `Field`) to avoid clashing with pydantic's `Field`.
- Lead schema field names carry a prefix or suffix (`lead_email`, `budget_nzd`, ...) so they cannot collide with type names in the code.
- The weakest-field paragraph lives in `output/weakest_field_note.md` and is pulled into the report, so regenerating the report never overwrites Saleh's edit.
- Corpus is 50 tenders (plan said 15) to give the dashboard real volume; the gold set is still 10.
- Gold labels were pre-filled by `gold/prefill_draft.py` (fixed rules, no LLM) and then verified by hand, instead of typed from scratch.
- `reference` is defined as the RFx ID, because the notice's own "Reference #" line is often blank.
