import pandas as pd
from google.cloud import dlp_v2
import os

# === File paths ===
INPUT_FILE = "data/unstructured/clinical_notes.csv"
OUTPUT_FILE = "data/deidentified/deidentified_notes.csv"

# === GCP Project ID ===
PROJECT_ID = "ehr-unstructured-nlp-project"

# === Load first 400 notes from clinical data ===
df = pd.read_csv(INPUT_FILE).head(400)

# === Initialize DLP API client ===
dlp = dlp_v2.DlpServiceClient()

# === Output storage ===
output = []

print("Starting de-identification for 400 clinical notes...")

# === Process each note individually ===
for idx, row in df.iterrows():
    note_id = row.get("note_id", idx)
    text = str(row.get("note", ""))

    try:
        # Item to be de-identified
        item = {"value": text}

        # Define types of sensitive data to detect
        inspect_config = {
            "info_types": [
                {"name": "PERSON_NAME"},
                {"name": "EMAIL_ADDRESS"},
                {"name": "PHONE_NUMBER"},
                {"name": "DATE_OF_BIRTH"}
            ],
            "include_quote": True
        }

        # Specify transformation strategy (replace with info type)
        deidentify_config = {
            "info_type_transformations": {
                "transformations": [{
                    "primitive_transformation": {
                        "replace_with_info_type_config": {}
                    }
                }]
            }
        }

        # Make de-identification request to DLP API
        response = dlp.deidentify_content(
            request={
                "parent": f"projects/{PROJECT_ID}",
                "inspect_config": inspect_config,
                "deidentify_config": deidentify_config,
                "item": item,
            }
        )

        # Store result
        output.append({
            "note_id": note_id,
            "deidentified_note": response.item.value
        })

    except Exception as e:
        print(f"Error on note_id {note_id}: {e}")

# === Save de-identified notes to CSV ===
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
pd.DataFrame(output).to_csv(OUTPUT_FILE, index=False)

print(f"De-identified notes saved to: {OUTPUT_FILE}")