from helpers import format_phone_number, excelTimestampToUnix

# User CSV column → Firestore User field
user_column_mapping = {
    # 🆔 Identification
    "userId": lambda row: row["_user_id_allocated"],
    "userName": lambda row: row["Name"],
    "emailAddress": lambda row: None,
    "phoneNumber": lambda row: format_phone_number(row["Contact Number - Primary"]),
    "phoneNos": lambda row: [
        {
            "number": format_phone_number(row["Contact Number - Primary"]),
            "addedOn": excelTimestampToUnix(row["Date of Creation"]),
        }
    ]
    + (
        [
            {
                "number": format_phone_number(row["Secondary No."]),
                "addedOn": excelTimestampToUnix(row["Date of Creation"]),
            }
        ]
        if row.get("Secondary No.")
        else []
    ),

    "userSource": lambda row: row.get("Lead Source", ""),

    # 📍 Addresses (keeping empty lists for now, same as you had)
    "addressLine1s": lambda row: [],
    "addressLine2s": lambda row: [],
    "addressLine3s": lambda row: [],
    "addresses": lambda row: [],

    # 👤 Agent Info
    "agentName": lambda row: row.get("Acquisition POC", ""),
    "acquisitionPOC": lambda row: row.get("Acquisition POC", ""),
    "salesPOC": lambda row: row.get("Sales PoC", ""),

    # 🔄 Lifecycle & Status
    "lifecycle": lambda row: "lead",
    "userInterest": lambda row: row.get("User Interest", ""),
    "escalated": lambda row: str(row.get("Escalated", "")).strip().lower() == "yes",
    "onHoldUntil": lambda row: None,

    # 📞 Contact Result Tracking
    "callStatus": lambda row: row.get("Communication Level Status", ""),
    "ASLC": lambda row: excelTimestampToUnix(row.get("Last Connected ")),
    "ASLA": lambda row: excelTimestampToUnix(row.get("Last Connected ")),

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
    "added": lambda row: excelTimestampToUnix(row.get("Date of Creation", "")),
    "lastModified": lambda row: excelTimestampToUnix(row.get("Date of Creation", "")),

    # 🧾 Audit / Last Update Info
    "updateBy": lambda row: None,

    # activity
    "activity": lambda row: [],
}
