from helpers import format_phone_number, excelTimestampToUnix
from exactWordMappings import POC_MAP, CALL_STATUS_MAP, USER_SOURCE_MAP


def safe_str(val):
    """Convert value to string safely and strip whitespace."""
    if val is None:
        return ""
    return str(val).strip()


user_column_mapping = {
    # 🆔 Identification
    "userId": lambda row: row["_user_id_allocated"],
    "userName": lambda row: safe_str(row.get("Name", "")) or "Unnamed",
    "emailAddress": lambda row: None,
    "phoneNumber": lambda row: format_phone_number(row.get("Primary Phone No.(Cleaned)- Main", "")) or "0000000000",
    "phoneNos": lambda row: [
        {
            "number": format_phone_number(row.get("Primary Phone No.(Cleaned)- Main", "")) or "0000000000",
            "addedOn": excelTimestampToUnix(row.get("Date")),
        }
    ] + (
        [
            {
                "number": format_phone_number(row.get("Secondary No.", "")),
                "addedOn": excelTimestampToUnix(row.get("Date")),
            }
        ]
        if row.get("Secondary No.")
        else []
    ),


    # 📍 Addresses
    "addressLine1s": lambda row: [],
    "addressLine2s": lambda row: [],
    "addressLine3s": lambda row: [],
    "addresses": lambda row: [],

    # 👤 Agent Info (applied POC_MAP)
    "agentName": lambda row: POC_MAP.get(safe_str(row.get("Acquisition POC", "")), safe_str(row.get("Acquisition POC", ""))),
    "acquisitionPOC": lambda row: POC_MAP.get(safe_str(row.get("Acquisition POC", "")), safe_str(row.get("Acquisition POC", ""))),
    "salesPOC": lambda row: POC_MAP.get(safe_str(row.get("Sales PoC", "")), safe_str(row.get("Sales PoC", ""))),

    # 🔄 Lifecycle & Status
    "lifecycle": lambda row: "lead",
    "userInterest": lambda row: "interested",
    "escalated": lambda row: safe_str(row.get("Escalated", "")).lower() == "yes",
    "onHoldUntil": lambda row: None,

    # 📞 Contact Result Tracking (applied CALL_STATUS_MAP)
    "callStatus": lambda row: CALL_STATUS_MAP.get(
        safe_str(row.get("Communication Level Status", "")),
        safe_str(row.get("Communication Level Status", ""))
    ),
    "ASLC": lambda row: excelTimestampToUnix(row.get("Date")),
    "ASLA": lambda row: excelTimestampToUnix(row.get("Date")),

    # 📊 Counters & Metrics
    "numberOfServices": lambda row: 0,
    "activeSr": lambda row: 0,
    "pausedSr": lambda row: 0,
    "dependencySr": lambda row: 0,
    "blockedSr": lambda row: 0,
    "preActiveSr": lambda row: 0,
    "closedSr": lambda row: 0,
    "archivedSr": lambda row: 0,
    "prioritySr": lambda row: 0,
    "docSubmittedSr": lambda row: 0,
    "qualifiedCount": lambda row: 0,
    "unqualifiedCount": lambda row: 0,
    "totalPaidAmount": lambda row: 0,

    # 🔗 Associations
    "serviceIds": lambda row: [],
    "paymentIds": lambda row: [],

    # 📝 Notes
    "notes": lambda row: [],

    # 📅 Timestamps
    "added": lambda row: excelTimestampToUnix(row.get("Date")),
    "lastModified": lambda row: excelTimestampToUnix(row.get("Date")),

    # 🧾 Audit / Last Update Info
    "updateBy": lambda row: None,

    # activity
    "activity": lambda row: [],

    # 🌐 User Source (applied USER_SOURCE_MAP)
    "userSource": lambda row: USER_SOURCE_MAP.get(
        safe_str(row.get("Lead Source", "")), safe_str(
            row.get("Lead Source", ""))
    ),
}
