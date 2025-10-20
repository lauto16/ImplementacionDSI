from django.db import models
from .Empleado import Empleado

class Usuario(models.Model):
    contrasenia = models.CharField(max_length=100)
    nombreUsuario = models.CharField(max_length=100)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

    def getEmpleado(self):
        return self.empleado

