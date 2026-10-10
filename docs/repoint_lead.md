# Re-point run: schema_realestate_lead

Command (the only thing that changes between document types is the YAML file):

```bash
python -m src.extract --schema config/schema_realestate_lead.yaml
```

3 documents processed. First record, trimmed to value and confidence:

```json
{
  "doc_id": "LEAD-2026-0001",
  "schema_used": "schema_realestate_lead",
  "confidence_min": 1.0,
  "fields": {
    "lead_name": {
      "value": "Jane Example",
      "confidence": 1.0
    },
    "lead_email": {
      "value": "jane@example.com",
      "confidence": 1.0
    },
    "lead_phone": {
      "value": "000 000 0000",
      "confidence": 1.0
    },
    "property_of_interest": {
      "value": "12 Nowhere Street, Exampleton",
      "confidence": 1.0
    },
    "budget_nzd": {
      "value": "900000",
      "confidence": 1.0
    },
    "move_timeframe": {
      "value": "within three months",
      "confidence": 1.0
    },
    "preferred_contact": {
      "value": "phone",
      "confidence": 1.0
    }
  }
}
```
