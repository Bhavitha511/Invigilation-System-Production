# Enhanced Allocation Logic Documentation

## Overview

The invigilation duty allocation system now includes intelligent conflict detection and manual intervention suggestions when automatic allocation cannot find suitable faculty.

## Allocation Rules (Priority Order)

### 1. Department Exclusion ✅
**Rule**: Faculty from the same department as the exam cannot invigilate their own students.

**Example**:
- Exam: CSE Department, Year 2
- ❌ CSE faculty cannot be assigned
- ✅ ECE, EEE, MECH, CIVIL faculty can be assigned

**Reason**: Prevents bias and maintains examination integrity.

---

### 2. Subject Teacher Exclusion ✅
**Rule**: The faculty member teaching the subject cannot invigilate that exam.

**Example**:
- Exam: CS201 - Database Management Systems
- Subject Teacher: Dr. John (CSE)
- ❌ Dr. John cannot be assigned (even if from different dept)
- ✅ Other faculty can be assigned

**Reason**: Teacher knows the exam content and students, creating conflict of interest.

---

### 3. Leave Status Check ✅
**Rule**: Faculty on approved leave cannot be assigned duties.

**Example**:
- Faculty: Dr. Smith
- Leave: 15 Mar 2026 - 20 Mar 2026 (Approved)
- Exam Date: 18 Mar 2026
- ❌ Dr. Smith cannot be assigned

**Reason**: Faculty is not available on campus.

---

### 4. Already Assigned Check ✅
**Rule**: Faculty cannot be assigned to multiple halls for the same exam.

**Example**:
- Exam: CS201 at 9:00 AM - 12:00 PM
- Dr. Brown already assigned to Hall A
- ❌ Dr. Brown cannot be assigned to Hall B for same exam

**Reason**: One person cannot be in two places at once.

---

### 5. Intelligent Timetable Clash Detection ✅

**Rule**: Faculty teaching during exam time creates a clash, UNLESS they're teaching the same year students who are taking the exam.

#### Scenario A: No Clash (Faculty is FREE)
```
Exam: Year 2 students, CS201, 9:00 AM - 12:00 PM
Faculty: Dr. Alice
Timetable: Teaching Year 2 students, 9:00 AM - 10:00 AM

Result: ✅ NO CLASH
Reason: Year 2 students are in the exam, so Dr. Alice's class is automatically cancelled.
        Dr. Alice is FREE and can invigilate.
```

#### Scenario B: Clash (Faculty is BUSY)
```
Exam: Year 2 students, CS201, 9:00 AM - 12:00 PM
Faculty: Dr. Bob
Timetable: Teaching Year 3 students, 9:00 AM - 10:00 AM

Result: ❌ CLASH
Reason: Year 3 students are NOT in the exam, they have regular classes.
        Dr. Bob must teach Year 3, cannot invigilate.
```

#### Scenario C: Partial Clash
```
Exam: Year 1 & 2 students, 9:00 AM - 12:00 PM
Faculty: Dr. Carol
Timetable: Teaching Year 1 students, 9:00 AM - 10:00 AM

Result: ✅ NO CLASH
Reason: Year 1 students are in the exam, class cancelled.
```

---

## Scoring & Selection

After filtering out ineligible faculty, the system scores remaining candidates:

### Proximity Score (100 points)
- **Same block as exam hall**: +100 points
- **Different block**: 0 points

**Example**:
- Exam Hall: Block A, Room 101
- Dr. Smith cabin: Block A, Room 205 → +100 points
- Dr. Jones cabin: Block B, Room 103 → 0 points

**Reason**: Reduces travel time, easier for faculty to reach exam hall quickly.

### Workload Score (Lower is Better)
- Count of current confirmed + pending assignments
- Faculty with fewer duties get priority

**Example**:
- Dr. Smith: 2 assignments → Lower priority
- Dr. Jones: 0 assignments → Higher priority

**Reason**: Distributes workload fairly across all faculty.

### Randomization
- Among faculty with same score and similar workload (±1)
- Ensures fairness and prevents bias

---

## Manual Intervention System

### When Suggestions are Created

The system creates manual intervention suggestions when:

1. **Not enough eligible faculty** to fill all required positions
2. **Faculty have timetable clashes** but could be made available

