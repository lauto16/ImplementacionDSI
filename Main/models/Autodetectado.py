from .EstadoEventoSismico import *
from .BloqueadoEnRevision import *
from ..views import GestorResultRevManual

class Autodetectado(EstadoEventoSismico):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombreEstado = "Autodetectado"
        self.estadoPersistencia = self.setEstadoPersistencia()

    def bloquear(
        self, evento_sismico, fecha_actual, gestor: GestorResultRevManual
    ) -> None:
        print('cambiando a estado bloqueado en revision')

        # buscar el empleado actual
        empleado = gestor.sesion.buscarUsuarioLogueado()

        # crear el estado BloqueadoEnRevision
        estadoBloqueadoEnRevision = BloqueadoEnRevision()

        # buscar el cambio de estado actual, ponerle fecha fin y crear el nuevo cambio de estado
        cambio_estado_obt = None
        for cambio_estado in evento_sismico.cambiosEstado.all():
            if cambio_estado.esActual():
                cambio_estado_obt = cambio_estado
                break

        cambio_estado_obt.setFechaHoraFin(fecha_actual=fecha_actual)

        cambio_estado_nuevo = self.crearCambioEstado(
            evento_sismico=evento_sismico,
            fecha_actual=fecha_actual,
            estado=estadoBloqueadoEnRevision.estadoPersistencia,
            empleado=empleado,
        )
        
        # set del estado en persistencia (fk)
        evento_sismico.estadoActual = estadoBloqueadoEnRevision.estadoPersistencia
        
        # add del estado en ejecucion
        evento_sismico.estadoActualEjecucion = estadoBloqueadoEnRevision

        # agregar cambio estado
        evento_sismico.cambiosEstado.add(cambio_estado_nuevo)
            
        
        # no se contempla en diagrama por ser parte del guardado en bd
        evento_sismico.save()

        