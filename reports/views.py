from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse
from .models import *
import matplotlib.pyplot as plt
import matplotlib as mt
mt.use('Agg')
import base64
from io import BytesIO


class EstudiantePDFView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        notas = Nota.objects.select_related('estudiante', 'materia').all()

        reporte = {}
        for nota in notas:
            estudiante = reporte.setdefault(nota.estudiante.nombre, {})
            materia = estudiante.setdefault(nota.materia.nombre, {'parciales': [None, None, None, None]})
            materia['parciales'][nota.parcial - 1] = nota.nota

        graficos = {}
        for estudiante, materias in reporte.items():
            plt.figure(figsize=(10, 6))
            for materia, datos in materias.items():
                plt.plot(
                    range(1, 5),
                    datos['parciales'],
                    marker='o',
                    label=materia
                )
            plt.title(f'Evolución de Notas - {estudiante}')
            plt.xlabel('Parciales')
            plt.ylabel('Nota')
            plt.xticks(range(1, 5), ['Parcial 1', 'Parcial 2', 'Parcial 3', 'Parcial 4'])
            plt.legend()

            # Convertir el gráfico en imagen base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            graficos[estudiante] = base64.b64encode(buffer.read()).decode('utf-8')
            buffer.close()
            plt.close()

        context = {'reporte': reporte, 'graficos': graficos}
        html_content = render_to_string('report.html', context)

        pdf = BytesIO()
        pisa_status = pisa.CreatePDF(BytesIO(html_content.encode('utf-8')), dest=pdf)
        pdf.seek(0)

        if pisa_status.err:
            return Response({"detail": "Error al generar el PDF"}, status=500)

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_estudiantes.pdf"'
        return response
