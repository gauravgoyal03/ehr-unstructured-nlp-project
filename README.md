# EHR Unstructured NLP Pipeline (GCP + AI)

This project extracts structured insights from synthetic EHR notes using de-identification and NER techniques. It demonstrates my full-stack data engineering and AI/ML skills.

## Features
- FHIR parsing and note generation
- DLP API-based de-identification
- Regex and Hugging Face NER (BERT-based)
- Outputs pushed to CSV for BigQuery ingestion

## Tech Stack
- Python, pandas, spaCy, transformers
- GCP: Cloud Storage, DLP, BigQuery, Vertex AI (planned)
- Airflow/Dagster (planned for orchestration)
- IAM roles configured via service accounts

## Key Scripts
| Script | Description |
|--------|-------------|
| `parse_fhir.py` | Parses synthetic FHIR JSONs |
| `generate_notes.py` | Constructs synthetic notes from structured data |
| `deidentify_notes.py` | Uses DLP API to redact PHI |
| `extract_entities_regex.py` | Extracts regex-based NER entities |
| `extract_entities_transformers.py` | Extracts clinical entities using BERT |

## Next Steps
- Orchestrate using Cloud Composer or Dagster
- Evaluate clinical NER models via Vertex AI Model Garden
- Deploy model APIs via Cloud Run

## GCP Security & IAM
- Secure buckets, private service endpoints
- Scoped IAM for DLP + NLP
- Uses `ehr-dlp-access@...` for fine-grained access