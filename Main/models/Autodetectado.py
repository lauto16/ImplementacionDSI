from .EstadoEventoSismico import *
from .BloqueadoEnRevision import *


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
