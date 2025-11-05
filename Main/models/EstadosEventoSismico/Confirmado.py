from .EstadoEventoSismico import * 

class Confirmado(EstadoEventoSismico):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombreEstado = "Confirmado"
        self.estadoPersistencia = self.setEstadoPersistencia()
