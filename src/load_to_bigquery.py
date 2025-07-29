# src/load_to_bigquery.py

import pandas as pd
from pandas_gbq import to_gbq

# Constants
INPUT_FILE = "data/deidentified/deidentified_notes.csv"
PROJECT_ID = "ehr-unstructured-nlp-project"
DATASET = "ehr_pipeline"
TABLE = "deidentified_notes"
DESTINATION = f"{DATASET}.{TABLE}"

# Load de-identified notes from CSV
print(f"Reading from {INPUT_FILE}...")
df = pd.read_csv(INPUT_FILE)

# Upload the DataFrame to BigQuery table
print(f"Uploading {len(df)} rows to BigQuery table {DESTINATION}...")
to_gbq(df, DESTINATION, project_id=PROJECT_ID, if_exists="replace")

print("Upload complete.")
