# Quick Reference Card

## 🚀 Getting Started

### Start Server
```bash
python manage.py runserver
```

### Access URLs
- **Home**: http://localhost:8000
- **Login**: http://localhost:8000/accounts/login/
- **Admin Dashboard**: http://localhost:8000/exams/admin-dashboard/
- **Faculty Dashboard**: http://localhost:8000/exams/faculty-dashboard/

## 👨‍💼 Admin Quick Actions

### Initial Setup
1. Login → Auto-creates departments
2. Manage Halls → Add exam halls
3. Create Faculty (Batch) → Upload faculty data
4. Upload Timetables → Faculty teaching schedules
5. Manage Courses → Add course catalog

### Daily Operations
1. **Create Exam** → Manual or CSV upload
2. **Assign Duties** → Select halls → Auto-allocate
3. **Monitor** → Check pending confirmations
4. **Approve Leaves** → Review leave requests
5. **View Logs** → Track faculty activities

### Key URLs
```
/exams/admin-dashboard/          - Main dashboard
/exams/create-exam/              - Create exam
/exams/upload-exam-timetable/    - Upload CSV
/accounts/faculty/list/          - All faculty
/accounts/faculty/action-logs/   - Activity logs
/exams/pending-assignments/      - Pending duties
/leaves/leave-requests-admin/    - Leave requests
```

## 👨‍🏫 Faculty Quick Actions

### First Time
1. Check email for credentials
2. Login → Verify OTP
3. Change password (mandatory)
4. Update profile (cabin, phone)
5. Add/verify timetable

### Regular Use
1. **Check Dashboard** → View assigned duties
2. **Respond to Duties** → Confirm or decline (with reason)
3. **Update Timetable** → Keep schedule current
4. **Apply for Leave** → Submit leave requests
5. **Edit Profile** → Update contact info

### Key URLs
```
/exams/faculty-dashboard/        - My duties
/accounts/faculty/profile/edit/  - Edit profile
/timetable/faculty-timetable/    - My timetable
/leaves/my-leaves/               - My leaves
```

## 📧 Email Notifications

### When Sent
- **Assignment**: Immediately when duty assigned
- **Reminder**: 30 minutes before deadline
- **Decline Alert**: When faculty declines (to admin)
- **Expired**: When assignment expires (to admin)
- **First Login**: When faculty account created

### Email Configuration
```python
# settings.py
EMAIL_HOST_USER = "your-email@gmail.com"
EMAIL_HOST_PASSWORD = "your-16-char-app-password"
```

## ⏰ Automated Tasks

### Setup (Windows Task Scheduler)
1. Task Scheduler → Create Basic Task
2. Name: "Check Pending Assignments"
3. Trigger: Every 15 minutes
4. Action: `python.exe manage.py check_pending_assignments`

### Setup (Linux/Mac Cron)
```bash
crontab -e
*/15 * * * * cd /path/to/project && python manage.py check_pending_assignments
```

### What It Does
- Sends reminder emails
- Expires pending assignments
- Notifies admin of declines
- Sends initial notifications

## 📊 CSV Formats

### Faculty Timetable
```csv
employee_id,day_of_week,start_time,end_time,course_code,course_name,year,is_lab
EMP001,MON,09:00,10:00,CS101,Data Structures,2,False
```

### Exam Timetable
```csv
exam_date,start_time,end_time,course_code,course_name,department_code,year,semester,exam_type
2026-05-15,09:00,12:00,CS101,Data Structures,CSE,2,1,MID
```

## 🎯 Allocation Rules

### Faculty Eligible If:
- ✅ Different department than exam
- ✅ Not teaching the subject
- ✅ Not on approved leave
- ✅ No timetable clash
- ✅ Not already assigned for this exam

### Priority Order:
1. Same block as exam hall (100 points)
2. Lower workload
3. Random among equals

## ⏱️ Timeline

### Assignment Flow
```
T-3 hours:  Assignment created → Email sent
T-1.5 hours: Response deadline
T-30 min:   Reminder email (if pending)
T-0:        Assignment expires (if not confirmed)
```

## 🔧 Management Commands

```bash
# Check pending assignments (run every 15 min)
python manage.py check_pending_assignments

# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Make migrations
python manage.py makemigrations

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver

# Run on specific port
python manage.py runserver 8080
```

## 🐛 Troubleshooting

### Email Not Sending
```python
# Check settings.py
EMAIL_HOST_USER = "correct-email@gmail.com"
EMAIL_HOST_PASSWORD = "16-char-app-password"  # Not regular password!
```

### Faculty Can't Login
- Check email was sent
- Verify OTP not expired (10 min)
- Ensure faculty is_active=True

### No Eligible Faculty
- Check timetables for clashes
- Verify different departments
- Check leave approvals
- Ensure faculty profiles active

### Migrations Error
```bash
python manage.py makemigrations
python manage.py migrate
```

## 📱 Status Indicators

### Assignment Status
- 🟡 **Pending** - Awaiting faculty response
- 🟢 **Confirmed** - Faculty confirmed availability
- 🔴 **Declined** - Faculty declined (with reason)
- ⚫ **Expired** - Deadline passed without response
- ⚪ **Cancelled** - Admin cancelled
- 🔵 **Reassigned** - Assigned to another faculty

### Leave Status
- 🟡 **Pending** - Awaiting admin approval
- 🟢 **Approved** - Leave approved
- 🔴 **Rejected** - Leave rejected

## 🎨 UI Features

### Admin Dashboard
- Statistics cards (exams, duties, faculty)
- Quick action panels
- Upcoming exams table
- Color-coded status

### Faculty Dashboard
- Animated pending assignments (yellow pulse)
- Urgency indicators
- Deadline countdown
- Two-button response (Available/Not Available)

## 📋 Departments Supported

- **CSE** - Computer Science and Engineering
- **CSM** - Computer Science and AI/ML
- **CSD** - Computer Science and Data Science
- **ECE** - Electronics and Communication Engineering
- **EEE** - Electrical and Electronics Engineering
- **MECH** - Mechanical Engineering
- **CIVIL** - Civil Engineering

## 🔐 Security Features

- OTP-based authentication
- Mandatory password change on first login
- Password reset with OTP
- Role-based access control
- Activity logging
- Session management

## 📈 Statistics Available

### Admin View
- Total upcoming exams
- Exams today
- Pending confirmations
- Total active faculty

### Faculty Detail
- Total assignments
- Confirmed duties
- Declined duties
- Pending responses

## 💡 Best Practices

### For Admins
1. Keep faculty timetables updated
2. Create exams at least 3 hours in advance
3. Monitor pending confirmations regularly
4. Review action logs weekly
5. Backup database regularly

### For Faculty
1. Respond to assignments promptly
2. Keep profile information current
3. Update timetable each semester
4. Apply for leaves in advance
5. Provide clear decline reasons

## 🆘 Support

### Check First
1. Console logs for errors
2. Email configuration
3. Database migrations status
4. Faculty profile setup

### Common Solutions
```bash
# Reset migrations (if needed)
python manage.py migrate exams zero
python manage.py migrate

# Clear cache
python manage.py clearsessions

# Check database
python manage.py dbshell
```

## 📚 Documentation

- **README.md** - Full documentation
- **SETUP_GUIDE.md** - Setup instructions
- **CHANGES_SUMMARY.md** - What's new
- **QUICK_REFERENCE.md** - This file

---

**Version**: 2.0  
**Last Updated**: March 2026  
**Django Version**: 5.0.4  
**Python Version**: 3.8+
