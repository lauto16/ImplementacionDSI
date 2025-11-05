from .EstadoEventoSismico import EstadoEventoSismico

class DerivadoAExperto(EstadoEventoSismico):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombreEstado = "DerivadoAExperto"
        self.estadoPersistencia = self.setEstadoPersistencia()