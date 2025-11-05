from .EstadoEventoSismico import EstadoEventoSismico

class SinRevision(EstadoEventoSismico):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombreEstado = "SinRevision"
        self.estadoPersistencia = self.setEstadoPersistencia()