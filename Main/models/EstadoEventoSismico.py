from abc import ABC, abstractmethod
from django.db import models

from .Empleado import Empleado
from .Estado import Estado


class EstadoEventoSismico(models.Model):
    """
    Clase padre para implemetar State
    """
    ambito = 'eventoSismico'
    nombre = ''

    class Meta:
        abstract = True

    def bloquear(self, evento, fecha_actual, empleado):
        """Bloquea el evento (si el estado lo permite)."""
        pass

    def confirmar(self, evento, empleado):
        """Confirma el evento (si el estado lo permite)."""
        pass

    def rechazar(self, evento, empleado):
        """Rechaza el evento (si el estado lo permite)."""
        pass

    def crear_estado(self, evento):
        """Crea un nuevo estado asociado al evento."""
        pass


class Confirmado(EstadoEventoSismico):
    nombre = models.ForeignKey(Estado, default=8, on_delete=models.CASCADE)


class Rechazado():
    nombre = models.ForeignKey(Estado, default=9, on_delete=models.CASCADE)


class BloqueadoEnRevision(EstadoEventoSismico):
    nombre = models.ForeignKey(Estado, default=10, on_delete=models.CASCADE)

    def confirmar(self) -> None:
        pass

    def rechazar(self) -> None:
        pass


class Autodetectado(EstadoEventoSismico):

    nombre = models.ForeignKey(Estado, default=7, on_delete=models.CASCADE)

    def bloquear(self, fecha_actual, empleado: Empleado) -> BloqueadoEnRevision:
        # Setear el cambio de estado etc, etc y todas las cosas relativas al bloqueo
        return BloqueadoEnRevision()
