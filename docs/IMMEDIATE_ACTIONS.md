# Immediate Actions Required

## 🚨 DO THESE RIGHT NOW (Before Any Deployment)

### 1. Secure Email Credentials (5 minutes)

**Step 1:** Install python-decouple
```bash
pip install python-decouple
```

**Step 2:** Create `.env` file in project root:
```env
DEBUG=True
SECRET_KEY=django-insecure-ti(f#aw^h#8g+91x!n$05(b67!$j--q_q-$y9$911@4*er*7$2
EMAIL_HOST_USER=bhavithayadalam11@gmail.com
EMAIL_HOST_PASSWORD=phyuicldfrzhhdck
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Step 3:** Add `.env` to `.gitignore`:
```bash
echo ".env" >> .gitignore
```

**Step 4:** Update `settings.py`:
```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
```

**Step 5:** Update requirements.txt:
```bash
echo "python-decouple==3.8" >> requirements.txt
```

**Step 6:** Remove credentials from git history (if already committed):
```bash
# This is complex - consider creating a new repository if credentials were committed
```

---

### 2. Fix Typo in Home Page (1 minute)

**File:** `templates/home.html` line 3

**Change:**
```html
{% block title %}invivgilation duties{% endblock %}
```

**To:**
```html
{% block title %}Invigilation Duties{% endblock %}
```

---

### 3. Fix Course Name in Batch Exam Creation (5 minutes)

**File:** `exams/views.py` - Add to `create_exam_batch` function

**Find the section where exams are created in the loop, and add:**
```python
# After getting department, year, semester
try:
    course = Course.objects.get(
        code=course_code,
        department=department,
        year=year,
        semester=semester
    )
    course_name = course.name
except Course.DoesNotExist:
    course_name = course_code

# Then use course_name when creating exam
exam = Exam.objects.create(
    course_code=course_code,
    course_name=course_name,  # Use the looked-up name
    # ... rest of fields
)
```

---

### 4. Add Time Slot Overlap Validation (10 minutes)

**File:** `timetable/views.py` - Update `api_slot_create` function

**Add before saving:**
```python
# Check for overlapping slots
overlapping = FacultyTimeSlot.objects.filter(
    faculty=faculty,
    day_of_week=day,
    start_time__lt=end_time,
    end_time__gt=start_time
).exists()

if overlapping:
    return JsonResponse({
        'success': False,
        'error': 'This time slot overlaps with an existing class'
    })
```

---

### 5. Add Transaction Handling to Batch Operations (10 minutes)

**File:** `accounts/views.py` - `create_faculty_batch` function

**Wrap the creation loop:**
```python
from django.db import transaction

# In create_faculty_batch view
try:
    with transaction.atomic():
        for i, emp_id in enumerate(employee_ids):
            # ... existing creation code
        
        messages.success(request, f"Created {created_count} faculty profiles.")
        return redirect("accounts:faculty_list")
except Exception as e:
    messages.error(request, f"Error creating faculty: {str(e)}")
    return render(request, "accounts/create_faculty_batch.html", {"departments": departments})
```

**Do the same for:** `exams/views.py` - `create_exam_batch` function

---

## 📋 Quick Checklist

- [ ] Move credentials to .env file
- [ ] Add .env to .gitignore
- [ ] Update settings.py to use environment variables
- [ ] Fix home page typo
- [ ] Fix course name in batch exam creation
- [ ] Add time slot overlap validation
- [ ] Add transaction handling to batch operations
- [ ] Test all changes locally
- [ ] Update requirements.txt
- [ ] Commit changes with proper message

---

## 🧪 Testing After Changes

### Test 1: Environment Variables
```bash
python manage.py shell
>>> from django.conf import settings
>>> print(settings.SECRET_KEY)  # Should print from .env
>>> print(settings.EMAIL_HOST_USER)  # Should print from .env
```

### Test 2: Batch Faculty Creation
1. Go to admin dashboard
2. Click "Create Faculty (Batch)"
3. Add 2-3 faculty members
4. Submit and verify no errors
5. Check that transaction rolls back if one fails

### Test 3: Batch Exam Creation
1. Go to admin dashboard
2. Click "Create Multiple Exams"
3. Add 2-3 exams
4. Verify course names are populated correctly

### Test 4: Time Slot Overlap
1. Login as faculty
2. Go to grid timetable
3. Create a time slot (e.g., MON 9:30-10:30)
4. Try to create overlapping slot (e.g., MON 10:00-11:00)
5. Should show error message

---

## ⚠️ Important Notes

1. **Never commit .env file** - It contains sensitive credentials
2. **Create .env.example** - Template for other developers:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password-here
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

3. **For production deployment:**
   - Set DEBUG=False
   - Generate new SECRET_KEY
   - Use production email credentials
   - Add production domain to ALLOWED_HOSTS

4. **Backup database before making changes:**
   ```bash
   python manage.py dumpdata > backup.json
   ```

---

## 🆘 If Something Goes Wrong

### Rollback Steps:
1. Restore from git: `git checkout -- <filename>`
2. Restore database: `python manage.py loaddata backup.json`
3. Check error logs in console
4. Verify .env file exists and has correct format

### Common Issues:
- **"config not found"** - Install python-decouple: `pip install python-decouple`
- **"Key error"** - Check .env file has all required variables
- **"Permission denied"** - Check file permissions on .env
- **"Import error"** - Restart Django server after installing packages

---

**Estimated Total Time:** 30-45 minutes  
**Difficulty:** Easy to Medium  
**Risk Level:** Low (if you backup first)
