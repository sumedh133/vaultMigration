import json
import os
from typing import List, Dict
from userMapping import user_column_mapping
from serviceMapping import service_column_mapping
from firebase_admin import firestore
from helpers import (
    determine_user_lifecycle,
    computeUserCounts,
    determine_bucket,
    add_service_note,
)

# Firestore client (initialized globally)
db = firestore.client()

note_columns = [
    "Contact Notes (Notes again)",
    "Comments & Next F-up Date (1st Note)",
    "BLOCKER PRIORITY ORDER (2nd Note)",
    "BESSCOM STATUS (3rd Note)",
    "BBMP STATUS (4th Note)",
    "EPID (5th Note)",
    "Reference number",
]

def build_user(row: Dict) -> Dict:
    return {field: func(row) for field, func in user_column_mapping.items()}

def build_service(row: Dict, user: Dict) -> Dict:
    service = {field: func(row, user) for field, func in service_column_mapping.items()}
    for col in note_columns:
        add_service_note(service, col, row)
    service["bucket"] = determine_bucket(service)
    return service

def aggregate_unique_addresses(services: List[Dict]) -> Dict[str, List[str]]:
    seen = set()
    addr1s, addr2s, addr3s, fulls = [], [], [], []

    for s in services:
        addr_tuple = (
            s.get("addressLine1", ""),
            s.get("addressLine2", ""),
            s.get("addressLine3", ""),
            s.get("address", ""),
        )
        if addr_tuple not in seen:
            seen.add(addr_tuple)
            addr1s.append(addr_tuple[0])
            addr2s.append(addr_tuple[1])
            addr3s.append(addr_tuple[2])
            fulls.append(addr_tuple[3])

    return {
        "addressLine1s": addr1s,
        "addressLine2s": addr2s,
        "addressLine3s": addr3s,
        "addresses": fulls,
    }

def migrateUser(batch_rows: List[Dict], save_to_file: bool = True, out_dir: str = "debug_outputs"):
    if not batch_rows:
        return None, []

    # 1️⃣ Build user
    user = build_user(batch_rows[0])

    # 2️⃣ Build services
    services = [build_service(row, user) for row in batch_rows]

    # 3️⃣ User lifecycle
    lifecycle = determine_user_lifecycle(services)
    user["lifecycle"] = lifecycle
    for s in services:
        s["lifecycle"] = lifecycle

    # 4️⃣ Counts
    counts = computeUserCounts(services)
    user.update(counts)
    user["serviceIds"] = [s["serviceId"] for s in services]

    # 5️⃣ Aggregate unique addresses
    user.update(aggregate_unique_addresses(services))

    if save_to_file:
        # Optional: save JSON locally
        os.makedirs(out_dir, exist_ok=True)
        file_path = os.path.join(out_dir, f"user_{user['userId']}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(
                {"user": user, "services": services},
                f,
                indent=4,
                ensure_ascii=False
            )
        print(f"✅ Debug JSON saved to {file_path}")
    else:
        # Push to Firebase in a single batch
        batch = db.batch()
        # Write the user
        user_ref = db.collection("vaultUsers").document(user["userId"])
        batch.set(user_ref, user)

        # Write the services to the top-level collection
        services_collection = db.collection("vaultServices")
        for service in services:
            service_ref = services_collection.document(service["serviceId"])
            batch.set(service_ref, service)

        batch.commit()
        print(f"✅ Pushed user {user['userId']} and {len(services)} services to Firebase in a single batch")


    return user, services
