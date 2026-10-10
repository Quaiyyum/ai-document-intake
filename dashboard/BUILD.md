# Building the Power BI page (about 30 minutes)

Data file: `applications.csv`, one row per document, exported from the SQLite status table by
`python -m src.export_bi`. It holds 56 documents: 50 real public tender notices, 3 fictional loan
applications and 3 fictional real-estate enquiries. Nothing in it is personal data.

## 0. Which data file

| File | Timestamps | Use it for |
| --- | --- | --- |
| `applications_simulated.csv` | SIMULATED: arrivals spread over 21 Sep to 9 Oct 2026 | Building and laying out the report |
| `applications.csv` | Real: everything arrived on 9 Oct 2026 | The honest record; swap to it in step 7 if you want real timings shown |

In the simulated file only `received_at`, `received_date`, `processed_at` and `turnaround_minutes`
are invented. Status, confidence and document type are the real pipeline output in both files.
While the report uses the simulated file it must carry the label in step 3.

## 1. Load the data

1. Open Power BI Desktop. Home > Get data > Text/CSV > choose `applications_simulated.csv` > Transform Data.
2. In the Power Query window, rename the query (right-hand pane, Name) to `applications`, then Close & Apply.
   The measures below use that name, and it makes swapping the file later a one-click change.
3. Open the Data view (table icon on the left) and check these column types; fix any that differ
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
| 1 | Intake volume | Stacked column chart | `received_date` (choose the date itself, not the Date Hierarchy) | `Documents` | `doc_type` |
| 2 | Workflow status | Clustered bar chart | `status` | `Documents` | |
| 3 | Turnaround | Clustered bar chart | `doc_type` | `Avg turnaround (min)` | |
| 4 | Needs-review rate | Card | | `Needs review rate` | |
| 5 | Filter | Slicer | `doc_type` | | |

Give each visual a plain title (Format > General > Title), for example "Documents received per day".
Add a page title: "Document intake: volume, status and turnaround".

**Required label while the simulated file is loaded:** add a text box under the page title reading
"Arrival and processing times are simulated for layout. Status, confidence and document type are real."

## 4. What the numbers should show (check against these)

| Check | Expected |
| --- | --- |
| Total documents | 56 |
| Status: extracted / processed / needs_review | 41 / 12 / 3 |
| Needs review rate | 26.8% (15 of 56 went to the review queue) |
| Tender notices / loan applications / enquiries | 50 / 3 / 3 |
| Days with arrivals (simulated file) | 14, between 21 Sep and 9 Oct 2026 |

## 5. Things to know before presenting it

- With the simulated file, the dates, the daily volumes and the turnaround figures are made up and
  must not be quoted as results. The counts in the table above are real.
- With the real file, every document arrived on 2026-10-09, so visual 1 is a single bar; put
  `doc_type` on its axis instead. Real turnaround is clock time from one demo run, not a figure for
  live operations.
- `turnaround_minutes` is empty for the 3 documents still waiting for review, so they are left out
  of the average.

## 6. Save and export

1. File > Save as > `intake.pbix`, in this same folder.
2. File > Export > Export to PDF, or take a screenshot of the page, and save it as `screenshot.png`
   in this same folder.

Both files then go into the repo's `dashboard/` folder.

## 7. Swapping to the real timings later

Home > Transform data > Data source settings > Change Source > choose `applications.csv` > Close & Apply.
Then remove the "simulated" text box and change visual 1's axis to `doc_type`.
