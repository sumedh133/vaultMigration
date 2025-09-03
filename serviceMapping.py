from helpers import excelTimestampToUnix, format_phone_number
from exactWordMappings import (
    POC_MAP,
    CALL_STATUS_MAP,
    USER_SOURCE_MAP,
    SERVICE_STAGE_MAP,
    SERVICE_STATUS_MAP,
    SUB_STAGE_MAP,
)
import random


def safe_str(val):
    """Convert value to string and strip whitespace safely."""
    if val is None:
        return ""
    return str(val).strip()

def generate_bucket_transitions(row):
    """Fill all buckets with the same enteredAt timestamp from Date column."""
    ts = excelTimestampToUnix(row.get("Date"))
    buckets = ["pre active", "active", "blocked", "closed", "archived"]
    return [{"bucket": bucket, "enteredAt": ts} for bucket in buckets]



def map_service_stage_status(row):
    stage = safe_str(row.get("Service Stage", ""))
    substage = safe_str(row.get("Sub Stage", ""))

    # Special case: Duplicate + Terminated
    if stage == "Duplicate" and substage == "Terminated":
        return {
            "serviceStatus": "lost",
            "serviceStage": "unqualified",
            "subStage": ""
        }

    # Normal mapping
    return {
        "serviceStatus": SERVICE_STATUS_MAP.get(safe_str(row.get("Status", "Open")), safe_str(row.get("Status", "Open"))),
        "serviceStage": SERVICE_STAGE_MAP.get(stage, "unqualified"),
        "subStage": "" if stage.lower() in ["qualified", "unqualified"] else (
            SUB_STAGE_MAP.get(stage.title(), [""])[0]
            if substage.title() not in SUB_STAGE_MAP.get(stage.title(), [])
            else substage.title()
        )
    }


service_column_mapping = {
    "serviceId": lambda row, user: row["_service_id_allocated"],
    "serviceName": lambda row, user: safe_str(row.get("Services", "")),
    "userId": lambda row, user: user["userId"],
    "userName": lambda row, user: user["userName"],
    "phoneNumber": lambda row, user: format_phone_number(user["phoneNumber"]),

    "serviceSource": lambda row, user: USER_SOURCE_MAP.get(
        safe_str(row.get("Lead Source", "")), safe_str(
            row.get("Lead Source", ""))
    ),

    # 👤 Agent Info
    "agentName": lambda row, user: POC_MAP.get(safe_str(row.get("Acquisition POC", "")), safe_str(row.get("Acquisition POC", ""))),
    "acquisitionPOC": lambda row, user: POC_MAP.get(safe_str(row.get("Acquisition POC", "")), safe_str(row.get("Acquisition POC", ""))),
    "serviceSalesPOC": lambda row, user: POC_MAP.get(safe_str(row.get("Sales PoC", "")), safe_str(row.get("Sales PoC", ""))),
    "servicePOC": lambda row, user: POC_MAP.get(safe_str(row.get("Service POC", "")), safe_str(row.get("Service POC", ""))),
    "blockerPOC": lambda row, user: POC_MAP.get(safe_str(row.get("Blocker POC", "")), safe_str(row.get("Blocker POC", ""))),

    # 🔄 Lifecycle & Status
    "lifecycle": lambda row, user: "lead",
    "serviceStatus": lambda row, user: map_service_stage_status(row)["serviceStatus"],
    "serviceStage": lambda row, user: map_service_stage_status(row)["serviceStage"],
    "subStage": lambda row, user: map_service_stage_status(row)["subStage"],


    "escalated": lambda row, user: safe_str(row.get("Escalated", "")).lower() == "yes",
    "priority": lambda row, user: False,

    # 📞 Contact Result Tracking
    "callStatus": lambda row, user: CALL_STATUS_MAP.get(safe_str(row.get("Communication Level Status", "")), safe_str(row.get("Communication Level Status", ""))),
    "ASLC": lambda row, user: excelTimestampToUnix(row.get("Date")),
    "ASLA": lambda row, user: excelTimestampToUnix(row.get("Date")),

    # 📍 Address
    "addressLine1": lambda row, user: safe_str(row.get("Society Name", "")) or f"Apartment-{random.randint(1000, 9999)}",
    "addressLine2": lambda row, user: safe_str(row.get("Unit No. (Optional but preferable)", "")),
    "addressLine3": lambda row, user: safe_str(row.get("Block No. (Optional)", "")),
    "address": lambda row, user: safe_str(row.get("Society Name", "")) or f"Apartment-{random.randint(1000, 9999)}",
    # "address": lambda row, user: ", ".join(
    #     part for part in [
    #         safe_str(row.get("Society (Area - Addrr1 1)", ""))
    #         # safe_str(row.get("Addr2 - (Jurisdiction)", ""))
    #     ] if part
    # ),

    # 📊 Financials
    "serviceAmount": lambda row, user: int(row.get("Service Price for CRM") or 0),
    "amountPaid": lambda row, user: 0,

    # 📄 Process Tracking
    "docummentSubmissionStatus": lambda row, user: safe_str(row.get("Document Collected", "")).lower() in ["yes", "not needed"],
    "summaryEmailSentStatus": lambda row, user: False,
    "blockerReason": lambda row, user: safe_str(row.get("Blocker Reason", "")) if safe_str(row.get("Blocked", "")).lower() == "yes" else "",

    # 🔗 Associations
    "paymentIds": lambda row, user: [],

    # 📝 Notes & Communication
    "notes": lambda row, user: [],
    "communicationTasks": lambda row, user: [],

    # 📅 Timestamps
    "added": lambda row, user: excelTimestampToUnix(row.get("Date")),
    "lastModified": lambda row, user: excelTimestampToUnix(row.get("Date")),
    "appliedDate": lambda row, user: excelTimestampToUnix(row.get("Applied Date")),
    "bucketTransitions": lambda row, user: generate_bucket_transitions(row),
    "completionTime": lambda row, user: None,
    
    "updateBy": lambda row, user: None,
}
