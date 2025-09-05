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


# def excelTimestampToUnix(excel_date):
#     """
#     Convert an Excel or string date to UNIX timestamp in seconds.
#     Handles Excel serial numbers or strings in MM/DD/YYYY format.
#     Returns None for empty/invalid dates.
#     """
#     if excel_date in (None, "", "NaT"):
#         return None

#     # Excel serial number (int/float)
#     if isinstance(excel_date, (int, float)):
#         excel_start = datetime(1899, 12, 30)
#         date = excel_start + timedelta(days=excel_date)
#         return int(date.timestamp())  # seconds

#     # String in MM/DD/YYYY format
#     if isinstance(excel_date, str):
#         excel_date = excel_date.strip()
#         if not excel_date:
#             return None
#         try:
#             date = datetime.strptime(excel_date, "%m/%d/%Y")
#             return int(date.timestamp())  # seconds
#         except ValueError:
#             return None

#     # Unknown type
#     return None


def excelTimestampToUnix(excel_date):
    """
    Convert an Excel date/timestamp to UNIX timestamp in seconds.
    Handles:
    - Excel serial numbers (int/float)
    - MM/DD/YYYY format strings
    - ISO format strings (YYYY-MM-DD HH:MM:SS with optional microseconds)
    - datetime objects
    Returns None for empty/invalid dates.
    """
    if excel_date in (None, "", "NaT"):
        return None
    
    # Handle datetime objects directly
    if isinstance(excel_date, datetime):
        return int(excel_date.timestamp())
    
    # Excel serial number (int/float)
    if isinstance(excel_date, (int, float)):
        # Check for NaN specifically
        import math
        if math.isnan(excel_date):
            return None
        excel_start = datetime(1899, 12, 30)
        date = excel_start + timedelta(days=excel_date)
        return int(date.timestamp())  # seconds
    
    # String formats
    if isinstance(excel_date, str):
        excel_date = excel_date.strip()
        if not excel_date:
            return None
        
        try:
            # Try MM/DD/YYYY format first
            date = datetime.strptime(excel_date, "%m/%d/%Y")
            return int(date.timestamp())
        except ValueError:
            pass
        
        try:
            # Try ISO format with microseconds (YYYY-MM-DD HH:MM:SS.ffffff)
            date = datetime.strptime(excel_date, "%Y-%m-%d %H:%M:%S.%f")
            return int(date.timestamp())
        except ValueError:
            pass
        
        try:
            # Try ISO format without microseconds (YYYY-MM-DD HH:MM:SS)
            date = datetime.strptime(excel_date, "%Y-%m-%d %H:%M:%S")
            return int(date.timestamp())
        except ValueError:
            pass
        
        try:
            # Try date only format (YYYY-MM-DD)
            date = datetime.strptime(excel_date, "%Y-%m-%d")
            return int(date.timestamp())
        except ValueError:
            pass
        
        # If all formats fail, return None
        return None
    
    # Unknown type
    return None

def format_phone_number(number: str) -> str:
    """
    Takes a phone number (with or without country code) and returns
    a clean string in the format +<countrycode><number>, no spaces.
    If no country code is present, assumes +91 (India).
    """
    if not number:
        return ""

    number_str = str(number).strip().replace(" ", "").replace("-", "")

    # If it already has a +, keep it as is (other country codes allowed)
    if number_str.startswith("+"):
        return number_str

    # Otherwise, assume it's Indian and add +91
    return "+91" + number_str


def determine_bucket(service: dict) -> str:
    status = service.get("serviceStatus", "").strip().lower()
    stage = service.get("serviceStage", "").strip().lower()
    blocker = service.get("blockerReason", "").strip()
    # print(status,stage,blocker)

    if status == "closed":
        return "closed"

    if blocker:
        return "blocked"

    if stage in ("qualified", "unqualified"):
        return "pre active"
    
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
    
    # print(note_content)

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
