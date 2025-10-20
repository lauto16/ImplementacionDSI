from django.db import models


class Estado(models.Model):
    ambito = models.CharField(max_length=100)
    nombreEstado = models.CharField(max_length=100)

    def esConfirmado(self) -> bool:
        if self.nombreEstado == "Confirmado":
            return True
        return False

    def esRechazado(self) -> bool:
        if self.nombreEstado == "Rechazado":
            return True
        return False

    def esAutodetectado(self) -> bool:
        if self.nombreEstado == "Autodetectado":
            return True
        return False

    def esAmbitoEventoSis(self) -> bool:
        if self.ambito == "EventoSismico":
            return True
        return False

    def esBloqueadoEnRevision(self) -> bool:
        if self.nombreEstado == "BloqueadoEnRevision":
            return True
        return False

