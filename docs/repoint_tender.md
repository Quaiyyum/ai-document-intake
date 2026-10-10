# Re-point run: schema_tender

Command (the only thing that changes between document types is the YAML file):

```bash
python -m src.extract --schema config/schema_tender.yaml
```

50 documents processed. First record, trimmed to value and confidence:

```json
{
  "doc_id": "GETS-2026-0002",
  "schema_used": "schema_tender",
  "confidence_min": 1.0,
  "fields": {
    "agency": {
      "value": "New Zealand Transport Agency (Waka Kotahi) - HISTORIC",
      "confidence": 1.0
    },
    "title": {
      "value": "14247 SH3 Ashhurst Shared Use Path",
      "confidence": 1.0
    },
    "reference": {
      "value": "35111110",
      "confidence": 1.0
    },
    "close_date": {
      "value": "2026-11-12",
      "confidence": 1.0
    },
    "category": {
      "value": "72141000 - Highway and road construction services",
      "confidence": 1.0
    },
    "region": {
      "value": "Manawatu-Wanganui",
      "confidence": 1.0
    },
    "contact_name": {
      "value": "Ashley Lamont",
      "confidence": 1.0
    }
  }
}
```
