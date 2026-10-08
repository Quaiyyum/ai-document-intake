# Labelling guide: gold/labels_tender.csv

The gold set is typed by hand from the PDFs before any extraction runs, then frozen in git.
It is never filled, corrected or "tidied" by a model, and never used for prompt tuning.
`gold/worklist.md` lists the 10 PDFs to open.

General rules
1. Copy values as printed on the notice. Do not tidy spelling or expand abbreviations.
2. Where a value wraps over two lines in the PDF, type it as one line with single spaces.
3. A field that is not on the notice is left empty.

| Column | Where it is on the notice | Rule |
| --- | --- | --- |
| `agency` | Breadcrumb near the top: `GETS > <agency> > ...` | The organisation name exactly as printed there |
| `title` | `Tender Name :` | As printed |
| `reference` | `RFx ID :` | The digits only. Not the `Reference #` line |
| `close_date` | `Close Date :` | `YYYY-MM-DD`, date only, no time |
| `category` | `Categories :` (may be several lines) | Each entry as printed, e.g. `43230000 - Software`. Join several with `; ` in alphabetical order, which is ascending code order |
| `region` | `Regions:` | As printed. Join several with `; ` in alphabetical order |
| `contact_name` | First line after `Contact :` | The name only (a person or a team). No job title, email or phone |

If a value contains a comma, your spreadsheet app quotes it automatically when saving as CSV;
in a text editor, wrap the whole value in double quotes.
