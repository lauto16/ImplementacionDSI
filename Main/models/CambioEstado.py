from django.db import models
from .Estado import Estado
from .Empleado import Empleado


class CambioEstado(models.Model):
    fechaHoraInicio = models.DateTimeField(null=True, blank=True)
    fechaHoraFin = models.DateTimeField(null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, null=False, db_column='estado_nombreEstado',)
    responsableInspeccion = models.ForeignKey(
        Empleado, on_delete=models.SET_NULL, null=True, default=None
    )

    def esActual(self) -> bool:
        return not self.fechaHoraFin

    def setFechaHoraFin(self, fecha_actual) -> None:
        self.fechaHoraFin = fecha_actual
        self.save()
