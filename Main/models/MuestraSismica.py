from django.db import models
from .DetalleMuestraSismica import DetalleMuestraSismica


class MuestraSismica(models.Model):
    fechaHoraMuestra = models.DateTimeField(null=True, blank=True)
    detalleMuestraSismica = models.ManyToManyField(DetalleMuestraSismica)

    def getDatos(self) -> list:
        """devuelve una lista con sus detalles"""
        resultado = []
        for detalle in self.detalleMuestraSismica.all():
            resultado.append(detalle.getDatos())
        return resultado

