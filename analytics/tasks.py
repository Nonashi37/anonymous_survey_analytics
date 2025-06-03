from celery import shared_task
from django.utils import timezone
from .analyzers import SurveyAnalyzer
from surveys.models import Professor


@shared_task
def run_daily_analytics():
    """Daily task to process analytics"""
    today = timezone.now().date()
    analyzer = SurveyAnalyzer(date=today)

    # Process all professors
    professors = Professor.objects.all()
    for professor in professors:
        try:
            analyzer.analyze_professor(professor.id)
        except Exception as e:
            print(f"Error analyzing professor {professor.id}: {e}")

    # Process all departments
    departments = Professor.objects.values_list('department', flat=True).distinct()
    for department in departments:
        try:
            analyzer.analyze_department(department)
        except Exception as e:
            print(f"Error analyzing department {department}: {e}")

    print(f"Daily analytics completed for {today}")