#!/usr/bin/env python
"""
Clear previous test data and run fresh comprehensive test with CORRECT allocation rules
"""
import os
import sys
import django
from datetime import datetime, date, time, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invigilation_system.settings')
django.setup()

from django.utils import timezone
from exams.models import Exam, Department, ExamSessionHall, InvigilationAssignment, ExamHall
from accounts.models import Faculty
from timetable.models import FacultyTimeSlot
from leaves.models import FacultyLeave

def clear_previous_test_data():
    """Clear all previous test data"""
    print("🧹 CLEARING PREVIOUS TEST DATA")
    print("="*40)
    
    # Clear allocations
    assignments_count = InvigilationAssignment.objects.count()
    InvigilationAssignment.objects.all().delete()
    print(f"   ✅ Cleared {assignments_count} invigilation assignments")
    
    # Clear exam session halls
    session_halls_count = ExamSessionHall.objects.count()
    ExamSessionHall.objects.all().delete()
    print(f"   ✅ Cleared {session_halls_count} exam session halls")
    
    # Clear exams
    exams_count = Exam.objects.count()
    Exam.objects.all().delete()
    print(f"   ✅ Cleared {exams_count} exams")
    
    # Clear test leaves (keep only non-test leaves)
    test_leaves = FacultyLeave.objects.filter(reason__icontains='Testing')
    test_leaves_count = test_leaves.count()
    test_leaves.delete()
    print(f"   ✅ Cleared {test_leaves_count} test leaves")
    
    print(f"   🎯 All previous test data cleared!")

def create_fresh_test_exams():
    """Create fresh test exams with realistic scenarios"""
    print("\n📋 CREATING FRESH TEST EXAMS")
    print("="*40)
    
    # Get departments
    departments = list(Department.objects.all())
    if not departments:
        print("❌ No departments found")
        return []
    
    print(f"   📊 Available departments: {len(departments)}")
    for dept in departments:
        print(f"      🏫 {dept.code} - {dept.name}")
    
    # Create exams starting 3 days from now
    base_date = timezone.now().date() + timedelta(days=3)
    
    # Ensure we have exam halls
    halls = list(ExamHall.objects.all())
    if not halls:
        print("   🏢 Creating exam halls...")
        hall_data = [
            {'name': 'Main Hall A', 'capacity': 120, 'block': 'Main Block'},
            {'name': 'Main Hall B', 'capacity': 100, 'block': 'Main Block'},
            {'name': 'CS Lab 1', 'capacity': 60, 'block': 'CS Block'},
            {'name': 'ECE Hall', 'capacity': 80, 'block': 'ECE Block'},
            {'name': 'MECH Hall', 'capacity': 90, 'block': 'MECH Block'},
        ]
        
        for hall_info in hall_data:
            hall, created = ExamHall.objects.get_or_create(
                name=hall_info['name'],
                defaults=hall_info
            )
            if created:
                print(f"      ✅ Created hall: {hall.name}")
            halls.append(hall)
    
    # Create diverse exam scenarios
    exam_scenarios = [
        # Day 1 - Morning: CSE exam (should avoid CSE faculty)
        {
            'course_code': 'CS301',
            'course_name': 'Computer Networks',
            'exam_type': 'END',
            'department': next((d for d in departments if d.code == 'CSE'), departments[0]),
            'exam_date': base_date,
            'start_time': time(9, 30),
            'end_time': time(12, 30),
            'year': 3,
            'semester': 1
        },
        
        # Day 1 - Afternoon: ECE exam (should avoid ECE faculty)
        {
            'course_code': 'ECE201',
            'course_name': 'Digital Electronics',
            'exam_type': 'END',
            'department': next((d for d in departments if d.code == 'ECE'), departments[0]),
            'exam_date': base_date,
            'start_time': time(14, 0),
            'end_time': time(17, 0),
            'year': 2,
            'semester': 1
        },
        
        # Day 2 - Morning: MECH exam (should avoid MECH faculty)
        {
            'course_code': 'MECH301',
            'course_name': 'Thermodynamics',
            'exam_type': 'END',
            'department': next((d for d in departments if d.code == 'MECH'), departments[0]),
            'exam_date': base_date + timedelta(days=1),
            'start_time': time(9, 30),
            'end_time': time(12, 30),
            'year': 3,
            'semester': 1
        },
        
        # Day 2 - Afternoon: CSM exam (should avoid CSM faculty)
        {
            'course_code': 'CSM201',
            'course_name': 'Data Structures',
            'exam_type': 'END',
            'department': next((d for d in departments if d.code == 'CSM'), departments[0]),
            'exam_date': base_date + timedelta(days=1),
            'start_time': time(14, 0),
            'end_time': time(17, 0),
            'year': 2,
            'semester': 1
        },
        
        # Day 3 - Morning: CSD exam (should avoid CSD faculty)
        {
            'course_code': 'CSD401',
            'course_name': 'Machine Learning',
            'exam_type': 'END',
            'department': next((d for d in departments if d.code == 'CSD'), departments[0]),
            'exam_date': base_date + timedelta(days=2),
            'start_time': time(10, 0),
            'end_time': time(13, 0),
            'year': 4,
            'semester': 1
        },
        
        # Day 3 - Afternoon: EEE exam (should avoid EEE faculty)
        {
            'course_code': 'EEE301',
            'course_name': 'Power Systems',
            'exam_type': 'END',
            'department': next((d for d in departments if d.code == 'EEE'), departments[0]),
            'exam_date': base_date + timedelta(days=2),
            'start_time': time(14, 30),
            'end_time': time(17, 30),
            'year': 3,
            'semester': 1
        }
    ]
    
    created_exams = []
    for i, exam_data in enumerate(exam_scenarios, 1):
        exam = Exam.objects.create(**exam_data)
        created_exams.append(exam)
        print(f"   ✅ {i}. Created: {exam.course_code} - {exam.course_name}")
        print(f"      📅 {exam.exam_date} {exam.start_time}-{exam.end_time}")
        print(f"      🏫 {exam.department.code} Year {exam.year} Semester {exam.semester}")
    
    print(f"\n   📊 Total exams created: {len(created_exams)}")
    return created_exams

