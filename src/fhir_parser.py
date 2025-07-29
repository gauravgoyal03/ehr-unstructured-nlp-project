import os
import json
import pandas as pd

# Directory containing FHIR JSON files
FHIR_DIR = "data/fhir"

# Lists to collect structured data
patients, conditions, medications, observations, encounters = [], [], [], [], []

# Recursively walk through FHIR directory to read all JSON files
for root, _, files in os.walk(FHIR_DIR):
    for filename in files:
        if filename.endswith(".json"):
            filepath = os.path.join(root, filename)
            with open(filepath, "r") as f:
                try:
                    bundle = json.load(f)

                    # Ensure it's a FHIR Bundle with entries
                    if bundle.get("resourceType") == "Bundle" and "entry" in bundle:
                        for entry in bundle["entry"]:
                            resource = entry.get("resource", {})
                            resource_type = resource.get("resourceType")

                            # Extract relevant fields based on resource type
                            if resource_type == "Patient":
                                patients.append({
                                    "id": resource.get("id"),
                                    "name": resource.get("name", [{}])[0].get("text", f"Patient-{resource.get('id')}"),
                                    "gender": resource.get("gender", "unknown"),
                                    "birthDate": resource.get("birthDate", "unknown")
                                })

                            elif resource_type == "Condition":
                                conditions.append({
                                    "id": resource.get("id"),
                                    "subject": resource.get("subject", {}).get("reference", "unknown"),
                                    "code": resource.get("code", {}).get("text", "unspecified"),
                                    "onsetDateTime": resource.get("onsetDateTime", "unknown")
                                })

                            elif resource_type == "MedicationRequest":
                                medications.append({
                                    "id": resource.get("id"),
                                    "subject": resource.get("subject", {}).get("reference", "unknown"),
                                    "medication": resource.get("medicationCodeableConcept", {}).get("text", "unspecified"),
                                    "authoredOn": resource.get("authoredOn", "unknown")
                                })

                            elif resource_type == "Observation":
                                observations.append({
                                    "id": resource.get("id"),
                                    "subject": resource.get("subject", {}).get("reference", "unknown"),
                                    "type": resource.get("code", {}).get("text", "unspecified"),
                                    "value": resource.get("valueQuantity", {}).get("value", ""),
                                    "unit": resource.get("valueQuantity", {}).get("unit", "")
                                })

                            elif resource_type == "Encounter":
                                encounters.append({
                                    "id": resource.get("id"),
                                    "subject": resource.get("subject", {}).get("reference", "unknown"),
                                    "type": resource.get("type", [{}])[0].get("text", "unspecified"),
                                    "reason": resource.get("reasonCode", [{}])[0].get("text", "unspecified"),
                                    "period": resource.get("period", {}).get("start", "unknown")
                                })

                except Exception as e:
                    print(f"Error processing {filename}: {e}")

# Save structured outputs as CSV
os.makedirs("data/structured", exist_ok=True)
pd.DataFrame(patients).to_csv("data/structured/patients.csv", index=False)
pd.DataFrame(conditions).to_csv("data/structured/conditions.csv", index=False)
pd.DataFrame(medications).to_csv("data/structured/medications.csv", index=False)
pd.DataFrame(observations).to_csv("data/structured/observations.csv", index=False)
pd.DataFrame(encounters).to_csv("data/structured/encounters.csv", index=False)

# Summary of extracted records
print("Parsing complete.")
print(f"Patients: {len(patients)}")
print(f"Conditions: {len(conditions)}")
print(f"Medications: {len(medications)}")
print(f"Observations: {len(observations)}")
print(f"Encounters: {len(encounters)}")