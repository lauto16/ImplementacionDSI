from .EstadoEventoSismico import * 
from .Confirmado import * 
from .Rechazado import * 

class BloqueadoEnRevision(EstadoEventoSismico):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombreEstado = "BloqueadoEnRevision"
        self.estadoPersistencia = self.setEstadoPersistencia()

    def buscarUsuarioLogueado(self, gestor):
        return gestor.sesion.buscarUsuarioLogueado()
    
    def confirmar(
        self, evento_sismico, fecha_actual, gestor
    ) -> None:
        print('cambiando a estado confirmado')
        
        empleado = self.buscarUsuarioLogueado(gestor)
        
        # crear el estado Confirmado
        estadoConfirmado = Confirmado()

        # buscar el cambio de estado actual, ponerle fecha fin y crear el nuevo cambio de estado
        cambio_estado_obt = None
        for cambio_estado in evento_sismico.cambiosEstado.all():
            if cambio_estado.esActual():
                cambio_estado_obt = cambio_estado

        cambio_estado_obt.setFechaHoraFin(fecha_actual=fecha_actual)
        
        cambio_estado_nuevo=self.crearCambioEstado(
            fecha_actual=fecha_actual,
            estado=estadoConfirmado.estadoPersistencia,
            empleado=empleado,
        )
        
        # set del estado en persistencia (fk)
        evento_sismico.estadoActual = estadoConfirmado.estadoPersistencia
        
        # add del estado en ejecucion
        evento_sismico.estadoActualEjecucion = estadoConfirmado

        # agregar cambio estado
        evento_sismico.cambiosEstado.add(cambio_estado_nuevo)
            
        # no se contempla en diagrama por ser parte del guardado en bd
        evento_sismico.save()
        
    def rechazar(
        self, evento_sismico, fecha_actual, gestor
    ) -> None:
        print('cambiando a estado rechazado')
        
        # buscar el empleado actual
        empleado = self.buscarUsuarioLogueado(gestor)
        
        # crear el estado Rechazado
        estadoRechazado = Rechazado()
        
        # buscar el cambio de estado actual, ponerle fecha fin y crear el nuevo cambio de estado
        cambio_estado_obt = None
        for cambio_estado in evento_sismico.cambiosEstado.all():
            if cambio_estado.esActual():
                cambio_estado_obt = cambio_estado
                break
            
        cambio_estado_obt.setFechaHoraFin(fecha_actual=fecha_actual)

        cambio_estado_nuevo = self.crearCambioEstado(
            empleado=empleado,
            fecha_actual=fecha_actual,
            estado=estadoRechazado.estadoPersistencia,
        )
        
        # set del estado en persistencia (fk)
        evento_sismico.estadoActual = estadoRechazado.estadoPersistencia
        
        # add del estado en ejecucion
        evento_sismico.estadoActualEjecucion = estadoRechazado

        # agregar cambio estado
        evento_sismico.cambiosEstado.add(cambio_estado_nuevo)
            
        # no se contempla en diagrama por ser parte del guardado en bd
        evento_sismico.save()