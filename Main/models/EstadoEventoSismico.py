from django.db import models


class EstadoEventoSismico(models.Model):
    """
    Clase padre para implemetar State
    """

    ambito = models.CharField(max_length=100)
    nombreEstado = models.CharField(max_length=100)
    
    class Meta:
        abstract = True

    def bloquear(self) -> None:
        pass

    def confirmar(self) -> None:
        pass

    def rechazar(self) -> None:
        pass
    
    
class Autodetectado(EstadoEventoSismico):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def bloquear(self) -> None:
        pass
   
 
class Confirmado(EstadoEventoSismico):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Rechazado(EstadoEventoSismico):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BloqueadoEnRevision(EstadoEventoSismico):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def confirmar(self) -> None:
        pass
    
    def rechazar(self) -> None:
        pass
