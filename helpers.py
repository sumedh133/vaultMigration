import datetime
from typing import Dict, Any
import time
from datetime import datetime, timedelta
import pandas as pd


def determine_user_lifecycle(services: list[dict]) -> str:
    """
    Determine the lifecycle of a user based on their services.

    Rules:
    - If at least one service has bucket 'active', user is 'customer'
    - Otherwise, user is 'lead'
    """
    for service in services:
        if service.get('bucket') != 'pre active':
            return 'customer'
    return 'lead'


def computeUserCounts(services: list) -> dict:
    import pprint

    # Initialize all counts to 0
    counts = {
        "numberOfServices": 0,
        "activeSr": 0,
        "pausedSr": 0,
        "dependencySr": 0,
        "blockedSr": 0,
        "preActiveSr": 0,
        "closedSr": 0,
        "archivedSr": 0,
        "prioritySr": 0,
        "docSubmittedSr": 0,
        "qualifiedCount": 0,
        "unqualifiedCount": 0
    }

    counts["numberOfServices"] = len(services)

    for idx, s in enumerate(services, start=1):
        # Safe casting + debug
        bucket = s.get("bucket")
        service_status = s.get("serviceStatus")
        stage = s.get("serviceStage")
        priority = s.get("priority", False)
        doc_submitted = s.get("docummentSubmissionStatus", False)

        # Debug unexpected types
        if not isinstance(bucket, str) and bucket is not None:
            print(
                f"[DEBUG] Service #{idx} has non-string bucket: {bucket} ({type(bucket)})")
        if not isinstance(service_status, str) and service_status is not None:
            print(
                f"[DEBUG] Service #{idx} has non-string serviceStatus: {service_status} ({type(service_status)})")
        if not isinstance(stage, str) and stage is not None:
            print(
                f"[DEBUG] Service #{idx} has non-string serviceStage: {stage} ({type(stage)})")
        if not isinstance(priority, bool):
            print(
                f"[DEBUG] Service #{idx} has non-bool priority: {priority} ({type(priority)})")
        if not isinstance(doc_submitted, bool):
            print(
                f"[DEBUG] Service #{idx} has non-bool docummentSubmissionStatus: {doc_submitted} ({type(doc_submitted)})")

        # Safe normalization
        bucket = str(bucket or "").lower()
        service_status = str(service_status or "").lower()
        stage = str(stage or "").lower()
        priority = bool(priority)
        doc_submitted = bool(doc_submitted)

        # Counting logic
        if bucket == "active":
            counts["activeSr"] += 1
        if service_status == "paused":
            counts["pausedSr"] += 1
        if bucket == "blocked":
            counts["blockedSr"] += 1
        if bucket == "pre active":
            counts["preActiveSr"] += 1
        if bucket == "closed" or service_status == "closed":
            counts["closedSr"] += 1
        if bucket == "archived":
            counts["archivedSr"] += 1
        if priority:
            counts["prioritySr"] += 1
        if doc_submitted:
            counts["docSubmittedSr"] += 1
        if stage == "qualified":
            counts["qualifiedCount"] += 1
        if stage == "unqualified":
            counts["unqualifiedCount"] += 1

    return counts


def excelTimestampToUnix(excel_date):
    """
    Convert an Excel or string date to UNIX timestamp in seconds.
    Handles Excel serial numbers or strings in MM/DD/YYYY format.
    Returns None for empty/invalid dates.
    """
    if excel_date in (None, "", "NaT"):
        return None

    # Excel serial number (int/float)
    if isinstance(excel_date, (int, float)):
        excel_start = datetime(1899, 12, 30)
        date = excel_start + timedelta(days=excel_date)
        return int(date.timestamp())  # seconds

    # String in MM/DD/YYYY format
    if isinstance(excel_date, str):
        excel_date = excel_date.strip()
        if not excel_date:
            return None
        try:
            date = datetime.strptime(excel_date, "%m/%d/%Y")
            return int(date.timestamp())  # seconds
        except ValueError:
            return None

    # Unknown type
    return None
def format_phone_number(number) -> str:
    """
    Takes an Excel phone number (with country code) and returns
    a clean string in the format +<countrycode><number>, no spaces.
    """
    if not number:
        return ""
    number_str = str(number).replace(" ", "").replace("-", "")
    if not number_str.startswith("+"):
        number_str = "+" + number_str
    return number_str


def determine_bucket(service: dict) -> str:
    status = service.get("serviceStatus", "").strip().lower()
    stage = service.get("stage", "").strip().lower()
    blocker = service.get("blockerReason", "").strip()

    if status == "closed":
        return "closed"
    elif blocker:
        return "blocked"
    elif stage in ("qualified", "unqualified"):
        return "pre active"
    else:
        return "active"


def add_service_note(service: Dict[str, Any], column_name: str, row: Dict[str, Any]):
    """
    Adds a note to the service's notes array if the column has content.

    - noteId: len(service['notes']) + 1
    - noteEntryDateTime: current unix timestamp (seconds)
    - agentName: acquisitionPOC from service
    - type: "general note"
    """
    note_content = row.get(column_name)

    # 🚫 Skip if NaN or empty string
    if note_content is None or pd.isna(note_content):
        return

    note_content = str(note_content).strip()
    if not note_content:
        return

    note_entry = {
        "noteContent": note_content,
        "noteEntryDateTime": int(time.time()),
        "noteId": len(service.get("notes", [])) + 1,
        "agentName": service.get("acquisitionPOC", ""),
        "type": "general note"
    }

    if "notes" not in service or service["notes"] is None:
        service["notes"] = []

    service["notes"].append(note_entry)
