from .Empleado import Empleado
from .CambioEstado import CambioEstado
from .Estado import Estado


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

    def crearCambioEstado(self, evento_sismico, fecha_actual, estado: Estado, empleado=None) -> None:
        nuevo_estado_cambio_estado = CambioEstado.objects.create(
            fechaHoraInicio=fecha_actual,
            fechaHoraFin=None,
            estado=estado,
            responsableInspeccion=empleado,
        )
        evento_sismico.cambiosEstado.add(nuevo_estado_cambio_estado)
        evento_sismico.estadoActual = estado
        evento_sismico.save()

    def bloquear(self, evento_sismico, fecha_actual, empleado) -> None:
        pass

    def confirmar(self, evento_sismico, fecha_actual, empleado) -> None:
        pass

    def rechazar(self, evento_sismico, fecha_actual, empleado) -> None:
        pass

    def esAutodetectado(self) -> bool:
        return self.nombreEstado == 'Autodetectado'
