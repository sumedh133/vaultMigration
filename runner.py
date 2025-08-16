import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
from migrateUser import migrateUser  # your optimized batch-write function

# Initialize Firebase once
if not firebase_admin._apps:
    cred = credentials.Certificate("iqol-crm-firebase-adminsdk-fbsvc-19f803d1d1.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()  # pass this to migrateUser if needed

def run_migration(xlsx_path: str, start_row: int = 0, end_row: int | None = None):
    # Load the Excel file into a DataFrame
    df = pd.read_excel(xlsx_path)
    df = df.fillna("")

    # Slice based on start/end rows (pandas is 0-indexed)
    if end_row is not None:
        df = df.iloc[start_row:end_row]
    else:
        df = df.iloc[start_row:]

    current_phone = None
    batch_rows = []

    for _, row in df.iterrows():
        phone = str(row.get("Contact Number - Primary", "")).strip()

        if current_phone is None or phone == current_phone:
            current_phone = phone
            batch_rows.append(row.to_dict())
        else:
            migrateUser(batch_rows)  # pushes user + services in a single Firestore batch
            current_phone = phone
            batch_rows = [row.to_dict()]

    if batch_rows:
        migrateUser(batch_rows, save_to_file=False)  # last batch

if __name__ == "__main__":
    run_migration(
        "Vault Data for migration Input from Team - AllservicedFinalScriptOutput_V1(WithoutPhoneNo).xlsx",
        start_row=110,
        end_row=112
    )
