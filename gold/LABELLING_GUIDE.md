# Labelling guide: gold/labels_tender.csv

The gold set is typed by hand from the PDFs before any extraction runs, then frozen in git.
It is never filled, corrected or "tidied" by a model, and never used for prompt tuning.

1. Copy values as printed on the notice. Do not tidy spelling or expand abbreviations.
2. `close_date` as `YYYY-MM-DD`, date only.
3. A field that is not on the notice is left empty.
4. `category` and `region`: the notice's own label. Several values are joined with `; ` in alphabetical order.
5. `contact_name`: the person's name only. No job title, email or phone.
