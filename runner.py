import pandas as pd
import firebase_admin
import os
from firebase_admin import credentials, firestore
from migrateUser import migrateUser  # updated to accept db as argument

# Initialize Firebase once
if not firebase_admin._apps:
    cred = credentials.Certificate("iqol-crm-firebase-adminsdk-fbsvc-19f803d1d1.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()


def allocate_ids(counter_doc_ref, label: str, chunk_size: int):
    """
    Pre-allocate a block of IDs in Firestore and return the list.
    IDs format: <label><prefix><count>, e.g., SRA1000
    Handles prefix rollover A->B->...->Z and count rollover 1000-9999.
    """
    counter_doc = counter_doc_ref.get()
    count = 999
    prefix = "A"
    doc_label = label

    if counter_doc.exists:
        data = counter_doc.to_dict()
        count = data.get("count", 999)
        prefix = data.get("prefix", "A")
        doc_label = data.get("label", label)

    ids = []
    final_count = count
    final_prefix = prefix

    for _ in range(chunk_size):
        new_count = final_count + 1
        if new_count > 9999:
            new_count = 1000
            if final_prefix == "Z":
                raise ValueError(f"{label} prefix limit reached (Z)")
            final_prefix = chr(ord(final_prefix) + 1)
        ids.append(f"{doc_label}{final_prefix}{new_count}")
        final_count = new_count

    # Update Firestore with the correct final count and prefix
    counter_doc_ref.update({
        "count": final_count,
        "prefix": final_prefix,
        "label": doc_label
    })

    return ids


def run_migration(xlsx_path: str, chunk_size: int = 500, checkpoint_file: str = "checkpoint.txt"):
    df = pd.read_excel(xlsx_path).fillna("")

    # Read checkpoint
    last_user_id = None
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, "r") as f:
            last_user_id = f.read().strip()

    # Filter rows to resume
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

    total_users = len(batches)
    print(f"🚀 Total users to migrate: {total_users}")

    # Counter references
    user_counter_ref = db.collection("vaultAdmin").document("lastUser")
    service_counter_ref = db.collection("vaultAdmin").document("lastService")

    # Process in chunks
    for i in range(0, total_users, chunk_size):
        chunk = batches[i:i + chunk_size]

        # Pre-allocate IDs
        user_ids = allocate_ids(user_counter_ref, "UID", len(chunk))
        service_counts = [len(user_rows) for user_rows in chunk]
        total_services_in_chunk = sum(service_counts)
        service_ids = allocate_ids(service_counter_ref, "SR", total_services_in_chunk)

        # Assign IDs to rows
        service_idx = 0
        for u_idx, user_rows in enumerate(chunk):
            for s_row in user_rows:
                s_row["_service_id_allocated"] = service_ids[service_idx]
                s_row["_user_id_allocated"] = user_ids[u_idx]
                service_idx += 1

        # Bulk write
        writer = db.bulk_writer()
        for user_rows in chunk:
            migrateUser(user_rows, writer, db)  # pass db to migrateUser
        writer.close()

        # Save checkpoint
        last_user_phone = str(chunk[-1][0].get("Contact Number - Primary", "")).strip()
        with open(checkpoint_file, "w") as f:
            f.write(last_user_phone)

        print(f"✅ Chunk {i // chunk_size + 1} committed ({len(chunk)} users, {total_services_in_chunk} services)")


if __name__ == "__main__":
    run_migration(
        "Vault Data for migration Input from Team.xlsx",
        chunk_size=200
    )
