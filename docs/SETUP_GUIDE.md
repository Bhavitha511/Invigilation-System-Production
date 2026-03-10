# Quick Setup Guide

## Immediate Next Steps

### 1. Run the Development Server
```bash
python manage.py runserver
```

### 2. Access the Application
- **URL**: http://localhost:8000
- **Admin Login**: http://localhost:8000/accounts/login/
- **Admin Dashboard**: http://localhost:8000/exams/admin-dashboard/

### 3. First-Time Admin Setup

#### Create Superuser (if not done)
```bash
python manage.py createsuperuser
```

#### Login as Admin
1. Go to http://localhost:8000/accounts/login/
2. Enter superuser credentials
3. You'll be redirected to admin dashboard

### 4. Initial Configuration

#### Step 1: Verify Departments
- Departments are auto-created on first dashboard visit
- Navigate to "Manage Departments" to verify:
  - CSE, CSM, CSD, ECE, EEE, MECH, CIVIL

#### Step 2: Add Exam Halls
1. Click "Manage Halls"
2. Add halls with:
   - Name (e.g., "Hall 101")
   - Block (e.g., "Block A")
   - Floor (optional)
   - Capacity (number of students)

#### Step 3: Create Faculty Profiles
**Option A: Batch Creation (Recommended)**
1. Click "Create Faculty Profiles (Batch Mode)"
2. Fill in the form with faculty details
3. System will:
   - Create user accounts
   - Send email with credentials
   - Set temporary password

**Option B: Manual Creation**
1. Click "Create Faculty" (single)
2. Fill in individual faculty details

**Faculty CSV Format** (if you want to prepare data):
```csv
employee_id,first_name,last_name,email,department_code,cabin_block,cabin_room,phone_number
EMP001,John,Doe,john@example.com,CSE,Block A,101,1234567890
EMP002,Jane,Smith,jane@example.com,ECE,Block B,202,0987654321
```

#### Step 4: Upload Faculty Timetables
1. Navigate to "Upload Timetables"
2. Upload CSV file with teaching schedules
3. Format:
```csv
employee_id,day_of_week,start_time,end_time,course_code,course_name,year,is_lab
EMP001,MON,09:00,10:00,CS101,Data Structures,2,False
EMP001,TUE,14:00,17:00,CS102,Database Lab,3,True
```

#### Step 5: Add Courses
1. Click "Manage Courses"
2. Add courses for each department with:
   - Course code
   - Course name
   - Year (1-4)
   - Semester (1-2)

#### Step 6: Create Exams
**Option A: Manual Creation**
1. Click "Create Exam"
2. Fill in exam details:
   - Course code and name
   - Department
   - Date and time
   - Exam type (MID/END/TEST)
   - Subject teacher (optional)

**Option B: CSV Upload**
1. Click "Upload Exam Timetable"
2. Upload CSV file
3. Format:
```csv
exam_date,start_time,end_time,course_code,course_name,department_code,year,semester,exam_type
2026-05-15,09:00,12:00,CS101,Data Structures,CSE,2,1,MID
```

#### Step 7: Assign Invigilation Duties
1. Go to exam detail page
2. Click "Assign Duties (Select Rooms)"
3. Select exam halls
4. Set required invigilators per hall
5. Click "Auto-Allocate Duties"
6. System will:
   - Find eligible faculty
   - Send email notifications
   - Set confirmation deadlines

### 5. Setup Automated Tasks (Important!)

The system needs to run periodic checks for:
- Sending reminder emails
- Expiring pending assignments
- Notifying admins

#### Windows (Task Scheduler)
1. Open Task Scheduler
2. Create Basic Task: "Check Pending Assignments"
3. Trigger: Repeat every 15 minutes
4. Action: Start a program
   - Program: `C:\path\to\venv\Scripts\python.exe`
   - Arguments: `manage.py check_pending_assignments`
   - Start in: `C:\Users\yadal\Downloads\KIRO - PROJECT`

#### Linux/Mac (Cron)
```bash
crontab -e
# Add this line:
*/15 * * * * cd /path/to/project && /path/to/venv/bin/python manage.py check_pending_assignments
```

### 6. Email Configuration

Update `invigilation_system/settings.py`:

```python
EMAIL_HOST_USER = "your-email@gmail.com"
EMAIL_HOST_PASSWORD = "your-16-char-app-password"
```

**Getting Gmail App Password:**
1. Go to Google Account settings
2. Security → 2-Step Verification
3. App passwords
4. Generate new app password
5. Copy the 16-character password

### 7. Test the System

#### Test Faculty Login
1. Create a test faculty account
2. Check email for credentials
3. Login at http://localhost:8000/accounts/login/
4. Verify OTP from email
5. Change password
6. Access faculty dashboard

#### Test Duty Assignment
1. Create an exam (future date)
2. Configure halls
3. Auto-allocate duties
4. Check faculty email for notification
5. Login as faculty and confirm/decline

### 8. Production Deployment (Optional)

For production deployment:

1. **Change SECRET_KEY** in settings.py
2. **Set DEBUG = False**
3. **Configure ALLOWED_HOSTS**
4. **Use PostgreSQL** instead of SQLite
5. **Setup static files serving**
6. **Use production WSGI server** (Gunicorn, uWSGI)
7. **Setup HTTPS**
8. **Configure proper email backend**

## Common Issues

### Issue: Email not sending
**Solution**: 
- Use Gmail app password, not regular password
- Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
- Verify internet connection

### Issue: Faculty can't login
**Solution**:
- Verify email was sent with credentials
- Check OTP expiration (10 minutes)
- Ensure faculty profile is active

### Issue: No eligible faculty for allocation
**Solution**:
- Check faculty timetables for clashes
- Verify faculty are from different departments
- Check leave approvals
- Ensure faculty profiles are active

### Issue: Static files not loading
**Solution**:
```bash
python manage.py collectstatic
```

## Quick Reference

### Admin URLs
- Dashboard: `/exams/admin-dashboard/`
- Create Exam: `/exams/create-exam/`
- Faculty List: `/accounts/faculty/list/`
- Action Logs: `/accounts/faculty/action-logs/`
- Manage Halls: `/exams/manage-halls/`
- Manage Departments: `/exams/manage-departments/`

### Faculty URLs
- Dashboard: `/exams/faculty-dashboard/`
- Edit Profile: `/accounts/faculty/profile/edit/`
- My Timetable: `/timetable/faculty-timetable/`
- My Leaves: `/leaves/my-leaves/`

### Management Commands
```bash
# Check pending assignments (run every 15 min)
python manage.py check_pending_assignments

# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic
```

## Support

For detailed documentation, see README.md

For issues:
1. Check console logs
2. Check email configuration
3. Verify database migrations
4. Check faculty profile setup
