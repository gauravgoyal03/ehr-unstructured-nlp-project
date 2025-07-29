import pandas as pd
import os
import random
from datetime import datetime
from tqdm import tqdm

# Define input/output paths
DATA_DIR = "data/structured"
OUTPUT_DIR = "data/unstructured"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load structured patient-related CSV files
patients_df = pd.read_csv(os.path.join(DATA_DIR, "patients.csv"))
conditions_df = pd.read_csv(os.path.join(DATA_DIR, "conditions.csv"))
medications_df = pd.read_csv(os.path.join(DATA_DIR, "medications.csv"))
observations_df = pd.read_csv(os.path.join(DATA_DIR, "observations.csv"))
encounters_df = pd.read_csv(os.path.join(DATA_DIR, "encounters.csv"))

# Helper: extract patient ID from FHIR-style reference string
def extract_patient_id(ref):
    return ref.split("/")[-1] if isinstance(ref, str) else "unknown"

# Standardize patient ID references in subject-based tables
for df in [conditions_df, medications_df, observations_df, encounters_df]:
    if "subject" in df.columns:
        df["patient_id"] = df["subject"].apply(extract_patient_id)

# Get unique patient IDs
patient_ids = set(patients_df["id"])
notes = []

print("Generating synthetic clinical notes...")
for patient_id in tqdm(list(patient_ids)[:5000]):  # Sample 5000 for processing

    # Get patient metadata
    name = patients_df.loc[patients_df["id"] == patient_id, "name"].values[0]
    birth = patients_df.loc[patients_df["id"] == patient_id, "birthDate"].values[0]

    # Filter rows related to current patient
    patient_conditions = conditions_df[conditions_df["patient_id"] == patient_id]
    patient_meds = medications_df[medications_df["patient_id"] == patient_id]
    patient_obs = observations_df[observations_df["patient_id"] == patient_id]

    # Format condition and medication strings
    condition_text = "; ".join(patient_conditions["code"].dropna().unique()[:5])
    med_text = "; ".join(patient_meds["medication"].dropna().unique()[:5])

    # Format observation records (first 5)
    obs_records = patient_obs.dropna(subset=["type", "value"])
    obs_text = "; ".join(
        f"{row['type']} = {row['value']} {row['unit']}"
        for _, row in obs_records.head(5).iterrows()
    )

    # Build the clinical note text
    note = f"""Patient Name: {name}
DOB: {birth}

Chief Complaints / Conditions:
{condition_text or "No known conditions"}

Prescribed Medications:
{med_text or "No medications prescribed"}

Recent Observations:
{obs_text or "No vitals recorded"}

Note generated on: {datetime.today().strftime('%Y-%m-%d')}
"""
    notes.append({"patient_id": patient_id, "note": note})

# Save notes to CSV
notes_df = pd.DataFrame(notes)
notes_df.to_csv(os.path.join(OUTPUT_DIR, "clinical_notes.csv"), index=False)

print("Synthetic clinical notes generated and saved to:")
print(f"   → {os.path.join(OUTPUT_DIR, 'clinical_notes.csv')}")