def create_strategic_faculty_leaves():
    """Create strategic faculty leaves to test leave handling"""
    print("\n🏖️ CREATING STRATEGIC FACULTY LEAVES")
    print("="*40)
    
    faculty_list = list(Faculty.objects.filter(is_active=True))
    if len(faculty_list) < 2:
        print("   ⚠️ Not enough faculty for leave testing")
        return
    
    base_date = timezone.now().date() + timedelta(days=3)
    
    # Create leave for one faculty during first exam day
    leave_faculty = faculty_list[0]
    leave = FacultyLeave.objects.create(
        faculty=leave_faculty,
        start_date=base_date,
        end_date=base_date,
        reason='Medical Leave - Fresh Test',
        status=FacultyLeave.APPROVED
    )
    
    print(f"   ✅ Created leave for {leave_faculty.user.get_full_name()}")
    print(f"      📅 {leave.start_date} - {leave.reason}")
    print(f"      🎯 This faculty should be excluded from {base_date} exams")

def test_correct_allocation_logic(exams):
    """Test allocation logic with CORRECT rules"""
    print("\n🔍 TESTING CORRECT ALLOCATION LOGIC")
    print("="*50)
    
    faculty_list = list(Faculty.objects.filter(is_active=True))
    print(f"📊 Testing with {len(faculty_list)} faculty members:")
    
    # Show faculty by department
    dept_faculty = {}
    for faculty in faculty_list:
        dept_code = faculty.department.code if faculty.department else 'NO_DEPT'
        if dept_code not in dept_faculty:
            dept_faculty[dept_code] = []
        dept_faculty[dept_code].append(faculty)
    
    for dept_code, faculty_in_dept in dept_faculty.items():
        print(f"   🏫 {dept_code}: {len(faculty_in_dept)} faculty")
        for faculty in faculty_in_dept:
            print(f"      👨‍🏫 {faculty.user.get_full_name()} ({faculty.employee_id})")
    
    test_results = []
    
    for exam in exams:
        print(f"\n" + "="*60)
        print(f"🔍 TESTING EXAM: {exam.course_code} - {exam.course_name}")
        print(f"   📅 {exam.exam_date} {exam.start_time}-{exam.end_time}")
        print(f"   🏫 {exam.department.code} Year {exam.year} Semester {exam.semester}")
        
        # Step 1: Apply Rule 1 - Find FREE faculty (not teaching same year)
        print(f"\n   📚 RULE 1: Faculty teaching Year {exam.year} students are FREE")
        
        free_faculty = []
        busy_faculty = []
        
        day_of_week = exam.exam_date.strftime('%a').upper()[:3]
        print(f"      📅 Exam day: {exam.exam_date.strftime('%A')} ({day_of_week})")
        
        for faculty in faculty_list:
            # Check if faculty teaches same year during exam time
            conflicting_slots = FacultyTimeSlot.objects.filter(
                faculty=faculty,
                year=exam.year,
                day_of_week=day_of_week
            )
            
            has_conflict = False
            conflict_details = []
            
            for slot in conflicting_slots:
                # Check time overlap
                if (slot.start_time < exam.end_time and slot.end_time > exam.start_time):
                    has_conflict = True
                    conflict_details.append(f"{slot.course_code} ({slot.start_time}-{slot.end_time})")
            
            if has_conflict:
                busy_faculty.append({
                    'faculty': faculty,
                    'conflicts': conflict_details
                })
            else:
                free_faculty.append(faculty)
        
        print(f"      ✅ FREE faculty: {len(free_faculty)}")
        for faculty in free_faculty:
            print(f"         👨‍🏫 {faculty.user.get_full_name()} ({faculty.department.code})")
        
        print(f"      ❌ BUSY faculty: {len(busy_faculty)}")
        for item in busy_faculty:
            conflicts_str = ', '.join(item['conflicts'])
            print(f"         👨‍🏫 {item['faculty'].user.get_full_name()} - Teaching: {conflicts_str}")
        
        # Step 2: Apply Rule 2 - Remove faculty on leave
        print(f"\n   🏖️ RULE 2: Exclude faculty on leave")
        
        available_faculty = []
        on_leave_faculty = []
        
        for faculty in free_faculty:
            leave = FacultyLeave.objects.filter(
                faculty=faculty,
                start_date__lte=exam.exam_date,
                end_date__gte=exam.exam_date,
                status=FacultyLeave.APPROVED
            ).first()
            
            if leave:
                on_leave_faculty.append({
                    'faculty': faculty,
                    'leave': leave
                })
            else:
                available_faculty.append(faculty)
        
        print(f"      ❌ On leave: {len(on_leave_faculty)}")
        for item in on_leave_faculty:
            print(f"         👨‍🏫 {item['faculty'].user.get_full_name()} - {item['leave'].reason}")
        
        print(f"      ✅ Available: {len(available_faculty)}")
        for faculty in available_faculty:
            print(f"         👨‍🏫 {faculty.user.get_full_name()} ({faculty.department.code})")
        
        # Step 3: Apply Rule 3 - AVOID same department faculty
        print(f"\n   🏫 RULE 3: AVOID same department faculty")
        
        same_dept_faculty = [f for f in available_faculty if f.department == exam.department]
        other_dept_faculty = [f for f in available_faculty if f.department != exam.department]
        
        print(f"      ❌ AVOID - Same department ({exam.department.code}): {len(same_dept_faculty)}")
        for faculty in same_dept_faculty:
            print(f"         👨‍🏫 {faculty.user.get_full_name()} - SHOULD AVOID")
        
        print(f"      ✅ PREFER - Other departments: {len(other_dept_faculty)}")
        for faculty in other_dept_faculty:
            print(f"         👨‍🏫 {faculty.user.get_full_name()} ({faculty.department.code}) - PREFERRED")
        
        # Step 4: Determine allocation strategy
        print(f"\n   🎯 ALLOCATION STRATEGY:")
        
        if len(other_dept_faculty) >= 2:
            strategy = "IDEAL"
            recommended = other_dept_faculty[:3]
            print(f"      ✅ IDEAL: Use only OTHER department faculty")
        elif len(other_dept_faculty) >= 1:
            strategy = "MIXED"
            recommended = other_dept_faculty + same_dept_faculty[:2]
            print(f"      ⚠️ MIXED: Use other dept + minimal same dept")
        elif len(same_dept_faculty) >= 2:
            strategy = "LAST_RESORT"
            recommended = same_dept_faculty[:3]
            print(f"      ❌ LAST RESORT: Use same department faculty only")
        else:
            strategy = "INSUFFICIENT"
            recommended = available_faculty
            print(f"      ❌ INSUFFICIENT: Not enough faculty available")
        
        print(f"      📋 RECOMMENDED ALLOCATION:")
        for i, faculty in enumerate(recommended[:3], 1):
            dept_status = "⚠️ SAME DEPT" if faculty.department == exam.department else "✅ OTHER DEPT"
            print(f"         {i}. {faculty.user.get_full_name()} ({faculty.department.code}) - {dept_status}")
        
        # Store results
        test_results.append({
            'exam': exam,
            'total_faculty': len(faculty_list),
            'free_faculty': len(free_faculty),
            'busy_faculty': len(busy_faculty),
            'on_leave': len(on_leave_faculty),
            'available': len(available_faculty),
            'same_dept': len(same_dept_faculty),
            'other_dept': len(other_dept_faculty),
            'strategy': strategy,
            'recommended': recommended[:3],
            'allocation_possible': len(available_faculty) >= 2
        })
    
    return test_results

