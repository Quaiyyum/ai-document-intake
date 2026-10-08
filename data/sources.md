# Sources

Every real document used in this project, so the corpus can be rebuilt. The files themselves are
third-party material and are not committed (`data/raw/` is gitignored).

## Tender notices (real, public)

Source: NZ Government Electronic Tenders Service, https://www.gets.govt.nz/

Each file is the public notice page saved as a PDF into `data/raw/tender/`.
Run `python -m src.fetch_docs` to verify the files and write `data/raw/manifest.csv`.

| doc_id | url | agency | retrieved | file_name | sha256 |
| --- | --- | --- | --- | --- | --- |

## Loan application form (real blank layout, fictional content)

To be added at checkpoint H4.

## Real-estate enquiries (fictional, script-written)

Written by `python -m src.make_fictional_leads`. No source document; every detail is made up.
