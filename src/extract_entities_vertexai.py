import json
import pandas as pd
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# === Configuration ===
KEY_PATH = "credentials/ehr-dlp-access.json"  # Path to service account JSON key
CSV_PATH = "data/deidentified/deidentified_notes.csv"  # Input CSV file
PROJECT_ID = "ehr-unstructured-nlp-project"
LOCATION = "us-central1"
BATCH_SIZE = 5  # Number of notes to process

# === Authenticate using service account ===
creds = service_account.Credentials.from_service_account_file(KEY_PATH)
creds = creds.with_scopes(["https://www.googleapis.com/auth/cloud-platform"])
creds.refresh(Request())
access_token = creds.token

# === Vertex AI Healthcare NLP endpoint for entity analysis ===
API_URL = f"https://healthcare.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/services/nlp:analyzeEntities"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# === Load de-identified clinical notes ===
df = pd.read_csv(CSV_PATH)
notes = df["deidentified_note"].dropna().tolist()

# === Process notes in batch ===
for idx, note in enumerate(notes[:BATCH_SIZE]):
    payload = {
        "documentContent": note
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        entities = response.json().get("entities", [])
        print(f"\nEntities for Note {idx + 1}:")
        for ent in entities:
            print(f" - {ent.get('mentionText')} ({ent.get('type')})")
    else:
        print(f"\nError on Note {idx + 1}: {response.status_code}")
        print(response.text)