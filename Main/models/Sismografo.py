from django.db import models
from .EstacionSismologica import EstacionSismologica
from .SerieTemporal import SerieTemporal


class Sismografo(models.Model):
    fechaAdquisicion = models.DateTimeField(null=True, blank=True)
    identificadorSismografo = models.CharField(max_length=100)
    nroSerie = models.CharField(max_length=100)
    estacionSismologica = models.ForeignKey(
        EstacionSismologica, on_delete=models.CASCADE
    )
    serieTemporal = models.ManyToManyField(SerieTemporal)

    def obtenerSismografo(self, serie_comparar):
        for serie in self.serieTemporal.all():
            if serie.fechaHoraRegistros == serie_comparar:
                ES = self.estacionSismologica
                return ES
        return None