### Suggestion Types

#### 1. Timetable Clash Suggestions

**Scenario**:
```
Exam: Year 2, CS201, 9:00 AM - 12:00 PM, Hall A
Required: 2 invigilators
Eligible: 1 faculty found
Shortage: 1 invigilator needed

Faculty with Clash:
- Dr. Brown (ECE)
- Teaching Year 3 students, EC301, 9:00 AM - 10:00 AM
```

**System Creates Suggestion**:
```
Faculty: Dr. Brown (ECE)
Clash: Teaching EC301 to Year 3 at 9:00-10:00 AM

Recommended Actions:
1. Swap this class with another faculty member
2. Reschedule this class to a different time slot
3. Find a substitute teacher for this period
4. Cancel this class for the day (if possible)
```

**Admin Actions**:
- **Implement**: Assign Dr. Brown after resolving the clash
- **Review**: Mark as reviewed for later action
- **Reject**: Not feasible, find another solution

---

## Allocation Flow Diagram

```
Start Auto-Allocation
        │
        ▼
Get All Active Faculty
        │
        ▼
For Each Exam Hall:
        │
        ├─── Filter Faculty ───┐
        │                      │
        │    ┌─────────────────┴─────────────────┐
        │    │                                   │
        │    ▼                                   ▼
        │  Same Dept?                    Subject Teacher?
        │    │ Yes → Exclude                │ Yes → Exclude
        │    │ No  → Continue               │ No  → Continue
        │    │                              │
        │    ▼                              ▼
        │  On Leave?                    Already Assigned?
        │    │ Yes → Exclude                │ Yes → Exclude
        │    │ No  → Continue               │ No  → Continue
        │    │                              │
        │    └──────────┬───────────────────┘
        │               │
        │               ▼
        │        Timetable Clash?
        │               │
        │         ┌─────┴─────┐
        │         │           │
        │      Yes (Clash)  No (Free)
        │         │           │
        │         ▼           ▼
        │   Create        Add to
        │   Suggestion    Eligible List
        │         │           │
        └─────────┴───────────┘
                  │
                  ▼
            Score Eligible Faculty
            (Proximity + Workload)
                  │
                  ▼
            Randomize Among Equals
                  │
                  ▼
            Select Top N Faculty
                  │
                  ▼
            Create Assignments
                  │
                  ▼
            Send Email Notifications
                  │
                  ▼
            End
```

---

## Example Scenarios

### Scenario 1: Perfect Allocation

**Setup**:
- Exam: Year 2, CS201, 9:00 AM - 12:00 PM
- Hall: Block A, requires 2 invigilators
- Available Faculty: 5 eligible

**Result**:
```
✅ Assigned: Dr. Smith (ECE, Block A) - Score: 100, Load: 1
✅ Assigned: Dr. Jones (EEE, Block A) - Score: 100, Load: 1
```

**No suggestions needed** - All positions filled.

---

### Scenario 2: Partial Allocation with Suggestions

**Setup**:
- Exam: Year 1, EC101, 2:00 PM - 5:00 PM
- Hall: Block B, requires 3 invigilators
- Available Faculty: 1 eligible, 2 with clashes

**Result**:
```
✅ Assigned: Dr. Kumar (CSE, Block B) - Score: 100, Load: 0

⚠️ Suggestions Created:
1. Dr. Patel (MECH) - Teaching Year 2 at 2:00-3:00 PM
   → Suggest: Swap class or find substitute
   
2. Dr. Singh (EEE) - Teaching Year 3 at 2:30-4:00 PM
   → Suggest: Reschedule class or cancel
```

**Admin Action Required**: Review and implement suggestions.

---

### Scenario 3: Complex Multi-Year Exam

**Setup**:
- Exam: Year 1 & 2 combined, MA101 (Math), 9:00 AM - 11:00 AM
- Hall: Block C, requires 4 invigilators

**Faculty Timetables**:
- Dr. A: Teaching Year 1 at 9:00-10:00 → ✅ FREE (Year 1 in exam)
- Dr. B: Teaching Year 2 at 9:30-10:30 → ✅ FREE (Year 2 in exam)
- Dr. C: Teaching Year 3 at 9:00-10:00 → ❌ CLASH (Year 3 not in exam)
- Dr. D: Teaching Year 4 at 10:00-11:00 → ❌ CLASH (Year 4 not in exam)
- Dr. E: No class → ✅ FREE
- Dr. F: No class → ✅ FREE

