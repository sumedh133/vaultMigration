import json
from typing import List, Dict
from userMapping import user_column_mapping
from serviceMapping import service_column_mapping
from helpers import (
    determine_user_lifecycle,
    computeUserCounts,
    determine_bucket,
    add_service_note,
)

note_columns = [
    "Contact Notes (Notes again)",
    "Comments & Next F-up Date (1st Note)",
    "BLOCKER PRIORITY ORDER (2nd Note)",
    "BESSCOM STATUS (3rd Note)",
    "BBMP STATUS (4th Note)",
    "EPID (5th Note)",
    "Reference number",
    "Lead ID (Passed in Notes)",
    "Notes"
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

def migrateUser(batch_rows: List[Dict], writer, db):
    """
    batch_rows: rows for a single user
    writer: Firestore BulkWriter
    db: Firestore client
    """

    if not batch_rows:
        return None, []

    # Assign pre-allocated user ID
    user_id = batch_rows[0].get("_user_id_allocated")
    if not user_id:
        raise ValueError("User ID not pre-allocated in row")

    # Build user
    user = build_user(batch_rows[0])
    user["userId"] = user_id  # override with pre-allocated ID

    # Deduplicate services by (serviceName, addressLine1)
    seen_services = set()
    services = []
    for row in batch_rows:
        service = build_service(row, user)

        # uniqueness key
        key = (service.get("serviceName", "").strip().lower(),
               service.get("addressLine2","").strip().lower(),
               service.get("addressLine1", "").strip().lower())

        if key in seen_services:
            continue  # skip duplicate
        seen_services.add(key)

        service_id = row.get("_service_id_allocated")
        if not service_id:
            raise ValueError("Service ID not pre-allocated in row")
        service["serviceId"] = service_id
        services.append(service)

    # User lifecycle
    lifecycle = determine_user_lifecycle(services)
    user["lifecycle"] = lifecycle
    for s in services:
        s["lifecycle"] = lifecycle

    # Counts
    counts = computeUserCounts(services)
    user.update(counts)
    user["serviceIds"] = [s["serviceId"] for s in services]

    # Aggregate unique addresses
    user.update(aggregate_unique_addresses(services))
    
    # ✅ Set user["added"] as the eldest service "added"
    added_timestamps = [s.get("added") for s in services if s.get("added") is not None]
    if added_timestamps:
        user["added"] = min(added_timestamps)

    # ✅ Set user["lastModified"] as the youngest service "lastModified"
    modified_timestamps = [s.get("lastModified") for s in services if s.get("lastModified") is not None]
    if modified_timestamps:
        user["lastModified"] = max(modified_timestamps)

    # Push to Firebase using BulkWriter
    user_ref = db.collection("vaultUsers").document(user["userId"])
    writer.set(user_ref, user)

    services_collection = db.collection("vaultServices")
    for service in services:
        service["userId"] = user["userId"]
        service_ref = services_collection.document(service["serviceId"])
        writer.set(service_ref, service)

    return user, services
