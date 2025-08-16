# Exact mappings for user interest
USER_INTEREST_MAP = {
    "Interested": "interested",
    "Not Interested": "not interested",
    "On Hold": "on hold",
}

# Escalated mapping from CSV to boolean
ESCALATED_MAP = {
    "Yes": True,
    "No": False,
}

# Lead source / user source mapping
USER_SOURCE_MAP = {
    "Referral": "Referral",
    "No Broker": "No Broker",
    "LinkedIn": "LinkedIn",
    "Society Camp": "Society Campaign",
    "ACN": "ACN",
}

# Communication / last call status mapping
CALL_STATUS_MAP = {
    "Connected": "connected",
    "Requested Callback": "requested callback",
    "RNR 1": "rnr1",
    "RNR 2": "rnr2",
    "RNR 3": "rnr3",
    "RNR 4": "rnr4",
    "Not Connected": "not connected",
}

# Blocker reasons mapping (optional for service-level, included for reference)
BLOCK_REASONS = [
    'Draft not visible on BBMP portal',
    'Incorrect draft name',
    'Draft already in use for another application',
    'Draft mapped to a different property',
    'Wrong assessment number on draft',
    'Property tax not paid',
    'SAS ID not available',
    'SAS ID application still in process',
    'SAS ID held by builder',
    'Sale deed not registered',
    'Shared sale deed already used',
    'Shared sale deed not yet used',
    'Multiple properties on same sale deed',
    'Co-owner unavailable (deceased)',
    'Aadhar not linked to phone number',
    'Aadhar OTP not accessible (user abroad)',
    'Converted land – extra documents required',
    'Loan certificate number required',
    'Case stuck at Revenue Office',
    'Property under Panchayat jurisdiction',
]

# Service names (for reference, user mapping uses serviceIds from these)
SERVICE_NAMES = [
    'E-Khata', 'Bescom', 'Khata Transfer', 'E-E (Electronic Transfer)',
    'Sale Deed Drafting', 'Release Deed Drafting', 'Rental Agreement',
    'Will Deed Drafting', 'Agreement to Sale Drafting', 'POA Drafting',
    'MODT Removal', 'Affidavit Drafting', 'Registry at SRO', 'Family Tree Drafting'
]

# Service status options (for reference, service-level mapping)
SERVICE_STATUS_MAP = {
    "Open": "open",
    "Pause": "paused",
    "Lost": "lost",
}


# Service stages mapping (for reference)
SERVICE_STAGE_MAP = {
    "Doc": "Doc",
    "Filing": "Filing",
    "Awaiting": "Awaiting",
    "Correction": "Correction",
    "To Close": "To Close",
}

# Sub-stage mapping per stage (service-level, for reference)
SUB_STAGE_MAP = {
    "Doc": ["To Validate", "Incomplete", "Blocked", "Verified"],
    "Filing": ["In Queue", "In Process", "Blocked", "Submitted"],
    "Awaiting": ["Awaiting", "Re-Apply", "Blocked", "Approved"],
    "Correction": ["Verifying", "To Correct", "Cancelled", "Completed"],
    "To Close": ["Doc Shared", "Invoiced", "Paid"],
}
