"""
Management command to seed demo faculty, timetables, exam halls, exams and duties.
Run once on production: python manage.py seed_demo_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, time, timedelta, datetime

User = get_user_model()


FACULTY_DATA = [
    # (first, last, email, emp_id, dept_code, cabin_block, cabin_room, phone)
    ("Ravi",      "Kumar",    "ravi.kumar@college.edu",    "EMP001", "ECE",   "B", "B-101", "9000000001"),
    ("Priya",     "Sharma",   "priya.sharma@college.edu",  "EMP002", "EEE",   "B", "B-102", "9000000002"),
    ("Suresh",    "Reddy",    "suresh.reddy@college.edu",  "EMP003", "MECH",  "C", "C-201", "9000000003"),
    ("Anitha",    "Nair",     "anitha.nair@college.edu",   "EMP004", "CIVIL", "C", "C-202", "9000000004"),
    ("Venkat",    "Rao",      "venkat.rao@college.edu",    "EMP005", "ECE",   "B", "B-103", "9000000005"),
    ("Deepa",     "Menon",    "deepa.menon@college.edu",   "EMP006", "EEE",   "A", "A-101", "9000000006"),
    ("Kiran",     "Babu",     "kiran.babu@college.edu",    "EMP007", "MECH",  "A", "A-102", "9000000007"),
    ("Lakshmi",   "Iyer",     "lakshmi.iyer@college.edu",  "EMP008", "CIVIL", "D", "D-101", "9000000008"),
    ("Arun",      "Pillai",   "arun.pillai@college.edu",   "EMP009", "ECE",   "D", "D-102", "9000000009"),
    ("Meena",     "Krishnan", "meena.krishnan@college.edu","EMP010", "EEE",   "B", "B-201", "9000000010"),
]

# Timetable slots per faculty: (day, start, end, dept_code, course_code, course_name, year, sem, is_lab)
TIMETABLE_DATA = {
    "EMP001": [
        ("MON", "09:00", "10:00", "ECE", "EC301", "Digital Electronics",       3, 1, False),
        ("WED", "11:00", "12:00", "ECE", "EC301", "Digital Electronics",       3, 1, False),
        ("FRI", "10:00", "11:00", "ECE", "EC201", "Circuit Theory",            2, 1, False),
    ],
    "EMP002": [
        ("TUE", "09:00", "10:00", "EEE", "EE301", "Power Systems",             3, 1, False),
        ("THU", "10:00", "11:00", "EEE", "EE201", "Electrical Machines",       2, 1, False),
        ("FRI", "14:00", "16:00", "EEE", "EE301L","Power Systems Lab",         3, 1, True),
    ],
    "EMP003": [
        ("MON", "10:00", "11:00", "MECH","ME301", "Thermodynamics",            3, 1, False),
        ("WED", "09:00", "10:00", "MECH","ME201", "Fluid Mechanics",           2, 1, False),
        ("THU", "14:00", "16:00", "MECH","ME301L","Thermodynamics Lab",        3, 1, True),
    ],
    "EMP004": [
        ("TUE", "11:00", "12:00", "CIVIL","CE301","Structural Analysis",       3, 1, False),
        ("FRI", "09:00", "10:00", "CIVIL","CE201","Surveying",                 2, 1, False),
        ("WED", "14:00", "16:00", "CIVIL","CE301L","Structures Lab",           3, 1, True),
    ],
    "EMP005": [
        ("MON", "11:00", "12:00", "ECE", "EC401", "VLSI Design",               4, 1, False),
        ("TUE", "10:00", "11:00", "ECE", "EC301", "Digital Electronics",       3, 1, False),
        ("THU", "09:00", "10:00", "ECE", "EC101", "Basic Electronics",         1, 1, False),
    ],
    "EMP006": [
        ("MON", "09:00", "10:00", "EEE", "EE401", "High Voltage Engineering",  4, 1, False),
        ("WED", "10:00", "11:00", "EEE", "EE101", "Basic Electrical",          1, 1, False),
        ("FRI", "11:00", "12:00", "EEE", "EE301", "Power Systems",             3, 1, False),
    ],
    "EMP007": [
        ("TUE", "09:00", "10:00", "MECH","ME401", "CAD/CAM",                   4, 1, False),
        ("THU", "11:00", "12:00", "MECH","ME101", "Engineering Mechanics",     1, 1, False),
        ("FRI", "10:00", "11:00", "MECH","ME201", "Fluid Mechanics",           2, 1, False),
    ],
    "EMP008": [
        ("MON", "14:00", "15:00", "CIVIL","CE401","Foundation Engineering",    4, 1, False),
        ("WED", "11:00", "12:00", "CIVIL","CE101","Engineering Drawing",       1, 1, False),
        ("THU", "10:00", "11:00", "CIVIL","CE201","Surveying",                 2, 1, False),
    ],
    "EMP009": [
        ("TUE", "14:00", "15:00", "ECE", "EC201", "Circuit Theory",            2, 1, False),
        ("WED", "09:00", "10:00", "ECE", "EC101", "Basic Electronics",         1, 1, False),
        ("FRI", "11:00", "12:00", "ECE", "EC401", "VLSI Design",               4, 1, False),
    ],
    "EMP010": [
        ("MON", "10:00", "11:00", "EEE", "EE201", "Electrical Machines",       2, 1, False),
        ("TUE", "11:00", "12:00", "EEE", "EE401", "High Voltage Engineering",  4, 1, False),
        ("THU", "14:00", "16:00", "EEE", "EE201L","Electrical Machines Lab",   2, 1, True),
    ],
}

# Exam halls to create if not present
HALLS_DATA = [
    # (name, block, floor, capacity)
    ("Hall-101", "A", "1", 60),
    ("Hall-102", "A", "1", 60),
    ("Hall-201", "B", "2", 80),
    ("Hall-202", "B", "2", 80),
    ("Hall-301", "C", "3", 50),
    ("Hall-302", "D", "3", 50),
]

# Exams to create (course_code, course_name, type, dept_code, year, sem, date, start, end)
EXAMS_DATA = [
    ("CS301", "Data Structures",        "MID", "CSE",   3, 1, "2026-04-20", "09:00", "12:00"),
    ("CS201", "Operating Systems",      "MID", "CSM",   2, 1, "2026-04-21", "09:00", "12:00"),
    ("CS401", "Machine Learning",       "END", "CSD",   4, 1, "2026-04-22", "14:00", "17:00"),
    ("CS101", "Programming Fundamentals","TEST","CSE",  1, 1, "2026-04-23", "09:00", "11:00"),
]


class Command(BaseCommand):
    help = "Seed demo faculty, timetables, exam halls, exams and invigilation duties"

    def handle(self, *args, **options):
        from accounts.models import Faculty
        from exams.models import Department, ExamHall, Exam, ExamSessionHall, InvigilationAssignment
        from timetable.models import FacultyTimeSlot, Course

        self.stdout.write("--- Seeding demo data ---")

        # 1. Ensure departments exist
        dept_map = {}
        for code, name in [
            ("CSE", "Computer Science and Engineering"),
            ("CSM", "Computer Science and AI/ML"),
            ("CSD", "Computer Science and Data Science"),
            ("ECE", "Electronics and Communication Engineering"),
            ("EEE", "Electrical and Electronics Engineering"),
            ("MECH", "Mechanical Engineering"),
            ("CIVIL", "Civil Engineering"),
        ]:
            dept, _ = Department.objects.get_or_create(code=code, defaults={"name": name})
            dept_map[code] = dept
        self.stdout.write(self.style.SUCCESS(f"  Departments ready: {len(dept_map)}"))

        # 2. Create faculty
        faculty_map = {}
        created_count = 0
        for first, last, email, emp_id, dept_code, cabin_block, cabin_room, phone in FACULTY_DATA:
            if Faculty.objects.filter(employee_id=emp_id).exists():
                faculty_map[emp_id] = Faculty.objects.get(employee_id=emp_id)
                continue
            username = f"{first.lower()}.{last.lower()}"
            # make username unique
            base = username
            i = 1
            while User.objects.filter(username=username).exists():
                username = f"{base}{i}"
                i += 1
            user = User.objects.create_user(
                username=username,
                email=email,
                password="Faculty@123",
                first_name=first,
                last_name=last,
                is_staff=False,
            )
            faculty = Faculty.objects.create(
                user=user,
                employee_id=emp_id,
                department=dept_map[dept_code],
                cabin_block=cabin_block,
                cabin_room=cabin_room,
                phone_number=phone,
                must_change_password=False,
            )
            faculty_map[emp_id] = faculty
            created_count += 1
        self.stdout.write(self.style.SUCCESS(f"  Faculty created: {created_count} new (skipped existing)"))

        # 3. Create timetable slots
        slot_count = 0
        for emp_id, slots in TIMETABLE_DATA.items():
            faculty = faculty_map.get(emp_id)
            if not faculty:
                continue
            for day, start, end, dept_code, code, name, year, sem, is_lab in slots:
                dept = dept_map.get(dept_code)
                exists = FacultyTimeSlot.objects.filter(
                    faculty=faculty, day_of_week=day,
                    start_time=start, end_time=end
                ).exists()
                if not exists:
                    FacultyTimeSlot.objects.create(
                        faculty=faculty,
                        day_of_week=day,
                        start_time=start,
                        end_time=end,
                        department=dept,
                        course_code=code,
                        course_name=name,
                        year=year,
                        semester=sem,
                        is_lab=is_lab,
                    )
                    slot_count += 1
        self.stdout.write(self.style.SUCCESS(f"  Timetable slots created: {slot_count}"))

        # 4. Create exam halls
        hall_map = {}
        hall_count = 0
        for name, block, floor, capacity in HALLS_DATA:
            hall, created = ExamHall.objects.get_or_create(
                name=name, block=block,
                defaults={"floor": floor, "capacity": capacity, "is_active": True}
            )
            hall_map[name] = hall
            if created:
                hall_count += 1
        self.stdout.write(self.style.SUCCESS(f"  Exam halls created: {hall_count} new"))

        # 5. Create exams
        admin_user = User.objects.filter(is_staff=True).first()
        exam_map = {}
        exam_count = 0
        for code, name, etype, dept_code, year, sem, edate, start, end in EXAMS_DATA:
            dept = dept_map[dept_code]
            exam, created = Exam.objects.get_or_create(
                course_code=code,
                exam_date=edate,
                department=dept,
                defaults={
                    "course_name": name,
                    "exam_type": etype,
                    "year": year,
                    "semester": sem,
                    "start_time": start,
                    "end_time": end,
                    "created_by": admin_user,
                }
            )
            exam_map[code] = exam
            if created:
                exam_count += 1
        self.stdout.write(self.style.SUCCESS(f"  Exams created: {exam_count} new"))

        # 6. Configure halls for each exam and auto-assign duties
        assignment_count = 0
        for code, exam in exam_map.items():
            # Assign 2 halls per exam
            halls = list(ExamHall.objects.filter(is_active=True)[:2])
            for hall in halls:
                session, _ = ExamSessionHall.objects.get_or_create(
                    exam=exam, hall=hall,
                    defaults={"required_invigilators": 2}
                )
                # Pick eligible faculty (different dept, not on leave, no clash)
                eligible = Faculty.objects.filter(is_active=True).exclude(
                    department=exam.department
                ).exclude(
                    invigilation_assignments__exam_session_hall__exam=exam
                )[:2]

                for faculty in eligible:
                    if InvigilationAssignment.objects.filter(
                        exam_session_hall__exam=exam, faculty=faculty
                    ).exists():
                        continue
                    exam_start_dt = datetime.combine(exam.exam_date, exam.start_time)
                    deadline = timezone.make_aware(exam_start_dt) - timedelta(hours=1, minutes=30)
                    InvigilationAssignment.objects.create(
                        exam_session_hall=session,
                        faculty=faculty,
                        status=InvigilationAssignment.PENDING_CONFIRMATION,
                        confirmation_deadline=deadline,
                        notification_sent_at=timezone.now(),
                    )
                    assignment_count += 1

        self.stdout.write(self.style.SUCCESS(f"  Invigilation assignments created: {assignment_count}"))
        self.stdout.write(self.style.SUCCESS("--- Done! All demo data seeded successfully ---"))
        self.stdout.write("")
        self.stdout.write("Faculty login credentials (all same password):")
        self.stdout.write("  Password: Faculty@123")
        for first, last, email, emp_id, *_ in FACULTY_DATA:
            username = f"{first.lower()}.{last.lower()}"
            self.stdout.write(f"  {username} / {email}")
