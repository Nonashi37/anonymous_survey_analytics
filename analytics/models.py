
# Problems that MY highnest have to solve somehow :)
# # We'll use string references for now - safer approach!
# # from surveys.models import Professor, Course, Survey, SurveyResponse
# makeing this more flexeble broh from surveys.models import Professor, Course, Survey, SurveyResponse
# this solution's now independent,flexible, testable, once my not as smart as 'me' backend friend has the survey models ready. I'll create a simple connector function

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class DailyAnalytics(models.Model):
    """Store daily aggregated analytics"""
    date = models.DateField(unique=True)
    total_surveys = models.IntegerField(default=0)
    total_responses = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    response_rate = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analytics for {self.date}"


class ProfessorAnalytics(models.Model):
    """Analytics for individual professors - using ID reference for flexibility"""
    professor_id = models.IntegerField()  # Reference by ID
    professor_name = models.CharField(max_length=200, blank=True)  # Cache the name
    date = models.DateField()
    total_responses = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    rating_distribution = models.JSONField(default=dict)  # {1: 5, 2: 10, 3: 20, etc.}
    sentiment_score = models.FloatField(default=0.0)  # -1 to 1
    common_keywords = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['professor_id', 'date']
        indexes = [
            models.Index(fields=['professor_id', 'date']),
        ]

    def __str__(self):
        return f"{self.professor_name} - {self.date}"


class DepartmentAnalytics(models.Model):
    """Department-level analytics"""
    department = models.CharField(max_length=100)
    date = models.DateField()
    total_responses = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    top_professors = models.JSONField(default=list)
    bottom_professors = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['department', 'date']

    def __str__(self):
        return f"{self.department} - {self.date}"


class AnalyticsReport(models.Model):
    """Store generated reports"""
    name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=50)  # 'professor', 'department', 'comparative'
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.report_type}"


# Temporary models for testing - you can remove these later
class TempProfessor(models.Model):
    """Temporary professor model for testing"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    department = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TempSurveyResponse(models.Model):
    """Temporary survey response for testing"""
    professor_id = models.IntegerField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    text_feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response for Professor {self.professor_id} - Rating: {self.rating}"