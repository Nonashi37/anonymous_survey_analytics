from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('professor/<int:professor_id>/', views.professor_detail, name='professor_detail'),
    path('compare/', views.compare_professors, name='compare_professors'),
]