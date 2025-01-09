from django.urls import path
from .views import EstudiantePDFView

urlpatterns = [
    path('', EstudiantePDFView.as_view(), name='estudiante-pdf'),
]
