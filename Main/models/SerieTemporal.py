from django.db import models
from .EstadoEventoSismico import Estado
from .MuestraSismica import MuestraSismica


class SerieTemporal(models.Model):
    condicionAlarma = models.CharField(max_length=200)
    fechaHoraInicioRegistroMuestras = models.DateTimeField(
        null=True, blank=True)
    fechaHoraRegistros = models.DateTimeField(null=True, blank=True)
    frecuenciaMuestreo = models.FloatField()
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    muestraSismica = models.ManyToManyField(MuestraSismica)

    def getDatosMuestra(self, sismografos: list) -> dict:
        datosMuestras = []
        for muestra in self.muestraSismica.all():
            datosMuestras = muestra.getDatos()

        ES = self.obtenerES(
            sismografos, serie_temporal=self.fechaHoraRegistros)
        datosMuestreo = {"estacionSismologica": ES,
                         "datosMuestras": datosMuestras}

        return datosMuestreo

    def obtenerES(self, sismografos: list, serie_temporal):
        for sismografo in sismografos:
            ES = sismografo.obtenerSismografo(serie_temporal)
            if ES:
                return ES

