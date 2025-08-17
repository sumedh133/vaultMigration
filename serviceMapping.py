from helpers import excelTimestampToUnix, format_phone_number
from exactWordMappings import SUB_STAGE_MAP

service_column_mapping = {
    "serviceId": lambda row, user: row["_service_id_allocated"],
    "serviceName": lambda row, user: row.get("Services", ""),
    "userId": lambda row, user: user["userId"],
    "userName": lambda row, user: user["userName"],
    "phoneNumber": lambda row, user: format_phone_number(user["phoneNumber"]),
    "serviceSource": lambda row, user: row.get("Lead Source", ""),

    # 👤 Agent Info
    "agentName": lambda row, user: row.get("Acquisition POC", ""),
    "acquisitionPOC": lambda row, user: row.get("Acquisition POC", ""),
    "serviceSalesPOC": lambda row, user: row.get("Sales PoC", ""),
    "servicePOC": lambda row, user: row.get("Service PoC", ""),
    "blockerPOC": lambda row, user: row.get("Blocker POC", ""),

    # 🔄 Lifecycle & Status
    "lifecycle": lambda row, user: "lead",
    "serviceStatus": lambda row, user: row.get("Status", "open").strip().lower(),
    "serviceStage": lambda row, user: (
        row.get("Service Stage", "").strip().lower() or "unqualified"
    ),

    "subStage": lambda row, user: (
        "" if (row.get("Service Stage", "").strip().lower() in ["qualified", "unqualified"])
        else (
            (lambda stage, sub: (
                sub if sub and sub in SUB_STAGE_MAP.get(stage, [])
                else (SUB_STAGE_MAP[stage][0] if stage in SUB_STAGE_MAP else "")
            ))(
                row.get("Service Stage", "").strip().lower(),
                row.get("Substage", "").strip()
            )
        )
    ),
    "escalated": lambda row, user: str(row.get("Escalated", "")).strip().lower() == "yes",
    "priority": lambda row, user: False,

    # 📞 Contact Result Tracking
    "callStatus": lambda row, user: row.get("Communication Level Status", ""),
    "ASLC": lambda row, user: excelTimestampToUnix(row.get("Last Connected ")),
    "ASLA": lambda row, user: excelTimestampToUnix(row.get("Last Connected ")),

    # 📍 Address
    "addressLine1": lambda row, user: row.get("Apartment Name", ""),
    "addressLine2": lambda row, user: row.get("Unit No. (Optional but preferable)", ""),
    "addressLine3": lambda row, user: row.get("Block No. (Optional)", ""),
    "address": lambda row, user: (
        ", ".join(
            part for part in [
                row.get("Society (Area - Addrr1 1)", "").strip(),
                row.get("Addr2 - (Jurisdiction)", "").strip()
            ] if part
        )
    ),


    # 📊 Financials
    "serviceAmount": lambda row, user: int(row.get("Service Price for CRM") or 0),
    "amountPaid": lambda row, user: 0,

    # 📄 Process Tracking
    "docummentSubmissionStatus": lambda row, user: str(row.get("Document Collected", "")).strip().lower() in ["yes", "not needed"],
    "summaryEmailSentStatus": lambda row, user: False,
    "blockerReason": lambda row, user: row.get("Blocker (Reason)", "")
    if str(row.get("Blocked", "")).strip().lower() == "yes"
    else "",


    # 🔗 Associations
    "paymentIds": lambda row, user: [],

    # 📝 Notes & Communication
    "notes": lambda row, user: [],
    "communicationTasks": lambda row, user: [],

    # 📅 Timestamps
    "added": lambda row, user: excelTimestampToUnix(row.get("Date of Creation")),
    "lastModified": lambda row, user: excelTimestampToUnix(row.get("Date of Creation")),
    "completionTime": lambda row, user: None,
    "updateBy": lambda row, user: None,
}
