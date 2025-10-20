from django.db import models


class EstacionSismologica(models.Model):
    codigoEstacion = models.CharField(max_length=100)
    documentoCertificacionAdq = models.TextField()
    fechaSolicitudCertificacion = models.DateTimeField(blank=True, null=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    nombre = models.CharField(max_length=100)
    nroCertificacionAdquisicion = models.CharField(max_length=100)

