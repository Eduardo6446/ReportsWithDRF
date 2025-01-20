

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
    
class Nota(models.Model):
    SEMESTRE_CHOICES = [
        (1, 'Primer Semestre'),
        (2, 'Segundo Semestre'),
    ]
    PARCIAL_CHOICES = [
        (1, 'Primer Parcial'),
        (2, 'Segundo Parcial'),
        (3, 'Tercer Parcial'),
        (4, 'Cuarto Parcial'),
    ]

    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    nota = models.FloatField()
    semestre = models.PositiveSmallIntegerField(choices=SEMESTRE_CHOICES, null=True)
    parcial = models.PositiveSmallIntegerField(choices=PARCIAL_CHOICES, null=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.estudiante.nombre} - {self.materia.nombre} (Semestre {self.semestre}, Parcial {self.parcial})"
