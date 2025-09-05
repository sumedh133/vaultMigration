import pandas as pd

# Load your Excel file
df = pd.read_excel("Fixing phone no.xlsx", sheet_name="Corrected Merged sheet",dtype={"Primary Phone No.(Cleaned)- Main": str}).fillna("")

# List the columns you want to check
columns_to_check = [
    "Status",
]

# Print unique values for each column
for col in columns_to_check:
    if col in df.columns:
        unique_vals = df[col].dropna().unique()
        print(f"\n--- {col} ({len(unique_vals)} unique values) ---")
        for val in unique_vals:
            print(val)
    else:
        print(f"\n--- {col} not found in the sheet ---")
