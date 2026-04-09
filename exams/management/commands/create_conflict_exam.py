"""
Creates a CSE exam on Monday 09:00-12:00 that conflicts with every seeded faculty's timetable.
Run: python manage.py create_conflict_exam
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Create a conflict exam for demo/viva purposes"

    def handle(self, *args, **options):
        from exams.models import Department, Exam

        dept = Department.objects.get(code="CSE")
        admin = User.objects.filter(is_staff=True).first()

        exam, created = Exam.objects.get_or_create(
            course_code="CS501",
            exam_date="2026-04-27",  # Monday
            department=dept,
            defaults={
                "course_name": "Advanced Algorithms",
                "exam_type": "END",
                "year": 4,
                "semester": 1,
                "start_time": "09:00",
                "end_time": "12:00",
                "created_by": admin,
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(
                "Conflict exam created: CS501 - Advanced Algorithms | CSE Y4S1 | Mon 27-Apr-2026 | 09:00-12:00"
            ))
        else:
            self.stdout.write("Exam already exists.")
