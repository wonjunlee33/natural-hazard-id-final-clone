"""
Extract Hazards and Synonyms from DOCX File

This script reads a DOCX file containing hazard information, extracts hazards and their synonyms,
and saves the data to a CSV file.
"""

import pandas as pd
import docx

# Read the docx file
doc = docx.Document("hips.docx")

hazards_and_synonyms = []

current_hazard = ""
synonym, name = False, False
for para in doc.paragraphs:
    if name is True and len(para.text) != 0:
        current_hazard = para.text.split("/")[-1].strip()
        name = False
    if synonym and not ("Synonyms" in para.text):
        # Add to list only if synonyms are present
        hazards_and_synonyms.append((current_hazard, para.text))
        synonym = False
    if para.text.startswith(("MH0", "ET0", "GH0", "EN0", "CH0", "BI0", "TL0", "SO0")):
        # Extract and clean hazard name
        current_hazard = para.text.split("/")[-1].strip()
        name = True
    elif "Synonyms" in para.text or "Synonym" in para.text:
        # Extract synonyms
        synonym = True

# Create a dataframe, and store into a CSV file
df = pd.DataFrame(hazards_and_synonyms, columns=["Hazard", "Synonyms"])
df.to_csv("data/hazards_and_synonyms.csv", index=False, encoding="utf-8")
