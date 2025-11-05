from .EstadoEventoSismico import EstadoEventoSismico

class PendienteDeCierre(EstadoEventoSismico):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombreEstado = "PendienteDeCierre"
        self.estadoPersistencia = self.setEstadoPersistencia()