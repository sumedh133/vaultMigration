POC_MAP = {
    # flattened all POC names to match frontend
    "Rahila": "Rahila Aqueel",
    "Dheeraj": "Dheeraj",
    "Daksh": "Daksh Rupani",
    "Pranjay": "Pranjay",
    "Pratham": "Pratham Lodha",
    "Srikanth G": "Srikanth ",
    "Manas": "Manas Pandit",
    "Divesh": "Divesh",
    "Prashant": "Prashant Kumar",
    "Ashmi": "Ashmi Jain",
    "Rajib": "Rajib",
    "Sushant": "Sushant",
    "Kushagra": "Kushagra Roshan",
    "Unassigned": "Unassigned",
    "Darvin": "Darvin",
    "Ajay": "Ajay",
    "Preethi": "Preethi Maruthi Hadaginal ",
    "Rohit": "Rohit",
    "Likith": "Likith Kumar DK",
    "Yash": "Yash Rajkotia",
    "Rajnandini": "Rajnandini",
    "Inbound": "Inbound",
    "Aryan R": "Aryan R",
    "Garima Doulani": "Garima Doulani",
    "unassigned": "Unassigned",
    "Unassigned": "Unassigned",
    "":"Unassigned"
}

SERVICE_STATUS_MAP = {
    "Open": "open",
    "Paused": "paused",
    "Lost": "lost",
    "Closed": "closed",
}


SERVICE_STAGE_MAP = {
    "Doc": "Doc",
    "Filing": "Filing",
    "Awaiting": "Awaiting",
    "Correction": "Correction",
    "ToClose": "To Close",
    "Duplicate": "Duplicate",
    "Qualified": "qualified",
    "Unqualified": "unqualified",
}

CALL_STATUS_MAP = {
    "Connected": "connected",
    "Requested Callback": "requested callback",
    "RNR1": "rnr1",
    "RNR2": "rnr2",
    "RNR3": "rnr3",
    "RNR4": "rnr4",
    "Not Connected": "not connected",
}

USER_SOURCE_MAP = {
    "Referral": "Referral",
    "Online Campaign": "Online Campaign",
    "Offline Camp": "Offline Camp",
    "Inbound": "Inbound",
    "Partner - ACN": "Partner - ACN",
    "Calling": "Calling",
    "Partner": "Partner",
    "Partners": "Partners",
    "Partner - NB": "Partner - NB",
    "LinkedIn": "LinkedIn",
    "Society Camp": "Society Camp",  # include all other raw values as-is
}


SUB_STAGE_MAP = {
    "Doc": ["To Validate", "Incomplete", "Blocked", "Verified"],
    "Filing": ["In Queue", "In Process", "Blocked", "Submitted"],
    "Awaiting": ["Awaiting", "Re-Apply", "Blocked", "Approved"],
    "Correction": ["Verifying", "To Correct", "Cancelled", "Completed"],
    "Toclose": ["Doc Shared", "Invoiced", "Paid"], #changed cause data has no space
}