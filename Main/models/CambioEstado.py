from django.db import models
from .EstadoEventoSismico import EstadoEventoSismico
from .Empleado import Empleado


class CambioEstado(models.Model):
    fechaHoraInicio = models.DateTimeField(null=True, blank=True)
    fechaHoraFin = models.DateTimeField(null=True, blank=True)
    estado = models.ForeignKey(EstadoEventoSismico, on_delete=models.CASCADE, null=False)
    responsableInspeccion = models.ForeignKey(
        Empleado, on_delete=models.SET_NULL, null=True, default=None
    )

    def esActual(self) -> bool:
        return not self.fechaHoraFin

    def setFechaHoraFin(self, fecha_actual) -> None:
        self.fechaHoraFin = fecha_actual
        self.save()
