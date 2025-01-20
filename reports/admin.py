from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Estudiante)
admin.site.register(Materia)
admin.site.register(Nota)