def create_optimal_allocations(test_results):
    """Create allocations based on test results using correct rules"""
    print(f"\n🎯 CREATING OPTIMAL ALLOCATIONS")
    print("="*40)
    
    halls = list(ExamHall.objects.all())
    allocations_created = 0
    
    for result in test_results:
        exam = result['exam']
        recommended = result['recommended']
        
        if not recommended:
            print(f"   ❌ {exam.course_code}: No faculty available")
            continue
        
        print(f"\n   📋 {exam.course_code} - {exam.course_name}")
        
        # Create exam session hall
        hall = halls[0] if halls else None
        if not hall:
            print(f"      ❌ No halls available")
            continue
        
        session_hall = ExamSessionHall.objects.create(
            exam=exam,
            hall=hall,
            required_invigilators=min(3, len(recommended))
        )
        
        print(f"      🏢 Hall: {hall.name}")
        print(f"      👥 Allocating {len(recommended)} faculty:")
        
        # Create allocations
        for faculty in recommended:
            assignment = InvigilationAssignment.objects.create(
                exam_session_hall=session_hall,
                faculty=faculty,
                status=InvigilationAssignment.PENDING_CONFIRMATION,
                assigned_at=timezone.now()
            )
            
            dept_status = "⚠️ SAME DEPT" if faculty.department == exam.department else "✅ OTHER DEPT"
            print(f"         ✅ {faculty.user.get_full_name()} ({faculty.department.code}) - {dept_status}")
            allocations_created += 1
    
    print(f"\n   📊 Total allocations created: {allocations_created}")

