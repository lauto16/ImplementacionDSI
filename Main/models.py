from django.db import models


class OrigenDeGeneracion(models.Model):
    descripcion = models.TextField()
    nombre = models.CharField(max_length=100)

    def getDatos(self) -> dict:
        return {"nombre": self.nombre, "descripcion": self.descripcion}


class ClasificacionSismo(models.Model):
    kmProfundidadDesde = models.FloatField()
    kmProfundidadHasta = models.FloatField()
    nombre = models.CharField(max_length=100)

    def getDatos(self) -> dict:
        return {
            "nombre": self.nombre,
            "kmProfundidadDesde": self.kmProfundidadDesde,
            "kmProfundidadHasta": self.kmProfundidadHasta,
        }


class MagnitudRichter(models.Model):
    descripcionMagnitud = models.CharField(max_length=200)
    numero = models.FloatField()


class AlcanceSismo(models.Model):
    descripcion = models.TextField()
    nombre = models.CharField(max_length=100)

    def getDatos(self) -> dict:
        return {"nombre": self.nombre, "descripcion": self.descripcion}


class Estado(models.Model):
    ambito = models.CharField(max_length=100)
    nombreEstado = models.CharField(max_length=100)

    def esConfirmado(self) -> bool:
        if self.nombreEstado == "Confirmado":
            return True
        return False

    def esRechazado(self) -> bool:
        if self.nombreEstado == "Rechazado":
            return True
        return False

    def esAutodetectado(self) -> bool:
        if self.nombreEstado == "Autodetectado":
            return True
        return False

    def esAmbitoEventoSis(self) -> bool:
        if self.ambito == "EventoSismico":
            return True
        return False

    def esBloqueadoEnRevision(self) -> bool:
        if self.nombreEstado == "BloqueadoEnRevision":
            return True
        return False


class TipoDeDato(models.Model):
    denominacion = models.CharField(max_length=100)
    nombreUnidadMedida = models.CharField(max_length=100)
    valorUmbral = models.FloatField()

    def as_dict(self) -> dict:
        return {
            "denominacion": self.denominacion,
            "nombreUnidadMedida": self.nombreUnidadMedida,
            "valorUmbral": self.valorUmbral,
        }


class EstacionSismologica(models.Model):
    codigoEstacion = models.CharField(max_length=100)
    documentoCertificacionAdq = models.TextField()
    fechaSolicitudCertificacion = models.DateTimeField(blank=True, null=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    nombre = models.CharField(max_length=100)
    nroCertificacionAdquisicion = models.CharField(max_length=100)


class Empleado(models.Model):
    apellido = models.CharField(max_length=100)
    mail = models.EmailField()
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)


class Usuario(models.Model):
    contrasenia = models.CharField(max_length=100)
    nombreUsuario = models.CharField(max_length=100)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

    def getEmpleado(self):
        return self.empleado


