from ..CambioEstado import CambioEstado
from ..Estado import Estado


class EstadoEventoSismico:
    def __init__(self):
        self.nombreEstado = ""
        self.ambito = "EventoSismico"
        self.estadoPersistencia = Estado

    def setEstadoPersistencia(self):
        """
        Setea el registro de la BD que representa el estado
        """
        all_estados = Estado.objects.all().filter(ambito="EventoSismico")
        for estado in all_estados:
            if estado.nombreEstado == self.nombreEstado:
                return estado
        return None

    def crearCambioEstado(self, fecha_actual, estado: Estado, empleado=None) -> CambioEstado:
        nuevo_estado_cambio_estado = CambioEstado.objects.create(
            fechaHoraInicio=fecha_actual,
            fechaHoraFin=None,
            estado=estado,
            responsableInspeccion=empleado,
        )

        return nuevo_estado_cambio_estado
    
    def bloquear(self, evento_sismico, fecha_actual, gestor) -> None:
        pass

    def confirmar(self, evento_sismico, fecha_actual, gestor) -> None:
        pass

    def rechazar(self, evento_sismico, fecha_actual, gestor) -> None:
        pass

    def esAutodetectado(self) -> bool:
        return self.nombreEstado == 'Autodetectado'