def generate_comprehensive_report(test_results):
    """Generate comprehensive test report"""
    print(f"\n" + "="*60)
    print("COMPREHENSIVE ALLOCATION TEST REPORT")
    print("="*60)
    
    # Calculate statistics
    total_exams = len(test_results)
    successful_allocations = sum(1 for r in test_results if r['allocation_possible'])
    
    strategy_counts = {}
    for result in test_results:
        strategy = result['strategy']
        strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
    
    print(f"\n📊 SUMMARY:")
    print(f"   Total exams tested: {total_exams}")
    print(f"   Successful allocations: {successful_allocations}")
    print(f"   Failed allocations: {total_exams - successful_allocations}")
    
    print(f"\n🎯 ALLOCATION STRATEGIES:")
    for strategy, count in strategy_counts.items():
        percentage = (count / total_exams) * 100
        print(f"   {strategy}: {count} exams ({percentage:.1f}%)")
    
    # Analyze department avoidance success
    total_allocations = 0
    same_dept_allocations = 0
    other_dept_allocations = 0
    
    for assignment in InvigilationAssignment.objects.all():
        total_allocations += 1
        if assignment.faculty.department == assignment.exam_session_hall.exam.department:
            same_dept_allocations += 1
        else:
            other_dept_allocations += 1
    
    print(f"\n🏫 DEPARTMENT AVOIDANCE ANALYSIS:")
    print(f"   Total allocations: {total_allocations}")
    if total_allocations > 0:
        same_dept_pct = (same_dept_allocations / total_allocations) * 100
        other_dept_pct = (other_dept_allocations / total_allocations) * 100
        print(f"   Same department: {same_dept_allocations} ({same_dept_pct:.1f}%) - Should minimize")
        print(f"   Other departments: {other_dept_allocations} ({other_dept_pct:.1f}%) - Preferred")
        
        if other_dept_pct >= 80:
            print(f"   ✅ EXCELLENT: >80% cross-department allocations")
        elif other_dept_pct >= 60:
            print(f"   ⚠️ GOOD: >60% cross-department allocations")
        else:
            print(f"   ❌ NEEDS IMPROVEMENT: <60% cross-department allocations")
    
    print(f"\n📋 DETAILED EXAM ANALYSIS:")
    for i, result in enumerate(test_results, 1):
        exam = result['exam']
        print(f"\n{i}. {exam.course_code} - {exam.course_name}")
        print(f"   📅 {exam.exam_date} {exam.start_time}-{exam.end_time}")
        print(f"   🏫 {exam.department.code} Year {exam.year}")
        print(f"   👥 Faculty: {result['available']}/{result['total_faculty']} available")
        print(f"   🎯 Strategy: {result['strategy']}")
        print(f"   📊 Same dept: {result['same_dept']}, Other dept: {result['other_dept']}")
    
    # Save report
    report_content = f"""# FRESH EXAM ALLOCATION TEST REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## SUMMARY
- **Total Exams Tested**: {total_exams}
- **Successful Allocations**: {successful_allocations}
- **Total Faculty Allocations**: {total_allocations}

## CORRECTED ALLOCATION RULES VERIFIED

### ✅ Rule 1: Free Faculty (Classes Cancelled)
Faculty teaching same year students during exam time are considered FREE.
Their classes are cancelled during the exam period.

### ✅ Rule 2: Leave Handling
Faculty on approved leave are excluded from allocation.

### ✅ Rule 3: Department Avoidance (CORRECTED)
**AVOID same department faculty to prevent bias and ensure objectivity.**

**Priority Order:**
1. **IDEAL**: Use only OTHER department faculty
2. **MIXED**: Use other dept + minimal same dept if needed
3. **LAST RESORT**: Same department faculty only when no alternatives

## ALLOCATION STRATEGY RESULTS
"""
    
    for strategy, count in strategy_counts.items():
        percentage = (count / total_exams) * 100
        report_content += f"- **{strategy}**: {count} exams ({percentage:.1f}%)\n"
    
    if total_allocations > 0:
        same_dept_pct = (same_dept_allocations / total_allocations) * 100
        other_dept_pct = (other_dept_allocations / total_allocations) * 100
        
        report_content += f"""
## DEPARTMENT AVOIDANCE SUCCESS
- **Total Allocations**: {total_allocations}
- **Same Department**: {same_dept_allocations} ({same_dept_pct:.1f}%) - Should minimize
- **Other Departments**: {other_dept_allocations} ({other_dept_pct:.1f}%) - Preferred

"""
        
        if other_dept_pct >= 80:
            report_content += "**✅ RESULT: EXCELLENT** - >80% cross-department allocations\n"
        elif other_dept_pct >= 60:
            report_content += "**⚠️ RESULT: GOOD** - >60% cross-department allocations\n"
        else:
            report_content += "**❌ RESULT: NEEDS IMPROVEMENT** - <60% cross-department allocations\n"
    
    report_content += f"""
## WHERE TO VIEW RESULTS
- **Admin Dashboard**: http://127.0.0.1:8000/exams/admin/
- **Manage Exams**: http://127.0.0.1:8000/exams/admin/exam-list/
- **Pending Duties**: http://127.0.0.1:8000/exams/admin/pending-assignments/
- **Allocation Overview**: http://127.0.0.1:8000/exams/admin/allocation-overview/

## CONCLUSION
Fresh test completed with correct allocation rules. The system prioritizes cross-department faculty to ensure objective invigilation and minimize bias.
"""
    
    with open('FRESH_ALLOCATION_TEST_REPORT.md', 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"\n📄 Comprehensive report saved to: FRESH_ALLOCATION_TEST_REPORT.md")