**Result**:
```
✅ Assigned: Dr. A, Dr. B, Dr. E, Dr. F (4 invigilators)
No suggestions needed - All positions filled!
```

---

## Admin Workflow

### Step 1: Create Exam
1. Navigate to "Create Exam"
2. Fill in exam details
3. Select subject teacher (optional but recommended)
4. Save exam

### Step 2: Configure Halls
1. Go to exam detail page
2. Click "Assign Duties (Select Rooms)"
3. Select exam halls
4. Set required invigilators per hall
5. Save configuration

### Step 3: Auto-Allocate
1. Click "Auto Allocate Invigilators"
2. System processes all rules
3. Creates assignments
4. Sends email notifications
5. Creates suggestions if needed

### Step 4: Review Suggestions (if any)
1. Click "View Suggestions" button
2. Review each suggestion
3. Choose action:
   - **Implement**: Resolve clash and assign faculty
   - **Review**: Mark for later action
   - **Reject**: Not feasible

### Step 5: Monitor Confirmations
1. Go to "Pending Assignments"
2. Monitor faculty responses
3. Handle declines
4. Reassign if needed

---

## Best Practices

### For Admins

1. **Set Subject Teachers**: Always specify who teaches each subject
2. **Update Timetables**: Ensure faculty timetables are current
3. **Plan Ahead**: Create exams at least 3 hours in advance
4. **Review Suggestions Promptly**: Don't let suggestions pile up
5. **Communicate**: Inform faculty about timetable changes

### For Faculty

1. **Keep Profile Updated**: Cabin location, phone number
2. **Maintain Timetable**: Add all teaching slots accurately
3. **Apply for Leaves Early**: Give admin time to plan
4. **Respond Promptly**: Confirm or decline within deadline
5. **Provide Reasons**: When declining, explain why

---

## Technical Details

### Database Models

#### AllocationSuggestion
```python
- exam: ForeignKey to Exam
- exam_session_hall: ForeignKey to ExamSessionHall
- faculty: ForeignKey to Faculty
- clash_type: 'TIMETABLE_CLASH', 'SAME_DEPT', etc.
- clash_details: JSON with clash information
- suggestion_type: 'SWAP_CLASS', 'CANCEL_CLASS', etc.
- suggestion_text: Human-readable suggestion
- status: 'PENDING', 'REVIEWED', 'IMPLEMENTED', 'REJECTED'
- reviewed_by: Admin who reviewed
- admin_notes: Admin's notes
```

### API Endpoints

```
GET  /exams/admin/exams/<id>/suggestions/     - List suggestions for exam
GET  /exams/admin/suggestions/<id>/           - View suggestion detail
POST /exams/admin/suggestions/<id>/           - Take action on suggestion
GET  /exams/admin/suggestions/                - List all suggestions
```

---

## Future Enhancements

1. **Automatic Clash Resolution**: AI-powered suggestions for optimal swaps
2. **Bulk Operations**: Implement multiple suggestions at once
3. **Notification System**: Alert admins when suggestions are created
4. **Analytics**: Track allocation success rate, common clash patterns
5. **Mobile App**: Faculty can view and respond on mobile
6. **Calendar Integration**: Sync with Google Calendar, Outlook

---

## Troubleshooting

### Issue: Too Many Suggestions

**Cause**: Not enough faculty or too many clashes

**Solutions**:
1. Add more faculty to the system
2. Review and update faculty timetables
3. Consider rescheduling some classes
4. Hire temporary invigilators

### Issue: Same Faculty Always Gets Assigned

**Cause**: Only one faculty meets all criteria

**Solutions**:
1. Check if other faculty have incorrect timetables
2. Verify cabin locations are set correctly
3. Review leave approvals
4. Add more faculty from other departments

### Issue: Suggestions Not Showing

**Cause**: All positions filled or no viable candidates

**Solutions**:
1. Check if all required positions are filled
2. Verify faculty timetables are accurate
3. Look for faculty on leave
4. Check department exclusions

---

**Last Updated**: March 2026  
**Version**: 2.1
