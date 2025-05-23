class OrigenDeGeneracion:
    def __init__(self, descripcion: str, nombre: str) -> None:
        self.descripcion = descripcion
        self.nombre = nombre

    def getNombre(self) -> str:
        return self.nombre


class ClasificacionSismo:
    def __init__(
        self, kmProfundidadDesde: float, kmProfundidadHasta: float, nombre: str
    ) -> None:
        self.kmProfundidadDesde = kmProfundidadDesde
        self.kmProfundidadHasta = kmProfundidadHasta
        self.nombre = nombre

    def getNombre(self) -> str:
        return self.nombre


class MagnitudRichter:
    def __init__(self, descripcionMagnitud: str, numero: float) -> None:
        self.descripcionMagnitud = descripcionMagnitud
        self.numero = numero


class AlcanceSismo:
    def __init__(self, descripcion: str, nombre: str) -> None:
        self.descripcion = descripcion
        self.nombre = nombre

    def getNombre(self) -> str:
        return self.nombre


class Estado:
    def __init__(self, ambito: str, nombreEstado: str) -> None:
        self.ambito: str = ambito
        self.nombreEstado: str = nombreEstado

    def esAutodetectado(self) -> bool:
        return self.nombreEstado == 'Autodetectado'


class TipoDeDato:
    def __init__(
        self, denominacion: str, nombreUnidadMedida: str, valorUmbral: float
    ) -> None:
        self.denominacion = denominacion
        self.nombreUnidadMedida = nombreUnidadMedida
        self.valorUmbral = valorUmbral

    def esTuDenominacion(self, denom_test) -> bool:
        if denom_test == self.denominacion:
            return True
        return False


class DetalleMuestraSismica:
    def __init__(self, valor, tipoDeDato: TipoDeDato) -> None:
        self.valor = valor
        self.tipoDeDato = tipoDeDato

    def getDatos(self) -> dict:
        return {"valor": self.valor, "tipo_de_dato": self.tipoDeDato}


class MuestraSismica:
    def __init__(self, fechaHoraMuestra) -> None:
        self.fechaHoraMuestra = fechaHoraMuestra
        self.detallesMuestraSismica = []

    def crearDetalleMuestra(self, valor, tipo_dato: TipoDeDato) -> None:
        new_detalle = DetalleMuestraSismica(valor=valor, tipoDeDato=tipo_dato)
        self.detallesMuestraSismica.append(new_detalle)


class SerieTemporal:
    def __init__(
        self,
        condicionAlarma: str,
        fechaHoraInicioRegistroMuestras,
        fechaHoraRegistros,
        frecuenciaMuestreo: float,
        estado: Estado,
        muestrasSismica: list,
    ) -> None:
        self.condicionAlarma = condicionAlarma
        self.fechaHoraInicioRegistroMuestras = fechaHoraInicioRegistroMuestras
        self.fechaHoraRegistros = fechaHoraRegistros
        self.frecuenciaMuestreo = frecuenciaMuestreo
        self.estado = estado
        self.muestrasSismica = muestrasSismica

    def getDatos(self) -> dict:
        return {
            "condicionAlarma": self.condicionAlarma,
            "fechaHoraInicioRegistroMuestras": self.fechaHoraInicioRegistroMuestras,
            "fechaHoraRegistros": self.fechaHoraRegistros,
            "frecuenciaMuestreo": self.frecuenciaMuestreo,
            "estado": self.estado.nombreEstado,
            #'muestrasSismica': self.muestrasSismica,
        }


class Empleado:
    def __init__(self, apellido: str, mail: str, nombre: str, telefono: str) -> None:
        self.apellido = apellido
        self.mail = mail
        self.nombre = nombre
        self.telefono = telefono


class Usuario:
    def __init__(
        self, contrasenia: str, nombreUsuario: str, empleado: Empleado
    ) -> None:
        # usar "ñ" es contra pep8
        self.contrasenia = contrasenia
        self.nombreUsuario = nombreUsuario
        self.empleado = empleado


class Sesion:
    def __init__(self, usuario: Usuario) -> None:
        self.usuario = usuario


class CambioEstado:
    def __init__(self, fechaHoraInicio, fechaHoraFin, estado: Estado, responsableInspeccion: Empleado) -> None:
        self.fechaHoraFin = fechaHoraFin
        self.fechaHoraInicio = fechaHoraInicio
        self.estado = estado
        self.responsableInspeccion = responsableInspeccion

    def esEstadoActual(self) -> bool:
        if self.fechaHoraFin == None:
            return True
        return False


class EstacionSismologica:
    def __init__(
        self,
        codigoEstacion,
        documentoCertificacionAdq,
        fechaSolicitudCertificacion,
        latitud,
        longitud,
        nombre,
        nroCertificacionAdquisicion,
    ) -> None:
        self.codigoEstacion = codigoEstacion
        self.documentoCertificacionAdq = documentoCertificacionAdq
        self.fechaSolicitudCertificacion = fechaSolicitudCertificacion
        self.latitud = latitud
        self.longitud = longitud
        self.nombre = nombre
        self.nroCertificacionAdquisicion = nroCertificacionAdquisicion


class Sismografo:
    def __init__(
        self,
        fechaAdquisicion,
        identificadorSismografo,
        nroSerie,
        estacionSismologica: EstacionSismologica,
    ) -> None:
        self.fechaAdquisicion = fechaAdquisicion
        self.identificadorSismografo = identificadorSismografo
        self.nroSerie = nroSerie
        self.estado = None
        self.cambioEstado = None
        self.estacionSismologica = estacionSismologica


class EventoSismico:
    def __init__(
        self,
        id: int,
        fechaHoraFin,
        fechaHoraOcurrencia,
        latitudEpicentro: float,
        longitudEpicentro: float,
        latitudHipocentro: float,
        longitudHipocentro: float,
        magnitud: MagnitudRichter,
        origenGeneracion: OrigenDeGeneracion,
        alcanceSismo: AlcanceSismo,
        estadoActual: Estado,
        clasificacion: ClasificacionSismo,
        cambiosEstado: list,
        seriesTemporales: list,
    ) -> None:
        self.id = id
        self.fechaHoraFin = fechaHoraFin
        self.fechaHoraOcurrencia = fechaHoraOcurrencia
        self.latitudEpicentro = latitudEpicentro
        self.longitudEpicentro = longitudEpicentro
        self.latitudHipocentro = latitudHipocentro
        self.longitudHipocentro = longitudHipocentro
        self.magnitud = magnitud
        self.origenGeneracion = origenGeneracion
        self.alcanceSismo = alcanceSismo
        self.estadoActual = estadoActual
        self.clasificacion = clasificacion
        self.cambiosEstado = cambiosEstado
        self.seriesTemporales = seriesTemporales
    
    def getValorMagnitud(self) -> float:
        return self.magnitud.numero

    def obtenerDatos(self) -> dict:
        return {
            'valorMagnitud': self.getValorMagnitud(),
            'latitudHipocentro': self.latitudHipocentro,
            'latitudEpicentro': self.latitudEpicentro,
            'longitudHipocentro': self.longitudHipocentro,
            'longitudEpicentro': self.longitudEpicentro,
            'fechaHoraOcurrencia': self.fechaHoraOcurrencia
        }

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
            "cambiosEstado": [x.estado.nombreEstado for x in self.cambiosEstado],
        }
