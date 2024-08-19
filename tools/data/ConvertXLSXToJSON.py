# Convert the hazard_definitions.xlsx file to a JSON file
import pandas as pd

hazard_df = pd.read_excel("data/hazard_definitions.xlsx")
hazard_df.to_json("data/hazard_definitions.json", orient="records", index=False)
