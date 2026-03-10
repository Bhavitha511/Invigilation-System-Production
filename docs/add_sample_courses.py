#!/usr/bin/env python
"""
Script to add sample courses for testing the exam creation feature.
Run with: python add_sample_courses.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invigilation_system.settings')
django.setup()

from timetable.models import Course
from exams.models import Department

def add_sample_courses():
    """Add sample courses for all departments"""
    
    print("=" * 60)
    print("ADDING SAMPLE COURSES")
    print("=" * 60)
    
    # Get all departments
    departments = Department.objects.all()
    print(f"\nFound {departments.count()} departments")
    
    # Sample courses for each year/semester
    courses_data = {
        'CSE': [
            # Year 1
            {'code': 'CS101', 'name': 'Programming Fundamentals', 'year': 1, 'semester': 1},
            {'code': 'CS102', 'name': 'Data Structures', 'year': 1, 'semester': 2},
            # Year 2
            {'code': 'CS201', 'name': 'Database Management Systems', 'year': 2, 'semester': 1},
            {'code': 'CS202', 'name': 'Operating Systems', 'year': 2, 'semester': 2},
            # Year 3
            {'code': 'CS301', 'name': 'Computer Networks', 'year': 3, 'semester': 1},
            {'code': 'CS302', 'name': 'Software Engineering', 'year': 3, 'semester': 2},
            # Year 4
            {'code': 'CS401', 'name': 'Machine Learning', 'year': 4, 'semester': 1},
            {'code': 'CS402', 'name': 'Cloud Computing', 'year': 4, 'semester': 2},
        ],
        'ECE': [
            # Year 1
            {'code': 'EC101', 'name': 'Basic Electronics', 'year': 1, 'semester': 1},
            {'code': 'EC102', 'name': 'Circuit Theory', 'year': 1, 'semester': 2},
            # Year 2
            {'code': 'EC201', 'name': 'Digital Electronics', 'year': 2, 'semester': 1},
            {'code': 'EC202', 'name': 'Signals and Systems', 'year': 2, 'semester': 2},
            # Year 3
            {'code': 'EC301', 'name': 'Communication Systems', 'year': 3, 'semester': 1},
            {'code': 'EC302', 'name': 'Microprocessors', 'year': 3, 'semester': 2},
            # Year 4
            {'code': 'EC401', 'name': 'VLSI Design', 'year': 4, 'semester': 1},
            {'code': 'EC402', 'name': 'Embedded Systems', 'year': 4, 'semester': 2},
        ],
        'EEE': [
            # Year 1
            {'code': 'EE101', 'name': 'Electrical Circuits', 'year': 1, 'semester': 1},
            {'code': 'EE102', 'name': 'Electromagnetic Theory', 'year': 1, 'semester': 2},
            # Year 2
            {'code': 'EE201', 'name': 'Power Systems', 'year': 2, 'semester': 1},
            {'code': 'EE202', 'name': 'Control Systems', 'year': 2, 'semester': 2},
            # Year 3
            {'code': 'EE301', 'name': 'Power Electronics', 'year': 3, 'semester': 1},
            {'code': 'EE302', 'name': 'Electrical Machines', 'year': 3, 'semester': 2},
            # Year 4
            {'code': 'EE401', 'name': 'Renewable Energy', 'year': 4, 'semester': 1},
            {'code': 'EE402', 'name': 'Smart Grid Technology', 'year': 4, 'semester': 2},
        ],
        'MECH': [
            # Year 1
            {'code': 'ME101', 'name': 'Engineering Mechanics', 'year': 1, 'semester': 1},
            {'code': 'ME102', 'name': 'Engineering Drawing', 'year': 1, 'semester': 2},
            # Year 2
            {'code': 'ME201', 'name': 'Thermodynamics', 'year': 2, 'semester': 1},
            {'code': 'ME202', 'name': 'Fluid Mechanics', 'year': 2, 'semester': 2},
            # Year 3
            {'code': 'ME301', 'name': 'Machine Design', 'year': 3, 'semester': 1},
            {'code': 'ME302', 'name': 'Manufacturing Processes', 'year': 3, 'semester': 2},
            # Year 4
            {'code': 'ME401', 'name': 'Robotics', 'year': 4, 'semester': 1},
            {'code': 'ME402', 'name': 'Automobile Engineering', 'year': 4, 'semester': 2},
        ],
        'CIVIL': [
            # Year 1
            {'code': 'CE101', 'name': 'Engineering Mechanics', 'year': 1, 'semester': 1},
            {'code': 'CE102', 'name': 'Building Materials', 'year': 1, 'semester': 2},
            # Year 2
            {'code': 'CE201', 'name': 'Structural Analysis', 'year': 2, 'semester': 1},
            {'code': 'CE202', 'name': 'Geotechnical Engineering', 'year': 2, 'semester': 2},
            # Year 3
            {'code': 'CE301', 'name': 'Concrete Technology', 'year': 3, 'semester': 1},
            {'code': 'CE302', 'name': 'Transportation Engineering', 'year': 3, 'semester': 2},
            # Year 4
            {'code': 'CE401', 'name': 'Environmental Engineering', 'year': 4, 'semester': 1},
            {'code': 'CE402', 'name': 'Construction Management', 'year': 4, 'semester': 2},
        ],
    }
    
    total_added = 0
    total_skipped = 0
    
    for dept in departments:
        dept_code = dept.code
        
        # Handle variations in department codes
        if dept_code == 'CIV':
            dept_code = 'CIVIL'
        
        if dept_code not in courses_data:
            print(f"\n⚠️  No sample data for {dept.code} - {dept.name}")
            continue
        
        print(f"\n📚 Adding courses for {dept.code} - {dept.name}")
        print("-" * 60)
        
        for course_info in courses_data[dept_code]:
            # Check if course already exists
            existing = Course.objects.filter(
                department=dept,
                code=course_info['code'],
                year=course_info['year'],
                semester=course_info['semester']
            ).first()
            
            if existing:
                print(f"   ⏭️  Skipped: {course_info['code']} (already exists)")
                total_skipped += 1
            else:
                Course.objects.create(
                    department=dept,
                    code=course_info['code'],
                    name=course_info['name'],
                    year=course_info['year'],
                    semester=course_info['semester']
                )
                print(f"   ✅ Added: {course_info['code']} - {course_info['name']} (Y{course_info['year']}S{course_info['semester']})")
                total_added += 1
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✅ Courses added: {total_added}")
    print(f"⏭️  Courses skipped (already exist): {total_skipped}")
    print(f"📊 Total courses in database: {Course.objects.count()}")
    print("\n✨ Sample courses added successfully!")
    print("\nYou can now:")
    print("1. Go to http://localhost:8000/exams/admin/create-exam/")
    print("2. Select any department, year, and semester")
    print("3. See the courses in the dropdown")
    print("=" * 60)

if __name__ == '__main__':
    add_sample_courses()
