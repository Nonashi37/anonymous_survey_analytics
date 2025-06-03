from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import ProfessorAnalytics, DepartmentAnalytics, DailyAnalytics
from .analyzers import SurveyAnalyzer, ComparativeAnalyzer
from .visualizers import ChartGenerator
from surveys.models import Professor, Course


@staff_member_required
def dashboard(request):
    """Main analytics dashboard"""
    # Get recent analytics data
    recent_date = timezone.now().date()
    daily_analytics = DailyAnalytics.objects.filter(
        date__gte=recent_date - timedelta(days=30)
    ).order_by('-date')

    # Get top performers
    top_professors = ProfessorAnalytics.objects.filter(
        date=recent_date
    ).order_by('-average_rating')[:10]

    chart_gen = ChartGenerator()

    context = {
        'daily_analytics': daily_analytics,
        'top_professors': top_professors,
        'total_surveys': sum(d.total_surveys for d in daily_analytics),
        'avg_rating': sum(d.average_rating for d in daily_analytics) / len(daily_analytics) if daily_analytics else 0,
    }

    return render(request, 'analytics/dashboard.html', context)


@staff_member_required
def professor_detail(request, professor_id):
    """Detailed analytics for a specific professor"""
    professor = get_object_or_404(Professor, id=professor_id)

    # Get professor analytics for the last 30 days
    analytics_data = ProfessorAnalytics.objects.filter(
        professor=professor,
        date__gte=timezone.now().date() - timedelta(days=30)
    ).order_by('-date')

    chart_gen = ChartGenerator()

    # Generate charts
    if analytics_data.exists():
        latest_analytics = analytics_data.first()
        rating_chart = chart_gen.create_rating_distribution_chart(
            latest_analytics.rating_distribution
        )
        sentiment_gauge = chart_gen.create_sentiment_gauge(
            latest_analytics.sentiment_score
        )
    else:
        rating_chart = None
        sentiment_gauge = None

    context = {
        'professor': professor,
        'analytics_data': analytics_data,
        'rating_chart': rating_chart,
        'sentiment_gauge': sentiment_gauge,
    }

    return render(request, 'analytics/professor_detail.html', context)


@staff_member_required
def compare_professors(request):
    """Compare multiple professors"""
    if request.method == 'POST':
        professor_ids = request.POST.getlist('professors')
        start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.POST['end_date'], '%Y-%m-%d').date()

        analyzer = ComparativeAnalyzer()
        comparison_data = analyzer.compare_professors(professor_ids, start_date, end_date)

        chart_gen = ChartGenerator()
        comparison_chart = chart_gen.create_professor_comparison_chart(comparison_data)

        return JsonResponse({
            'chart': comparison_chart,
            'data': comparison_data
        })

    professors = Professor.objects.all()
    return render(request, 'analytics/compare_professors.html', {'professors': professors})