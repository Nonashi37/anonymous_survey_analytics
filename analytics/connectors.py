# # analytics/connectors.py
# def get_professor_data(professor_id):
#     """Connect to actual professor model when ready"""
#     try:
#         from surveys.models import Professor
#         return Professor.objects.get(id=professor_id)
#     except ImportError:
#         # Fallback to temp model
#         from .models import TempProfessor
#         return TempProfessor.objects.get(id=professor_id)