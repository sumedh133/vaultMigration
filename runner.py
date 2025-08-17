import pandas as pd
import firebase_admin
import os
from firebase_admin import credentials, firestore
from migrateUser import migrateUser  # your optimized batch-write function

# Initialize Firebase once
if not firebase_admin._apps:
    cred = credentials.Certificate("iqol-crm-firebase-adminsdk-fbsvc-19f803d1d1.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()  # pass this to migrateUser if needed

def run_migration(xlsx_path: str, chunk_size: int = 500, checkpoint_file: str = "checkpoint.txt"):
    df = pd.read_excel(xlsx_path).fillna("")
    
    # Read checkpoint
    last_user_id = None
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, "r") as f:
            last_user_id = f.read().strip()
    
    # Filter rows to resume if checkpoint exists
    if last_user_id:
        df = df[df["Contact Number - Primary"].astype(str) != last_user_id]

    # Group rows by user (based on phone)
    all_rows = df.to_dict(orient="records")
    batches = []
    current_phone = None
    batch_rows = []

    for row in all_rows:
        phone = str(row.get("Contact Number - Primary", "")).strip()
        if current_phone is None or phone == current_phone:
            current_phone = phone
            batch_rows.append(row)
        else:
            batches.append(batch_rows)
            current_phone = phone
            batch_rows = [row]
    if batch_rows:
        batches.append(batch_rows)

    # Process in chunks
    for i in range(0, len(batches), chunk_size):
        chunk = batches[i:i + chunk_size]
        writer = db.bulk_writer()
        for user_rows in chunk:
            migrateUser(user_rows, writer)
        writer.close()  # commits chunk to Firestore

        # Save checkpoint (last user's phone)
        last_user_phone = str(chunk[-1][0].get("Contact Number - Primary", "")).strip()
        with open(checkpoint_file, "w") as f:
            f.write(last_user_phone)

        print(f"✅ Chunk {i // chunk_size + 1} committed ({len(chunk)} users)")

if __name__ == "__main__":
    run_migration(
        "Vault Data for migration Input from Team - AllservicedFinalScriptOutput_V1(WithoutPhoneNo).xlsx",
        chunk_size=20
    )
