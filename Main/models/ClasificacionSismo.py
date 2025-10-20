from django.db import models

class ClasificacionSismo(models.Model):
    kmProfundidadDesde = models.FloatField()
    kmProfundidadHasta = models.FloatField()
    nombre = models.CharField(max_length=100)

    def getDatos(self) -> dict:
        return {
            "nombre": self.nombre,
            "kmProfundidadDesde": self.kmProfundidadDesde,
            "kmProfundidadHasta": self.kmProfundidadHasta,
        }