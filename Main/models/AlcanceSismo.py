from django.db import models

class AlcanceSismo(models.Model):
    descripcion = models.TextField()
    nombre = models.CharField(max_length=100)

    def getDatos(self) -> dict:
        return {"nombre": self.nombre, "descripcion": self.descripcion}

