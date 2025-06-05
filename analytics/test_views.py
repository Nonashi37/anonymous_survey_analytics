from django.shortcuts import render
from django.http import JsonResponse
from .models import ProfessorAnalytics, DepartmentAnalytics, DailyAnalytics, TempProfessor
from django.utils import timezone
from datetime import timedelta


def test_dashboard(request):
    """Quick test dashboard to see your analytics in action!"""

    # Get recent data
    recent_analytics = DailyAnalytics.objects.all().order_by('-date')[:10]
    top_professors = ProfessorAnalytics.objects.filter(
        date=timezone.now().date()
    ).order_by('-average_rating')[:5]

    # Get department performance
    departments = DepartmentAnalytics.objects.filter(
        date=timezone.now().date()
    ).order_by('-average_rating')

    context = {
        'recent_analytics': recent_analytics,
        'top_professors': top_professors,
        'departments': departments,
        'total_professors': TempProfessor.objects.count(),
    }

    return render(request, 'analytics/test_dashboard.html', context)


def professor_detail_test(request, professor_id):
    """Test view for individual professor analytics"""
    professor = TempProfessor.objects.get(id=professor_id)

    # Get analytics for last 7 days
    analytics = ProfessorAnalytics.objects.filter(
        professor_id=professor_id,
        date__gte=timezone.now().date() - timedelta(days=7)
    ).order_by('-date')

    context = {
        'professor': professor,
        'analytics': analytics,
    }

    return render(request, 'analytics/professor_test.html', context)