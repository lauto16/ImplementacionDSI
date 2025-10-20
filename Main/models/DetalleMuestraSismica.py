from django.db import models
from .TipoDeDato import TipoDeDato

class DetalleMuestraSismica(models.Model):
    valor = models.FloatField()
    tipoDeDato = models.ForeignKey(TipoDeDato, on_delete=models.CASCADE)

    def getDatos(self) -> dict:
        return {
            "valor": self.valor,
            "tipoDeDato": (
                self.tipoDeDato.as_dict()
                if hasattr(self.tipoDeDato, "as_dict")
                else self.tipoDeDato_id
            ),
        }

