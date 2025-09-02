import pandas as pd

# Load your Excel file
df = pd.read_excel("Vault Data for migration Input from Team.xlsx")

# List the columns you want to check
columns_to_check = [
    "Services",
    "Lead Source",
    "Status",
    "Communication Level Status",
    "Service Stage",
    "Substage",
    "Blocked",
    "Sales PoC",
    "Acquisition POC",
    "Service PoC",
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