class CambioEstado(models.Model):
    fechaHoraInicio = models.DateTimeField(null=True, blank=True)
    fechaHoraFin = models.DateTimeField(null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    responsableInspeccion = models.ForeignKey(
        Empleado, on_delete=models.SET_NULL, null=True, default=None
    )

    def esActual(self) -> bool:
        return not self.fechaHoraFin

    def setFechaHoraFin(self, fecha_actual) -> None:
        self.fechaHoraFin = fecha_actual
        self.save()


class DetalleMuestraSismica(models.Model):
    valor = models.FloatField()
    tipoDeDato = models.ForeignKey(TipoDeDato, on_delete=models.CASCADE)

    def getDatos(self) -> dict:
        return {
            "valor": self.valor,
            "tipoDeDato": (
                self.tipoDeDato.as_dict()
                if hasattr(self.tipoDeDato, "as_dict")
                else self.tipoDeDato_id
            ),
        }


class MuestraSismica(models.Model):
    fechaHoraMuestra = models.DateTimeField(null=True, blank=True)
    detalleMuestraSismica = models.ManyToManyField(DetalleMuestraSismica)

    def getDatos(self) -> list:
        """devuelve una lista con sus detalles"""
        resultado = []
        for detalle in self.detalleMuestraSismica.all():
            resultado.append(detalle.getDatos())
        return resultado


class SerieTemporal(models.Model):
    condicionAlarma = models.CharField(max_length=200)
    fechaHoraInicioRegistroMuestras = models.DateTimeField(null=True, blank=True)
    fechaHoraRegistros = models.DateTimeField(null=True, blank=True)
    frecuenciaMuestreo = models.FloatField()
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    muestraSismica = models.ManyToManyField(MuestraSismica)

    def getDatosMuestra(self, sismografos: list) -> dict:
        datosMuestras = []
        for muestra in self.muestraSismica.all():
            datosMuestras = muestra.getDatos()

        ES = self.obtenerES(sismografos, serie_temporal=self.fechaHoraRegistros)
        datosMuestreo = {"estacionSismologica": ES, "datosMuestras": datosMuestras}


        return datosMuestreo

    def obtenerES(self, sismografos: list, serie_temporal):
        for sismografo in sismografos:
            ES = sismografo.obtenerSismografo(serie_temporal)
            if ES:
                return ES
            

class Sismografo(models.Model):
    fechaAdquisicion = models.DateTimeField(null=True, blank=True)
    identificadorSismografo = models.CharField(max_length=100)
    nroSerie = models.CharField(max_length=100)
    estacionSismologica = models.ForeignKey(
        EstacionSismologica, on_delete=models.CASCADE
    )
    serieTemporal = models.ManyToManyField(SerieTemporal)

    def obtenerSismografo(self, serie_comparar):
        for serie in self.serieTemporal.all():
                print(serie.fechaHoraRegistros, '   ', serie_comparar)
                if serie.fechaHoraRegistros == serie_comparar:
                    ES = self.estacionSismologica
                    return ES
        return None


class EventoSismico(models.Model):
    fechaHoraFin = models.DateTimeField(null=True, blank=True)
    fechaHoraOcurrencia = models.DateTimeField(null=True, blank=True)
    latitudEpicentro = models.FloatField()
    longitudEpicentro = models.FloatField()
    latitudHipocentro = models.FloatField()
    longitudHipocentro = models.FloatField()
    magnitud = models.ForeignKey(MagnitudRichter, on_delete=models.CASCADE)
    origenGeneracion = models.ForeignKey(OrigenDeGeneracion, on_delete=models.CASCADE)
    alcanceSismo = models.ForeignKey(AlcanceSismo, on_delete=models.CASCADE)
    estadoActual = models.ForeignKey(
        Estado, on_delete=models.CASCADE, related_name="eventos_actuales"
    )
    clasificacion = models.ForeignKey(ClasificacionSismo, on_delete=models.CASCADE)
    cambiosEstado = models.ManyToManyField(CambioEstado)
    serieTemporal = models.ManyToManyField(SerieTemporal)

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
                color(f"Fecha/Hora de Ocurrencia: {self.fechaHoraOcurrencia}", "1;32"),
                color(f"Fecha/Hora de Fin: {self.fechaHoraFin}", "1;32"),
                color(f"Latitud Epicentro: {self.latitudEpicentro}", "1;36"),
                color(f"Longitud Epicentro: {self.longitudEpicentro}", "1;36"),
                color(f"Latitud Hipocentro: {self.latitudHipocentro}", "1;36"),
                color(f"Longitud Hipocentro: {self.longitudHipocentro}", "1;36"),
                color(f"Magnitud: {dict_from_obj(self.magnitud)}", "1;35"),
                color(
                    f"Origen de Generación: {dict_from_obj(self.origenGeneracion)}",
                    "1;35",
                ),
                color(f"Alcance del Sismo: {dict_from_obj(self.alcanceSismo)}", "1;35"),
                color(f"Estado Actual: {dict_from_obj(self.estadoActual)}", "1;33"),
                color(f"Clasificación: {dict_from_obj(self.clasificacion)}", "1;33"),
                color(
                    f"Cantidad de Cambios de Estado: {self.cambiosEstado.count()}",
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
            "id": self.id,
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
                self.magnitud.numero if hasattr(self.magnitud, "numero") else 10
            ),
        }

    def getAlcance(self) -> str:
        return self.alcanceSismo.getDatos()

    def getClasificacion(self) -> str:
        return self.clasificacion.getDatos()

    def getOrigenGeneracion(self) -> str:
        return self.origenGeneracion.getDatos()

    def crearCambioEstado(self, fecha_actual, estado: Estado, empleado=None) -> None:
        nuevo_estado_cambio_estado = CambioEstado.objects.create(
            fechaHoraInicio=fecha_actual, fechaHoraFin=None, estado=estado, responsableInspeccion=empleado)
        self.cambiosEstado.add(nuevo_estado_cambio_estado)
        self.estadoActual = estado
        self.save()

    def bloquear(self, fecha_actual, estado: Estado) -> None:
        cambio_estado_obt = None
        for cambio_estado in self.cambiosEstado.all():
            if cambio_estado.esActual():
                cambio_estado_obt = cambio_estado
                break
        cambio_estado_obt.setFechaHoraFin(fecha_actual=fecha_actual)
        self.crearCambioEstado(fecha_actual=fecha_actual, estado=estado)
                      
    def buscarSerieTemporal(self, sismografos: list):
        resultado = []
        for serieTemporal in self.serieTemporal.all():
            resultado.append(serieTemporal.getDatosMuestra(sismografos))
        return resultado

    def confirmar(self, fecha_actual, estado: Estado, empleado: Empleado) -> None:
        for cambio_estado in self.cambiosEstado.all():
            if cambio_estado.esActual():
                cambio_estado.setFechaHoraFin(fecha_actual=fecha_actual)
                self.crearCambioEstado(fecha_actual=fecha_actual, estado=estado, empleado=empleado)

    def rechazar(self, fecha_actual) -> None:
        for cambio_estado in self.cambiosEstado.all():
            if cambio_estado.esActual():
                cambio_estado.setFechaHoraFin(fecha_actual=fecha_actual)
    
    def esAutodetectado(self):
        if self.estadoActual.esAutodetectado():
            return True
        return False


class Sesion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fechaInicio = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def buscarUsuarioLogueado(self):
        return self.usuario.getEmpleado()
