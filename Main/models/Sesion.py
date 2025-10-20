from django.db import models
from .Usuario import Usuario


class Sesion(models.Model):
    usuario = models.ForeignKey(Usuario, primary_key=True, on_delete=models.CASCADE)
    fechaInicio = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def buscarUsuarioLogueado(self):
        return self.usuario.getEmpleado()
