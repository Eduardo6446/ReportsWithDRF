

from django.db import models

class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    fecha_nacimiento = models.DateField()
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    creditos = models.IntegerField()
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
class nota(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    nota = models.FloatField()
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.estudiante.nombre + ' - ' + self.materia.nombre