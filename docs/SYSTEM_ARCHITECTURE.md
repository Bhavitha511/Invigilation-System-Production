# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
├─────────────────────────────────────────────────────────────────┤
│  Admin Dashboard          │         Faculty Dashboard           │
│  - Statistics             │         - My Duties                 │
│  - Exam Management        │         - Confirm/Decline           │
│  - Faculty Management     │         - Profile Edit              │
│  - Duty Allocation        │         - Timetable                 │
│  - Action Logs            │         - Leave Requests            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DJANGO APPLICATION                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   Accounts   │  │    Exams     │  │  Timetable   │        │
│  │   - Auth     │  │   - Exams    │  │  - Slots     │        │
│  │   - Faculty  │  │   - Halls    │  │  - Courses   │        │
│  │   - Profile  │  │   - Assign   │  │  - Upload    │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐                           │
│  │    Leaves    │  │     Logs     │                           │
│  │  - Requests  │  │  - Actions   │                           │
│  │  - Approval  │  │  - Tracking  │                           │
│  └──────────────┘  └──────────────┘                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BUSINESS LOGIC                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Auto-Allocation Algorithm:                                    │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ 1. Filter Eligible Faculty                             │   │
│  │    - Different department                              │   │
│  │    - Not subject teacher                               │   │
│  │    - Not on leave                                      │   │
│  │    - No timetable clash                                │   │
│  │                                                         │   │
│  │ 2. Score Faculty                                       │   │
│  │    - Proximity: +100 for same block                    │   │
│  │    - Workload: Lower is better                         │   │
│  │                                                         │   │
│  │ 3. Randomize Among Equals                              │   │
│  │                                                         │   │
│  │ 4. Assign & Notify                                     │   │
│  │    - Create assignment                                 │   │
│  │    - Set deadline (T-1.5 hours)                        │   │
│  │    - Send email                                        │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    NOTIFICATION SYSTEM                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Email Notifications:                                          │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ • Assignment Created    → Faculty                      │   │
│  │ • Reminder (T-30 min)   → Faculty                      │   │
│  │ • Declined              → Admin                        │   │
│  │ • Expired               → Admin                        │   │
│  │ • First Login           → Faculty                      │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AUTOMATED TASKS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Management Command (Every 15 minutes):                        │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ check_pending_assignments                              │   │
│  │                                                         │   │
│  │ 1. Check for expired assignments                       │   │
│  │    → Mark as EXPIRED                                   │   │
│  │    → Notify admin                                      │   │
│  │                                                         │   │
│  │ 2. Send reminder emails                                │   │
│  │    → 30 min before deadline                            │   │
│  │    → Only if not already sent                          │   │
│  │                                                         │   │
│  │ 3. Send initial notifications                          │   │
│  │    → 3 hours before exam                               │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SQLite Database (Development) / PostgreSQL (Production)       │
│                                                                 │
│  Tables:                                                        │
│  • auth_user                                                    │
│  • accounts_faculty                                             │
│  • exams_exam                                                   │
│  • exams_examhall                                               │
│  • exams_examsessionhall                                        │
│  • exams_invigilationassignment                                 │
│  • timetable_facultytimeslot                                    │
│  • timetable_course                                             │
│  • leaves_facultyleave                                          │
│  • logs_facultyactionlog                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagrams

### 1. Duty Assignment Flow

```
Admin Creates Exam
       │
       ▼
Admin Configures Halls
       │
       ▼
Admin Clicks "Auto-Allocate"
       │
       ▼
┌──────────────────────────────────────┐
│  Allocation Algorithm                │
│  1. Get all active faculty           │
│  2. Filter by rules                  │
│  3. Score by proximity & workload    │
│  4. Randomize among equals           │
│  5. Select top N                     │
└──────────────────────────────────────┘
       │
       ▼
Create InvigilationAssignment
       │
       ├─────────────────┬─────────────────┐
       ▼                 ▼                 ▼
Set Deadline    Send Email         Log Action
(T-1.5 hrs)     to Faculty         to Database
       │                 │                 │
       └─────────────────┴─────────────────┘
                         │
                         ▼
              Faculty Receives Email
                         │
                         ▼
              Faculty Logs In
                         │
                ┌────────┴────────┐
                ▼                 ▼
           Confirms          Declines
                │                 │
                ▼                 ▼
        Status=CONFIRMED   Status=DECLINED
                │          Send Admin Alert
                │                 │
                └─────────────────┘
                         │
                         ▼
                  Assignment Complete
```

### 2. Faculty Response Flow

```
Faculty Logs In
       │
       ▼
Views Dashboard
       │
       ▼
Sees Pending Assignment (Yellow Highlight)
       │
       ├─────────────────────────────┐
       ▼                             ▼
Clicks "Available"          Clicks "Not Available"
       │                             │
       ▼                             ▼
Confirm Assignment          Enter Decline Reason
       │                             │
       ▼                             ▼
Status → CONFIRMED          Status → DECLINED
confirmed_at = now          declined_at = now
       │                    decline_reason = text
       │                             │
       │                             ▼
       │                    Send Email to Admin
       │                             │
       └─────────────────────────────┘
                         │
                         ▼
              Redirect to Dashboard
                         │
                         ▼
              Show Success Message
```

### 3. Automated Task Flow

```
Cron/Task Scheduler (Every 15 min)
       │
       ▼
Run: check_pending_assignments
       │
       ├─────────────────┬─────────────────┬─────────────────┐
       ▼                 ▼                 ▼                 ▼
Check Expired    Send Reminders   Send Initial    Log Results
Assignments      (T-30 min)       Notifications
       │                 │         (T-3 hrs)           │
       ▼                 ▼                 ▼           │
Mark as EXPIRED   Update reminder   Update notif     │
       │          _sent_at          _sent_at          │
       ▼                 │                 │           │
Notify Admin            │                 │           │
       │                 │                 │           │
       └─────────────────┴─────────────────┴───────────┘
                         │
                         ▼
                  Task Complete
```