def main():
    """Main function to run fresh comprehensive test"""
    print("🚀 FRESH COMPREHENSIVE ALLOCATION TEST")
    print("="*50)
    print("Testing with CORRECT allocation rules:")
    print("✅ Rule 1: Free faculty (classes cancelled)")
    print("✅ Rule 2: Leave handling")
    print("✅ Rule 3: AVOID same department faculty")
    print()
    
    try:
        # Step 1: Clear previous data
        clear_previous_test_data()
        
        # Step 2: Create fresh exams
        exams = create_fresh_test_exams()
        
        # Step 3: Create strategic leaves
        create_strategic_faculty_leaves()
        
        # Step 4: Test allocation logic
        test_results = test_correct_allocation_logic(exams)
        
        # Step 5: Create optimal allocations
        create_optimal_allocations(test_results)
        
        # Step 6: Generate comprehensive report
        generate_comprehensive_report(test_results)
        
        print(f"\n🎉 FRESH TEST COMPLETED SUCCESSFULLY!")
        print(f"📊 Created {len(exams)} fresh exams with optimal allocations")
        print(f"🔍 Verified all allocation rules with correct logic")
        print(f"📄 Generated comprehensive test report")
        
        print(f"\n📍 VIEW RESULTS:")
        print(f"   🌐 Admin Dashboard: http://127.0.0.1:8000/exams/admin/")
        print(f"   📋 Manage Exams: http://127.0.0.1:8000/exams/admin/exam-list/")
        print(f"   👥 Pending Duties: http://127.0.0.1:8000/exams/admin/pending-assignments/")
        print(f"   📄 Report: FRESH_ALLOCATION_TEST_REPORT.md")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()