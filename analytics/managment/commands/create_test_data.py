import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from analytics.models import TempProfessor, TempSurveyResponse, ProfessorAnalytics, DepartmentAnalytics, DailyAnalytics


class Command(BaseCommand):
    help = 'Generate test data for analytics demonstration'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Creating EPIC test data for your analytics!")

        # Clear existing test data
        TempProfessor.objects.all().delete()
        TempSurveyResponse.objects.all().delete()
        ProfessorAnalytics.objects.all().delete()
        DepartmentAnalytics.objects.all().delete()
        DailyAnalytics.objects.all().delete()

        # Create professors
        professors_data = [
            {"name": "Dr. Sarah Johnson", "email": "s.johnson@uni.edu", "department": "Computer Science"},
            {"name": "Prof. Michael Chen", "email": "m.chen@uni.edu", "department": "Computer Science"},
            {"name": "Dr. Emily Rodriguez", "email": "e.rodriguez@uni.edu", "department": "Mathematics"},
            {"name": "Prof. David Wilson", "email": "d.wilson@uni.edu", "department": "Mathematics"},
            {"name": "Dr. Lisa Thompson", "email": "l.thompson@uni.edu", "department": "Physics"},
            {"name": "Prof. James Anderson", "email": "j.anderson@uni.edu", "department": "Physics"},
            {"name": "Dr. Maria Garcia", "email": "m.garcia@uni.edu", "department": "Chemistry"},
            {"name": "Prof. Robert Taylor", "email": "r.taylor@uni.edu", "department": "Chemistry"},
            {"name": "Dr. Jennifer Lee", "email": "j.lee@uni.edu", "department": "Biology"},
            {"name": "Prof. Christopher Brown", "email": "c.brown@uni.edu", "department": "Biology"},
        ]

        professors = []
        for prof_data in professors_data:
            professor = TempProfessor.objects.create(**prof_data)
            professors.append(professor)
            self.stdout.write(f"✅ Created professor: {professor.name}")

        # Create survey responses for the last 30 days
        feedback_templates = [
            # Positive feedback
            "Excellent professor! Very clear explanations and helpful.",
            "Great teaching style, makes complex topics easy to understand.",
            "Very knowledgeable and passionate about the subject.",
            "Helpful office hours and responds quickly to emails.",
            "Engaging lectures with real-world examples.",

            # Neutral feedback
            "Good professor overall, lectures could be more interactive.",
            "Decent teaching, but sometimes goes too fast.",
            "Fair grading and clear expectations.",
            "Could use more examples in class.",
            "Okay professor, nothing special but gets the job done.",

            # Negative feedback
            "Lectures are boring and hard to follow.",
            "Very disorganized and unclear assignments.",
            "Harsh grading with little feedback.",
            "Difficult to understand with heavy accent.",
            "Not helpful during office hours.",
        ]

        total_responses = 0

        for day_offset in range(30):  # Last 30 days
            current_date = timezone.now().date() - timedelta(days=day_offset)
            daily_responses = 0
            daily_total_rating = 0

            for professor in professors:
                # Each professor gets 5-25 responses per day (random)
                num_responses = random.randint(5, 25)

                for _ in range(num_responses):
                    # Create realistic rating distribution
                    # Better professors get higher ratings
                    if professor.name in ["Dr. Sarah Johnson", "Prof. Michael Chen", "Dr. Emily Rodriguez"]:
                        # Top performers - mostly 4s and 5s
                        rating = random.choices([3, 4, 5], weights=[10, 40, 50])[0]
                        feedback = random.choice(feedback_templates[:5])  # Positive feedback
                    elif professor.name in ["Prof. David Wilson", "Dr. Lisa Thompson", "Prof. James Anderson"]:
                        # Good performers - mostly 3s and 4s
                        rating = random.choices([2, 3, 4, 5], weights=[10, 40, 40, 10])[0]
                        feedback = random.choice(feedback_templates[5:10])  # Neutral feedback
                    else:
                        # Average performers - mixed ratings
                        rating = random.choices([1, 2, 3, 4, 5], weights=[5, 15, 50, 25, 5])[0]
                        feedback = random.choice(feedback_templates[10:])  # Mixed feedback

                    # Sometimes no text feedback
                    if random.random() > 0.7:
                        feedback = ""

                    TempSurveyResponse.objects.create(
                        professor_id=professor.id,
                        rating=rating,
                        text_feedback=feedback,
                        created_at=timezone.make_aware(
                            datetime.combine(current_date, datetime.min.time())
                        )
                    )

                    daily_responses += 1
                    daily_total_rating += rating
                    total_responses += 1

            # Create daily analytics
            if daily_responses > 0:
                DailyAnalytics.objects.create(
                    date=current_date,
                    total_surveys=len(professors),  # Number of professors surveyed
                    total_responses=daily_responses,
                    average_rating=daily_total_rating / daily_responses,
                    response_rate=random.uniform(0.6, 0.9)  # Random response rate
                )

        self.stdout.write(f"🎉 Created {total_responses} survey responses!")
        self.stdout.write("🔥 Now run the analytics processor to see the magic!")
        self.stdout.write("Run: python manage.py process_test_analytics")

