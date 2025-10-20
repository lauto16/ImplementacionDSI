from django.db import models


class Empleado(models.Model):
    apellido = models.CharField(max_length=100)
    mail = models.EmailField()
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)

