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


class Autodetectado(EstadoEventoSismico):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombreEstado = "Autodetectado"
        self.estadoPersistencia = self.setEstadoPersistencia()

    def bloquear(
        self, evento_sismico, fecha_actual, empleado: Empleado
    ) -> None:
        print('cambiando a estado bloqueado en revision')
        # crear el estado BloqueadoEnRevision
        estadoBloqeadoEnRevision = BloqueadoEnRevision()

        # buscar el cambio de estado actual, ponerle fecha fin y crear el nuevo cambio de estado
        cambio_estado_obt = None
        for cambio_estado in evento_sismico.cambiosEstado.all():
            if cambio_estado.esActual():
                cambio_estado_obt = cambio_estado
                break

        cambio_estado_obt.setFechaHoraFin(fecha_actual=fecha_actual)
        
        self.crearCambioEstado(
            evento_sismico=evento_sismico,
            fecha_actual=fecha_actual,
            estado=estadoBloqeadoEnRevision.estadoPersistencia,
            empleado=empleado,
        )
        
        evento_sismico.estadoActualEjecucion = estadoBloqeadoEnRevision


class Confirmado(EstadoEventoSismico):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombreEstado = "Confirmado"
        self.estadoPersistencia = self.setEstadoPersistencia()


class Rechazado(EstadoEventoSismico):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombreEstado = "Rechazado"
        self.estadoPersistencia = self.setEstadoPersistencia()


class BloqueadoEnRevision(EstadoEventoSismico):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombreEstado = "BloqueadoEnRevision"
        self.estadoPersistencia = self.setEstadoPersistencia()

    def confirmar(
        self, evento_sismico, fecha_actual, empleado: Empleado
    ) -> None:
        print('cambiando a estado confirmado')
        # crear el estado Confirmado
        estadoConfirmado = Confirmado()

        # buscar el cambio de estado actual, ponerle fecha fin y crear el nuevo cambio de estado
        cambio_estado_obt = None
        for cambio_estado in evento_sismico.cambiosEstado.all():
            if cambio_estado.esActual():
                cambio_estado_obt = cambio_estado

        cambio_estado_obt.setFechaHoraFin(fecha_actual=fecha_actual)
        self.crearCambioEstado(
            evento_sismico=evento_sismico,
            fecha_actual=fecha_actual,
            estado=estadoConfirmado.estadoPersistencia,
            empleado=empleado,
        )
        
        evento_sismico.estadoActualEjecucion = estadoConfirmado

    def rechazar(
        self, evento_sismico, fecha_actual, empleado: Empleado
    ) -> None:
        print('cambiando a estado rechazado')
        # crear el estado Rechazado
        estadoRechazado = Rechazado()
        
        # buscar el cambio de estado actual, ponerle fecha fin y crear el nuevo cambio de estado
        cambio_estado_obt = None
        for cambio_estado in evento_sismico.cambiosEstado.all():
            if cambio_estado.esActual():
                cambio_estado_obt = cambio_estado
            
        cambio_estado_obt.setFechaHoraFin(fecha_actual=fecha_actual)

        self.crearCambioEstado(
            evento_sismico=evento_sismico,
            empleado=empleado,
            fecha_actual=fecha_actual,
            estado=estadoRechazado.estadoPersistencia,
        )
        
        evento_sismico.estadoActualEjecucion = estadoRechazado
