export interface User {
    // 🆔 Identification
    userId: string
    userName: string
    emailAddress: string | null
    phoneNumber: string //+ with country code and then phone no. with no spaces
    phoneNos?: PhoneRecord[] //array of phone numbers for this user with 1st element being phoneNumber
    userSource: string  // exact names : 
    addressLine1s: string[]     //society
    addressLine2s: string[]     //block
    addressLine3s: string[]     //unit
    addresses: string[]

    // 👤 Agent Info
    agentName: string // who added the user- person logged in when user was added- acquisitionPOC
    acquisitionPOC: string  //must be same as internal agents name
    salesPOC: string    //must   be same as internal agents name

    // 🔄 Lifecycle & Status
    lifecycle: string // exact string: lead, customer
    userInterest: string    //exact: interested, not interested, on hold
    escalated: boolean      
    onHoldUntil?: number    // unix timestamp

    // 📞 Contact Result Tracking
    callStatus: string // result of last call
    ASLC: number // last call timestamp
    ASLA: number // last answered call timestamp

    // 📊 Counters & Metrics- used for service level filters- all derived
    numberOfServices: number
    activeSr?: number
    pausedSr?: number
    dependencySr?: number
    blockedSr?: number
    preActiveSr: number
    closedSr?: number
    archivedSr?: number
    prioritySr: number
    docSubmittedSr: number
    qualifiedCount?: number
    unqualifiedCount: number

    totalPaidAmount: number // derived sum of all user payments

    // 🔗 Associations
    serviceIds: string[]
    paymentIds?: string[]

    // 📝 Notes
    notes: NoteEntry[]

    // 📅 Timestamps
    added: number
    lastModified: number

    // 🧾 Audit / Last Update Info
    updateBy?: {
        userInterest?: string
        escalated?: string
        acquisitionPOC?: string
        salesPOC?: string
    }

    activity: Activity[]
}

export interface Service {
    // 🆔 Identification
    serviceId: string
    serviceName: string // one of the service names from dropdown options
    userId: string
    userName: string
    phoneNumber: string
    serviceSource: string   // same as user source- doesnt change once given

    // 👤 Agent Info
    agentName: string   // who added the service- person logged in when created service
    acquisitionPOC: string  // exact name of internal agent
    serviceSalesPOC: string // exact name of internal agent
    servicePOC?: string // exact name of internal agent
    blockerPOC?: string // exact name of internal agent

    // 🔄 Lifecycle & Status
    lifecycle: string // exact: lead or customer
    bucket: 'pre active' | 'active' | 'blocked' | 'closed' | 'archived'
    serviceStatus: string // open, paused, lost
    serviceStage: string // unqualified, qualified, to close, etc
    subStage: string    // derived from service stage
    escalated: boolean  // true or false 
    priority: boolean  
    pauseMetadata?: PauseMetadata  //empty by def
    onHoldUntil?: number    //empty by def

    // 📞 Contact Result Tracking
    callStatus: string  // result of last call
    ASLC: number    // last call timestamp
    ASLA: number    // last answered call timestamp
    // contactResults?: contactResult[]

    // 📍 Address
    addressLine1: string
    addressLine2: string
    addressLine3: string
    address?: string        // an editable address option provided in nexus

    // 📊 Financials
    serviceAmount: number   // cost of service
    amountPaid: number      // amt paid till now for this service - 0 at start

    // 📄 Process Tracking
    docummentSubmissionStatus: boolean      
    summaryEmailSentStatus: boolean  //not needed
    blockerReason: string   //only is bucket is blocker

    // 🔗 Associations
    paymentIds: string[]

    // 📝 Notes & Communication
    // communication: CommunicationEntry[]
    notes: NoteEntry[]
    communicationTasks: CommunicationTask[]

    // 📅 Timestamps
    added: number
    lastModified: number    
    completionTime?: number // timestamp when service status became completed

    // 🧾 Audit / Last Update Info
    updateBy?: {
        serviceStatus?: string
        servicePOC?: string
        bucket?: string
        priority?: string
        serviceStage?: string
        blockerPOC?: string
        acquisitionPOC?: string
        serviceSalesPOC?: string
        docummentSubmissionStatus?: string
        escalated?: string
        substage?: string
    }
}

export interface Payment {
    // Identification
    paymentId: string
    userId: string
    serviceId: string
    transactionId: string | null

    // Payment Info
    paymentType: string
    paymentAmount: number
    serviceAmount: number
    paymentMethod: string | null

    // Status / Timing
    paymentStatus: string
    paymentDate: number | null
    dueDate: number | null

    // Notes
    notes: NoteEntry | null

    // Timestamps
    added: number

    // Flags / Admin
    isDeleted?: boolean
    agentName?: string
}

export interface CommunicationTask {
    taskId: string
    srId: string
    title: string
    detail: string
    message: string
    status: 'pending' | 'done'
    assignedTo: string
    createdAt: number
    dueDate: number
    triggerEvent: string
}

interface NoteEntry {
    noteContent: string
    noteEntryDateTime: number
    noteId?: string
    agentName: string
    type?: string
}

export interface Activity {
    id?: number
    time: number
    user: string
    action: string
    target?: string
    note?: string
    from?: string
    to?: string
    changes?: string
    status?: string
    serviceId?: string
    label?: string
    details?: string[]
}

export type PhoneRecord = {
    number: string
    addedOn: number
}

export interface PauseMetadata {
    pausedUntil?: number
    pausedBy?: string
    dueToDependency?: boolean
    dependencyServiceId?: string
}
