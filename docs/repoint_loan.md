# Re-point run: schema_loan_application

Command (the only thing that changes between document types is the YAML file):

```bash
python -m src.extract --schema config/schema_loan_application.yaml
```

3 documents processed. First record, trimmed to value and confidence:

```json
{
  "doc_id": "LOAN-2026-0001",
  "schema_used": "schema_loan_application",
  "confidence_min": 1.0,
  "fields": {
    "applicant_first_name": {
      "value": "Jane",
      "confidence": 1.0
    },
    "applicant_last_name": {
      "value": "Example",
      "confidence": 1.0
    },
    "date_of_birth": {
      "value": "1990-02-14",
      "confidence": 1.0
    },
    "home_address": {
      "value": "12 Nowhere Street, Exampleton",
      "confidence": 1.0
    },
    "employer_name": {
      "value": "Example Widgets Ltd",
      "confidence": 1.0
    },
    "annual_income": {
      "value": "80000",
      "confidence": 1.0
    },
    "loan_purpose": {
      "value": "Buy a first home",
      "confidence": 1.0
    },
    "amount_to_borrow": {
      "value": "400000",
      "confidence": 1.0
    },
    "settlement_date": {
      "value": "2026-12-15",
      "confidence": 1.0
    }
  }
}
```
