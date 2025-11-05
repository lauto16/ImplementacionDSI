from .EstadoEventoSismico import EstadoEventoSismico

class Cerrado(EstadoEventoSismico):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombreEstado = "Cerrado"
        self.estadoPersistencia = self.setEstadoPersistencia()