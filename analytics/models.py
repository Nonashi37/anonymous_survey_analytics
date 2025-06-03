from django.db import models
from django.contrib.auth.models import User
# Problems that MY highnest have to solve somehow :)
# # We'll use string references for now - safer approach!
# # from surveys.models import Professor, Course, Survey, SurveyResponse
from surveys.models import Professor, Course, Survey, SurveyResponse


class DailyAnalytics(models.Model):
    """Store daily aggregated analytics"""
    date = models.DateField(unique=True)
    total_surveys = models.IntegerField(default=0)
    total_responses = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    response_rate = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)


class ProfessorAnalytics(models.Model):
    """Analytics for individual professors"""
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    date = models.DateField()
    total_responses = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    rating_distribution = models.JSONField(default=dict)  # {1: 5, 2: 10, 3: 20, etc.}
    sentiment_score = models.FloatField(default=0.0)  # -1 to 1
    common_keywords = models.JSONField(default=list)

    class Meta:
        unique_together = ['professor', 'date']


class DepartmentAnalytics(models.Model):
    """Department-level analytics"""
    department = models.CharField(max_length=100)
    date = models.DateField()
    total_responses = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    top_professors = models.JSONField(default=list)
    bottom_professors = models.JSONField(default=list)

    class Meta:
        unique_together = ['department', 'date']


class AnalyticsReport(models.Model):
    """Store generated reports"""
    name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=50)  # 'professor', 'department', 'comparative'
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)