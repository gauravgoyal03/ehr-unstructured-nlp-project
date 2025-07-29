import medspacy
from medspacy.ner import TargetMatcher
from medspacy.target_matcher import TargetRule
import pandas as pd

# === Initialize medspaCy NLP pipeline ===
nlp = medspacy.load()

# === Define custom clinical entity rules ===
target_matcher = TargetMatcher(nlp)
rules = [
    TargetRule("warfarin", "MEDICATION"),
    TargetRule("INR", "LAB_TEST"),
    TargetRule("5mg", "DOSAGE"),
    TargetRule("daily", "FREQUENCY"),
    TargetRule("patient", "PERSON"),
]

# Add rules to matcher and insert into pipeline
target_matcher.add(rules)
nlp.add_pipe(target_matcher, last=True)

# === Load de-identified clinical notes ===
CSV_PATH = "data/deidentified/deidentified_notes.csv"
df = pd.read_csv(CSV_PATH)

# Select a sample of notes to test (adjust count as needed)
sample_notes = df["deidentified_note"].dropna().tolist()[:5]

# === Run entity extraction ===
for idx, note in enumerate(sample_notes):
    doc = nlp(note)
    print(f"\nEntities in Note {idx+1}:")
    if doc.ents:
        for ent in doc.ents:
            print(f" - {ent.text} ({ent.label_})")
    else:
        print("No entities found.")