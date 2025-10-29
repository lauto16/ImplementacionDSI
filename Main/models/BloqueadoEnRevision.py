from .EstadoEventoSismico import * 
from .Confirmado import * 
from .Rechazado import * 

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
#
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
