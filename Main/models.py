from django.db import models


class OrigenDeGeneracion(models.Model):
    descripcion = models.TextField()
    nombre = models.CharField(max_length=100)

    def getNombre(self) -> str:
        return f"Nombre: {self.nombre},  descripcion: {self.descripcion}"


class ClasificacionSismo(models.Model):
    kmProfundidadDesde = models.FloatField()
    kmProfundidadHasta = models.FloatField()
    nombre = models.CharField(max_length=100)

    def getNombre(self) -> str:
        return f"Nombre: {self.nombre},  kmProfundidadDesde: {self.kmProfundidadDesde},  kmProfundidadHasta: {self.kmProfundidadHasta}"


class MagnitudRichter(models.Model):
    descripcionMagnitud = models.CharField(max_length=200)
    numero = models.FloatField()


class AlcanceSismo(models.Model):
    descripcion = models.TextField()
    nombre = models.CharField(max_length=100)

    def getNombre(self) -> str:
        return f"Nombre: {self.nombre},  descripcion: {self.descripcion}"


class Estado(models.Model):
    ambito = models.CharField(max_length=100)
    nombreEstado = models.CharField(max_length=100)


class TipoDeDato(models.Model):
    denominacion = models.CharField(max_length=100)
    nombreUnidadMedida = models.CharField(max_length=100)
    valorUmbral = models.FloatField()


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


class CambioEstado(models.Model):
    fechaHoraInicio = models.DateTimeField(null=True, blank=True)
    fechaHoraFin = models.DateTimeField(null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    responsableInspeccion = models.ForeignKey(
        Empleado, on_delete=models.SET_NULL, null=True)


class DetalleMuestraSismica(models.Model):
    valor = models.FloatField()
    tipoDeDato = models.ForeignKey(TipoDeDato, on_delete=models.CASCADE)


class MuestraSismica(models.Model):
    fechaHoraMuestra = models.DateTimeField(null=True, blank=True)
    detalleMuestraSismica = models.ManyToManyField(DetalleMuestraSismica)


class SerieTemporal(models.Model):
    condicionAlarma = models.CharField(max_length=200)
    fechaHoraInicioRegistroMuestras = models.DateTimeField(
        null=True, blank=True)
    fechaHoraRegistros = models.DateTimeField(null=True, blank=True)
    frecuenciaMuestreo = models.FloatField()
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    muestraSismica = models.ManyToManyField(MuestraSismica)


class Sismografo(models.Model):
    fechaAdquisicion = models.DateTimeField(null=True, blank=True)
    identificadorSismografo = models.CharField(max_length=100)
    nroSerie = models.CharField(max_length=100)
    estacionSismologica = models.ForeignKey(
        EstacionSismologica, on_delete=models.CASCADE)
    serieTemporal = models.ManyToManyField(SerieTemporal)


class EventoSismico(models.Model):
    fechaHoraFin = models.DateTimeField(null=True, blank=True)
    fechaHoraOcurrencia = models.DateTimeField(null=True, blank=True)
    latitudEpicentro = models.FloatField()
    longitudEpicentro = models.FloatField()
    latitudHipocentro = models.FloatField()
    longitudHipocentro = models.FloatField()
    magnitud = models.ForeignKey(MagnitudRichter, on_delete=models.CASCADE)
    origenGeneracion = models.ForeignKey(
        OrigenDeGeneracion, on_delete=models.CASCADE)
    alcanceSismo = models.ForeignKey(AlcanceSismo, on_delete=models.CASCADE)
    estadoActual = models.ForeignKey(
        Estado, on_delete=models.CASCADE, related_name='eventos_actuales')
    clasificacion = models.ForeignKey(
        ClasificacionSismo, on_delete=models.CASCADE)
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

        return "\n".join([
            color("=== Evento Sísmico ===", "1;34"),
            color(
                f"Fecha/Hora de Ocurrencia: {self.fechaHoraOcurrencia}", "1;32"),
            color(f"Fecha/Hora de Fin: {self.fechaHoraFin}", "1;32"),
            color(f"Latitud Epicentro: {self.latitudEpicentro}", "1;36"),
            color(f"Longitud Epicentro: {self.longitudEpicentro}", "1;36"),
            color(f"Latitud Hipocentro: {self.latitudHipocentro}", "1;36"),
            color(f"Longitud Hipocentro: {self.longitudHipocentro}", "1;36"),
            color(f"Magnitud: {dict_from_obj(self.magnitud)}", "1;35"),
            color(
                f"Origen de Generación: {dict_from_obj(self.origenGeneracion)}", "1;35"),
            color(
                f"Alcance del Sismo: {dict_from_obj(self.alcanceSismo)}", "1;35"),
            color(
                f"Estado Actual: {dict_from_obj(self.estadoActual)}", "1;33"),
            color(
                f"Clasificación: {dict_from_obj(self.clasificacion)}", "1;33"),
            color(
                f"Cantidad de Cambios de Estado: {self.cambiosEstado.count()}", "1;31"),
            color(
                f"Cantidad de Series Temporales: {self.serieTemporal.count()}", "1;31"),
        ])

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "fechaHoraFin": (
                self.fechaHoraFin.strftime("%Y-%m-%d %H:%M:%S")
                if hasattr(self.fechaHoraFin, "strftime")
                else self.fechaHoraFin
            ),
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
                self.magnitud.numero
                if hasattr(self.magnitud, "numero")
                else self.magnitud
            ),
            "origenGeneracion": (
                self.origenGeneracion.getNombre()
                if hasattr(self.origenGeneracion, "getNombre")
                else self.origenGeneracion
            ),
            "alcanceSismo": self.alcanceSismo.getNombre(),
            "estadoActual": self.estadoActual.nombreEstado,
            "clasificacion": self.clasificacion.getNombre(),
            "cambiosEstado": [x.estado.nombreEstado for x in self.cambiosEstado.all()],
        }


class Sesion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fechaInicio = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
