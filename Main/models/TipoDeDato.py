from django.db import models

class TipoDeDato(models.Model):
    denominacion = models.CharField(max_length=100)
    nombreUnidadMedida = models.CharField(max_length=100)
    valorUmbral = models.FloatField()

    def as_dict(self) -> dict:
        return {
            "denominacion": self.denominacion,
            "nombreUnidadMedida": self.nombreUnidadMedida,
            "valorUmbral": self.valorUmbral,
        }

