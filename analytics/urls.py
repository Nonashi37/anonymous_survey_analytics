# from django.urls import path
# from . import views
#
# app_name = 'analytics'
#
# urlpatterns = [
#     path('', views.dashboard, name='dashboard'),
#     path('professor/<int:professor_id>/', views.professor_detail, name='professor_detail'),
#     path('compare/', views.compare_professors, name='compare_professors'),
# ]

from django.urls import path
from . import views
from .test_views import test_dashboard, professor_detail_test

app_name = 'analytics'

urlpatterns = [
    path('test/', test_dashboard, name='test_dashboard'),
    path('test/professor/<int:professor_id>/', professor_detail_test, name='professor_test'),
]