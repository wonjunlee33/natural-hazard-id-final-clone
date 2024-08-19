"""
This module picks data from the disaster_data_500_ea.xlsx such that each Hazard has equal 
representation in the dataset
"""

import pandas as pd
import numpy as np

# Load the dataset
reports_df = pd.read_excel("data/disaster_data_500_ea.xlsx")
print(reports_df["UNDRR Categories"])

# Get the unique hazards
hazards = np.unique(reports_df["UNDRR Categories"])
print(hazards)

# Get the number of reports for each hazard
hazard_counts = reports_df["UNDRR Categories"].value_counts()
print(hazard_counts)

# Get the minimum number of reports for each hazard
min_count = 400
print(min_count)

# Get rows such that each hazard has 400 reports, accounting for each report has multiple hazards
rows = []
for hazard in hazards:
    rows.append(
        reports_df[reports_df["UNDRR Categories"] == hazard].sample(
            n=min_count, random_state=1, replace=True
        )
    )
print(rows)

# Concatenate the rows
balanced_df = pd.concat(rows)
print(balanced_df)

# Remove duplicates
balanced_df.drop_duplicates(inplace=True)

# Save the balanced dataset
balanced_df.to_excel("data/disaster_data_400_ea_balanced.xlsx", index=False)
