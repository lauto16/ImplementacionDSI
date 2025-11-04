from EstadoEventoSismico import *


class Rechazado(EstadoEventoSismico):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombreEstado = "Rechazado"
        self.estadoPersistencia = self.setEstadoPersistencia()
