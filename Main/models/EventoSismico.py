from django.db import models

from .AlcanceSismo import AlcanceSismo
from .CambioEstado import CambioEstado
from .ClasificacionSismo import ClasificacionSismo
from .EstadoEventoSismico import EstadoEventoSismico
from .MagnitudRichter import MagnitudRichter
from .OrigenDeGeneracion import OrigenDeGeneracion
from .SerieTemporal import SerieTemporal
from .Empleado import Empleado


class EventoSismico(models.Model):
    fechaHoraFin = models.DateTimeField(null=True, blank=True)
    fechaHoraOcurrencia = models.DateTimeField(null=True, blank=True)
    idCompuesto = models.CharField(
        max_length=1000, primary_key=True, editable=False)
    latitudEpicentro = models.FloatField()
    longitudEpicentro = models.FloatField()
    latitudHipocentro = models.FloatField()
    longitudHipocentro = models.FloatField()
    magnitud = models.ForeignKey(MagnitudRichter, on_delete=models.CASCADE)
    origenGeneracion = models.ForeignKey(
        OrigenDeGeneracion, on_delete=models.CASCADE)
    alcanceSismo = models.ForeignKey(AlcanceSismo, on_delete=models.CASCADE)
    estadoActual = models.ForeignKey(
        EstadoEventoSismico, on_delete=models.CASCADE, related_name="eventos_actuales"
    )
    clasificacion = models.ForeignKey(
        ClasificacionSismo, on_delete=models.CASCADE)
    cambiosEstado = models.ManyToManyField(CambioEstado)
    serieTemporal = models.ManyToManyField(SerieTemporal)

    def save(self, *args, **kwargs):
        if not self.idCompuesto:
            self.idCompuesto = f"{self.latitudEpicentro};{self.longitudEpicentro}"
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        def dict_from_obj(obj):
            if not obj:
                return "None"
            return {
                field.name: getattr(obj, field.name)
                for field in obj._meta.fields
                if not isinstance(getattr(obj, field.name), models.Model)
            }

        def color(text, code):
            return f"\033[{code}m{text}\033[0m"

        return "\n".join(
            [
                color("=== Evento Sísmico ===", "1;34"),
                color(
                    f"Fecha/Hora de Ocurrencia: {self.fechaHoraOcurrencia}", "1;32"),
                color(f"Fecha/Hora de Fin: {self.fechaHoraFin}", "1;32"),
                color(f"Latitud Epicentro: {self.latitudEpicentro}", "1;36"),
                color(f"Longitud Epicentro: {self.longitudEpicentro}", "1;36"),
                color(f"Latitud Hipocentro: {self.latitudHipocentro}", "1;36"),
                color(
                    f"Longitud Hipocentro: {self.longitudHipocentro}", "1;36"),
                color(f"Magnitud: {dict_from_obj(self.magnitud)}", "1;35"),
                color(
                    f"Origen de Generación: {dict_from_obj(self.origenGeneracion)}",
                    "1;35",
                ),
                color(
                    f"Alcance del Sismo: {dict_from_obj(self.alcanceSismo)}", "1;35"),
                color(
                    f"EstadoEventoSismico Actual: {dict_from_obj(self.estadoActual)}", "1;33"),
                color(
                    f"Clasificación: {dict_from_obj(self.clasificacion)}", "1;33"),
                color(
                    f"Cantidad de Cambios de EstadoEventoSismico: {self.cambiosEstado.count()}",
                    "1;31",
                ),
                color(
                    f"Cantidad de Series Temporales: {self.serieTemporal.count()}",
                    "1;31",
                ),
            ]
        )

    def obtenerDatos(self) -> dict:
        return {
            "id": self.idCompuesto,
            "fechaHoraOcurrencia": (
                self.fechaHoraOcurrencia.strftime("%Y-%m-%d %H:%M:%S")
                if hasattr(self.fechaHoraOcurrencia, "strftime")
                else self.fechaHoraOcurrencia
            ),
            "latitudEpicentro": self.latitudEpicentro,
            "longitudEpicentro": self.longitudEpicentro,
            "latitudHipocentro": self.latitudHipocentro,
            "longitudHipocentro": self.longitudHipocentro,
            "magnitud": (
                self.magnitud.numero if hasattr(
                    self.magnitud, "numero") else 10
            ),
        }

    def getAlcance(self) -> str:
        return self.alcanceSismo.getDatos()

    def getClasificacion(self) -> str:
        return self.clasificacion.getDatos()

    def getOrigenGeneracion(self) -> str:
        return self.origenGeneracion.getDatos()

    def crearCambioEstado(self, fecha_actual, estado: EstadoEventoSismico, empleado=None) -> None:
        nuevo_estado_cambio_estado = CambioEstado.objects.create(
            fechaHoraInicio=fecha_actual, fechaHoraFin=None, estado=estado, responsableInspeccion=empleado)
        self.cambiosEstado.add(nuevo_estado_cambio_estado)
        self.estadoActual = estado
        self.save()

    def bloquear(self, fecha_actual, estado: EstadoEventoSismico, empleado: Empleado) -> None:
        cambio_estado_obt = None
        for cambio_estado in self.cambiosEstado.all():
            if cambio_estado.esActual():
                cambio_estado_obt = cambio_estado
                break

        cambio_estado_obt.setFechaHoraFin(fecha_actual=fecha_actual)
        self.crearCambioEstado(fecha_actual=fecha_actual, estado=estado, empleado=empleado)

    def buscarSerieTemporal(self, sismografos: list):
        resultado = []
        for serieTemporal in self.serieTemporal.all():
            resultado.append(serieTemporal.getDatosMuestra(sismografos))
        return resultado

    def confirmar(self, fecha_actual, estado: EstadoEventoSismico, empleado: Empleado) -> None:
        for cambio_estado in self.cambiosEstado.all():
            if cambio_estado.esActual():
                cambio_estado.setFechaHoraFin(fecha_actual=fecha_actual)
                self.crearCambioEstado(
                    fecha_actual=fecha_actual, estado=estado, empleado=empleado)

    def rechazar(self, fecha_actual, empleado: Empleado, estado_Rechazado: EstadoEventoSismico) -> None:
        for cambio_estado in self.cambiosEstado.all():
            if cambio_estado.esActual():
                cambio_estado.setFechaHoraFin(fecha_actual=fecha_actual)
        
        self.crearCambioEstado(
                empleado=empleado,
                fecha_actual=fecha_actual,
                estado=estado_Rechazado,
            )

    def esAutodetectado(self):
        if self.estadoActual.esAutodetectado():
            return True
        return False
    
