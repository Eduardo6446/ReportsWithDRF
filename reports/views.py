from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse
from .models import *

class EstudiantePDFView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # Obtener los datos de los estudiantes
        notas = nota.objects.select_related('estudiante', 'materia').all()
        context = {'notas': notas}

        # Renderizar el HTML con los datos
        html_content = render_to_string('report.html', context)

        # Crear el PDF
        pdf = BytesIO()
        pisa_status = pisa.CreatePDF(BytesIO(html_content.encode('utf-8')), dest=pdf)
        pdf.seek(0)

        if pisa_status.err:
            return Response({"detail": "Error al generar el PDF"}, status=500)

        # Devolver el PDF como respuesta
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_estudiantes.pdf"'
        return response