## Component Interaction

### Models Relationships

```
User (Django Auth)
  │
  └─── Faculty (1:1)
         │
         ├─── FacultyTimeSlot (1:N)
         │
         ├─── FacultyLeave (1:N)
         │
         ├─── FacultyActionLog (1:N)
         │
         └─── InvigilationAssignment (1:N)
                │
                └─── ExamSessionHall (N:1)
                       │
                       ├─── Exam (N:1)
                       │      │
                       │      ├─── Department (N:1)
                       │      │
                       │      └─── Faculty (subject_teacher) (N:1)
                       │
                       └─── ExamHall (N:1)

Department (1:N)
  │
  ├─── Faculty
  │
  ├─── Exam
  │
  └─── Course
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      AUTHENTICATION                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Login Flow:                                                    │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ 1. User enters username/password                       │   │
│  │ 2. System validates credentials                        │   │
│  │ 3. Generate 6-digit OTP                                │   │
│  │ 4. Send OTP via email                                  │   │
│  │ 5. User enters OTP                                     │   │
│  │ 6. Validate OTP (10 min expiry)                        │   │
│  │ 7. Create session                                      │   │
│  │ 8. Check must_change_password flag                     │   │
│  │ 9. Redirect to dashboard or password change            │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AUTHORIZATION                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Role-Based Access:                                            │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ Admin (is_staff=True):                                 │   │
│  │  • All admin views                                     │   │
│  │  • Faculty management                                  │   │
│  │  • Exam management                                     │   │
│  │  • Duty allocation                                     │   │
│  │  • View all logs                                       │   │
│  │                                                         │   │
│  │ Faculty (is_staff=False):                              │   │
│  │  • Own dashboard                                       │   │
│  │  • Own profile edit                                    │   │
│  │  • Own timetable                                       │   │
│  │  • Own assignments                                     │   │
│  │  • Own leaves                                          │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AUDIT LOGGING                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  All Actions Logged:                                           │
│  • Profile changes                                             │
│  • Timetable updates                                           │
│  • Assignment responses                                        │
│  • Leave requests                                              │
│  • Admin actions                                               │
│                                                                 │
│  Log Fields:                                                   │
│  • Faculty                                                     │
│  • Action type                                                 │
│  • Description                                                 │
│  • Timestamp                                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                      FRONTEND                                   │
├─────────────────────────────────────────────────────────────────┤
│  • HTML5                                                        │
│  • CSS3                                                         │
│  • JavaScript (ES6+)                                            │
│  • Bootstrap 5.3.3                                              │
│  • Font Awesome 6.4.0                                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND                                    │
├─────────────────────────────────────────────────────────────────┤
│  • Python 3.8+                                                  │
│  • Django 5.0.4                                                 │
│  • Django ORM                                                   │
│  • Django Templates                                             │
│  • Django Forms                                                 │
│  • Django Admin                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATABASE                                   │
├─────────────────────────────────────────────────────────────────┤
│  • SQLite (Development)                                         │
│  • PostgreSQL (Production-ready)                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      EXTERNAL SERVICES                          │
├─────────────────────────────────────────────────────────────────┤
│  • SMTP (Gmail) - Email notifications                           │
│  • Cron/Task Scheduler - Automated tasks                        │
└─────────────────────────────────────────────────────────────────┘
```

## Deployment Architecture (Production)

```
┌─────────────────────────────────────────────────────────────────┐
│                      LOAD BALANCER                              │
│                      (Nginx/Apache)                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│   Application Server 1   │  │   Application Server 2   │
│   (Gunicorn/uWSGI)       │  │   (Gunicorn/uWSGI)       │
└──────────────────────────┘  └──────────────────────────┘
                │                           │
                └─────────────┬─────────────┘
                              ▼
                ┌──────────────────────────┐
                │   Database Server        │
                │   (PostgreSQL)           │
                └──────────────────────────┘
                              │
                              ▼
                ┌──────────────────────────┐
                │   Static Files Server    │
                │   (Nginx/CDN)            │
                └──────────────────────────┘
                              │
                              ▼
                ┌──────────────────────────┐
                │   Background Tasks       │
                │   (Celery + Redis)       │
                └──────────────────────────┘
```

## Performance Considerations

### Database Optimization
- Indexes on foreign keys
- select_related() for 1:1 and N:1
- prefetch_related() for 1:N and M:N
- Query result limiting

### Caching Strategy (Future)
```
┌─────────────────────────────────────────────────────────────────┐
│                      CACHE LAYERS                               │
├─────────────────────────────────────────────────────────────────┤
│  • Redis - Session storage                                     │
│  • Redis - Query results                                       │
│  • Redis - Celery broker                                       │
│  • Browser - Static files                                      │
│  • CDN - Static assets                                         │
└─────────────────────────────────────────────────────────────────┘
```

### Scalability
- Horizontal scaling (multiple app servers)
- Database replication (read replicas)
- Background task queue (Celery)
- Static file CDN
- Load balancing

## Monitoring & Logging

```
┌─────────────────────────────────────────────────────────────────┐
│                      MONITORING                                 │
├─────────────────────────────────────────────────────────────────┤
│  • Application logs (Django logging)                           │
│  • Database query logs                                         │
│  • Email delivery logs                                         │
│  • User action logs (FacultyActionLog)                         │
│  • Error tracking (Sentry - optional)                          │
│  • Performance monitoring (New Relic - optional)               │
└─────────────────────────────────────────────────────────────────┘
```

---

**Last Updated**: March 2026  
**Version**: 2.0
