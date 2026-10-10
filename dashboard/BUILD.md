# Building the Power BI page (about 30 minutes)

Data file: `applications.csv`, one row per document, exported from the SQLite status table by
`python -m src.export_bi`. It holds 56 documents: 50 real public tender notices, 3 fictional loan
applications and 3 fictional real-estate enquiries. Nothing in it is personal data.

## 1. Load the data

1. Open Power BI Desktop. Home > Get data > Text/CSV > choose `applications.csv` > Load.
2. Open the Data view (table icon on the left) and check these column types; fix any that differ
   with Column tools > Data type:

| Column | Type |
| --- | --- |
| `received_at`, `processed_at` | Date/time |
| `received_date` | Date |
| `turnaround_minutes`, `confidence_min` | Whole number / Decimal number |
| everything else | Text |

## 2. Add three measures

Home > New measure, once for each line:

```
Documents = COUNTROWS(applications)
Needs review rate = DIVIDE(CALCULATE(COUNTROWS(applications), applications[needed_review] = "Yes"), COUNTROWS(applications))
Avg turnaround (min) = AVERAGE(applications[turnaround_minutes])
```

Select `Needs review rate` and set its format to Percentage (Measure tools > Format).

## 3. Build the visuals

| # | Visual | Type | Axis | Values | Legend |
| --- | --- | --- | --- | --- | --- |
| 1 | Intake volume | Stacked column chart | `doc_type` | `Documents` | `status` |
| 2 | Workflow status | Clustered bar chart | `status` | `Documents` | |
| 3 | Turnaround | Clustered bar chart | `doc_type` | `Avg turnaround (min)` | |
| 4 | Needs-review rate | Card | | `Needs review rate` | |
| 5 | Filter | Slicer | `doc_type` | | |

Give each visual a plain title (Format > General > Title), for example
"Documents received by type and status". Add a page title: "Document intake: volume, status and turnaround".

## 4. What the numbers should show (check against these)

| Check | Expected |
| --- | --- |
| Total documents | 56 |
| Status: extracted / processed / needs_review | 41 / 12 / 3 |
| Needs review rate | 26.8% (15 of 56 went to the review queue) |
| Tender notices / loan applications / enquiries | 50 / 3 / 3 |

## 5. Things to know before presenting it

- Every document was received on one day (2026-10-09), so a chart by date would be a single bar.
  That is why visual 1 uses document type on the axis. If more documents are added on later days,
  switch its axis to `received_date`.
- Turnaround is real clock time from one demo run (files saved about 08:20, extraction about 10:00,
  human review about 11:25). It is not a figure for live operations.
- `turnaround_minutes` is empty for the 3 documents still waiting for review, so they are left out
  of the average.

## 6. Save and export

1. File > Save as > `intake.pbix`, in this same folder.
2. File > Export > Export to PDF, or take a screenshot of the page, and save it as `screenshot.png`
   in this same folder.

Both files then go into the repo's `dashboard/` folder.
