# firestore_types.py
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Union

# -------------------
# Supporting Types
# -------------------
@dataclass
class NoteEntry:
    noteContent: str
    noteEntryDateTime: int
    agentName: str
    noteId: Optional[str] = None
    type: Optional[str] = None

@dataclass
class Activity:
    id: Optional[int] = None
    time: int = 0
    user: str = ""
    action: str = ""
    target: Optional[str] = None
    note: Optional[str] = None
    from_field: Optional[str] = None  # renamed from 'from' to avoid keyword
    to: Optional[str] = None
    changes: Optional[str] = None
    status: Optional[str] = None
    serviceId: Optional[str] = None
    label: Optional[str] = None
    details: Optional[List[str]] = field(default_factory=list)

@dataclass
class PhoneRecord:
    number: str
    addedOn: int

@dataclass
class PauseMetadata:
    pausedUntil: Optional[int] = None
    pausedBy: Optional[str] = None
    dueToDependency: Optional[bool] = None
    dependencyServiceId: Optional[str] = None

@dataclass
class CommunicationTask:
    taskId: str
    srId: str
    title: str
    detail: str
    message: str
    status: str  # 'pending' | 'done'
    assignedTo: str
    createdAt: int
    dueDate: int
    triggerEvent: str

@dataclass
class Payment:
    paymentId: str
    userId: str
    serviceId: str
    transactionId: Optional[str]
    paymentType: str
    paymentAmount: float
    serviceAmount: float
    paymentMethod: Optional[str]
    paymentStatus: str
    paymentDate: Optional[int]
    dueDate: Optional[int]
    notes: Optional[NoteEntry] = None
    added: int = 0
    isDeleted: Optional[bool] = False
    agentName: Optional[str] = None

# -------------------
# Main Firestore Types
# -------------------
@dataclass
class Service:
    serviceId: str
    serviceName: str
    userId: str
    userName: str
    phoneNumber: str
    serviceSource: str = ""
    agentName: str = ""
    acquisitionPOC: str = ""
    serviceSalesPOC: str = ""
    servicePOC: Optional[str] = None
    blockerPOC: Optional[str] = None
    lifecycle: str = "lead"
    bucket: str = "pre active"  # 'pre active' | 'active' | 'blocked' | 'closed' | 'archived'
    serviceStatus: str = ""
    serviceStage: str = ""
    subStage: str = ""
    escalated: bool = False
    priority: bool = False
    pauseMetadata: Optional[PauseMetadata] = None
    onHoldUntil: Optional[int] = None
    callStatus: str = ""
    ASLC: int = 0
    ASLA: int = 0
    addressLine1: str = ""
    addressLine2: str = ""
    addressLine3: str = ""
    address: Optional[str] = None
    serviceAmount: float = 0
    amountPaid: float = 0
    docummentSubmissionStatus: bool = False
    summaryEmailSentStatus: bool = False
    blockerReason: str = ""
    paymentIds: List[str] = field(default_factory=list)
    notes: List[NoteEntry] = field(default_factory=list)
    communicationTasks: List[CommunicationTask] = field(default_factory=list)
    added: int = 0
    lastModified: int = 0
    completionTime: Optional[int] = None
    updateBy: Optional[Dict[str, Union[str, bool]]] = None

@dataclass
class User:
    userId: str
    userName: str
    emailAddress: Optional[str]
    phoneNumber: str
    phoneNos: List[PhoneRecord] = field(default_factory=list)
    userSource: str = ""
    addressLine1s: List[str] = field(default_factory=list)
    addressLine2s: List[str] = field(default_factory=list)
    addressLine3s: List[str] = field(default_factory=list)
    agentName: str = ""
    acquisitionPOC: str = ""
    salesPOC: str = ""
    lifecycle: str = "lead"
    userInterest: str = ""
    escalated: bool = False
    onHoldUntil: Optional[int] = None
    callStatus: str = ""
    ASLC: int = 0
    ASLA: int = 0
    numberOfServices: int = 0
    activeSr: Optional[int] = None
    pausedSr: Optional[int] = None
    dependencySr: Optional[int] = None
    blockedSr: Optional[int] = None
    preActiveSr: int = 0
    closedSr: Optional[int] = None
    archivedSr: Optional[int] = None
    prioritySr: int = 0
    docSubmittedSr: int = 0
    qualifiedCount: Optional[int] = None
    unqualifiedCount: int = 0
    totalPaidAmount: float = 0
    serviceIds: List[str] = field(default_factory=list)
    paymentIds: Optional[List[str]] = None
    notes: List[NoteEntry] = field(default_factory=list)
    added: int = 0
    lastModified: int = 0
    updateBy: Optional[Dict[str, str]] = None
    address: Optional[str] = None
    activity: List[Activity] = field(default_factory=list)
