# Testing Create Exam Feature

## Current Database Status

You have:
- **2 courses** in the database:
  1. CSE (Department ID: 1) - Year 1, Semester 1 - Course: R204GA54101 (Linear Algebra and Calculus)
  2. MECH (Department ID: 6) - Year 1, Semester 1 - Course: R204GA54101 (Linear Algebra and Calculus)

## How to Test

### Step 1: Start the Server
```bash
python manage.py runserver
```

### Step 2: Navigate to Create Exam
1. Login as admin
2. Go to: http://localhost:8000/exams/admin/create-exam/
3. Or click "Create Exam" from admin dashboard

### Step 3: Fill the Form

#### Test Case 1: CSE Course
1. **Department**: Select "CSE - Computer Science and Engineering"
2. **Year**: Select "1"
3. **Semester**: Select "1"
4. **Wait**: The course dropdown should automatically load
5. **Course Code**: You should see "R204GA54101 - Linear Algebra and Calculus"
6. **Course Name**: Should auto-fill with "Linear Algebra and Calculus"
7. **Exam Type**: Select "MID", "END", or "TEST"
8. **Exam Date**: Pick a future date
9. **Start Time**: e.g., 09:00
10. **End Time**: e.g., 12:00
11. Click "Create Exam"

#### Test Case 2: MECH Course
1. **Department**: Select "MECH - Mechanical Engineering"
2. **Year**: Select "1"
3. **Semester**: Select "1"
4. **Course Code**: Should show "R204GA54101 - Linear Algebra and Calculus"
5. Fill rest of the form
6. Click "Create Exam"

#### Test Case 3: No Courses Available
1. **Department**: Select "ECE - Electronics and Communication Engineering"
2. **Year**: Select "2"
3. **Semester**: Select "1"
4. **Result**: Should show "No courses found for this selection"
5. **Message**: "Please add courses in 'Manage Courses' first"

## Troubleshooting

### If courses don't load:

1. **Open Browser Console** (F12 → Console tab)
2. Look for messages like:
   - "Loading courses for: {dept, year, sem}"
   - "Fetching from: /exams/api/courses/..."
   - "Received data: ..."
   - "Loaded X courses"

3. **Check for errors**:
   - Red error messages in console
   - Network errors (check Network tab)
   - 403/404/500 errors

### Common Issues:

#### Issue 1: "No courses found"
**Cause**: No courses exist for that department/year/semester combination
**Solution**: Add courses first via "Manage Courses"

#### Issue 2: Dropdown stays disabled
**Cause**: JavaScript not loading or error in code
**Solution**: 
- Check browser console for errors
- Refresh page (Ctrl+F5)
- Clear browser cache

#### Issue 3: API returns error
**Cause**: Permission issue or server error
**Solution**:
- Check you're logged in as admin
- Check server console for errors
- Verify URL: http://localhost:8000/exams/api/courses/?department=1&year=1&semester=1

## Adding More Courses

To add more courses for testing:

### Option 1: Via Django Admin
1. Go to: http://localhost:8000/admin/
2. Navigate to "Timetable" → "Courses"
3. Click "Add Course"
4. Fill in:
   - Department
   - Code (e.g., CS101)
   - Name (e.g., Data Structures)
   - Year (1-4)
   - Semester (1-2)
5. Save

### Option 2: Via Manage Courses Page
1. Go to admin dashboard
2. Click "Manage Courses"
3. Add courses via the interface

### Option 3: Via Django Shell
```bash
python manage.py shell
```

```python
from timetable.models import Course
from exams.models import Department

# Get departments
cse = Department.objects.get(code='CSE')
ece = Department.objects.get(code='ECE')

# Add CSE courses
Course.objects.create(
    department=cse,
    code='CS101',
    name='Data Structures',
    year=2,
    semester=1
)

Course.objects.create(
    department=cse,
    code='CS102',
    name='Database Management Systems',
    year=2,
    semester=1
)

# Add ECE courses
Course.objects.create(
    department=ece,
    code='EC201',
    name='Digital Electronics',
    year=2,
    semester=1
)

Course.objects.create(
    department=ece,
    code='EC202',
    name='Signals and Systems',
    year=2,
    semester=1
)

print("Courses added successfully!")
```

## Expected Behavior

### Visual Feedback:
1. **Before selection**: Yellow alert "Please select Department, Year, and Semester"
2. **While loading**: "Loading courses..." in dropdown, blue status text
3. **After loading**: 
   - Success: Green status "X course(s) available"
   - No courses: Red status "No courses found"
   - Error: Red status "Error: ..."

### Dropdown States:
1. **Initial**: Disabled, shows "-- Select Department, Year, Semester First --"
2. **Loading**: Disabled, shows "Loading courses..."
3. **Loaded**: Enabled, shows courses
4. **No courses**: Disabled, shows "No courses found"
5. **Error**: Disabled, shows "Error loading courses"

## Success Criteria

✅ Dropdown loads courses when all three fields are selected
✅ Course name auto-fills when course is selected
✅ Form submits successfully
✅ Exam appears in exam list
✅ Clear error messages when no courses found
✅ Visual feedback at each step

## Next Steps After Testing

If everything works:
1. Add more courses for different departments
2. Create multiple exams
3. Test the duty allocation feature
4. Verify email notifications

If issues persist:
1. Check browser console for JavaScript errors
2. Check server console for Python errors
3. Verify database has courses
4. Test API endpoint directly in browser
