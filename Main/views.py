from .evento_sismico import (
    EventoSismico,
    MagnitudRichter,
    OrigenDeGeneracion,
    AlcanceSismo,
    Estado,
    ClasificacionSismo,
    CambioEstado,
    SerieTemporal,
    MuestraSismica,
    TipoDeDato,
    Sismografo,
    EstacionSismologica,
    Sesion,
    Usuario,
    Empleado
)
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views import View
from django.shortcuts import render
from datetime import datetime


class GestorResultRevManual:
    def __init__(self) -> None:
        self.eventosAutodetectados = []
        self.estados = []
        self.eventoSisActual = None
        self.fechaHoraActual = None
        self.estado_BloqueadoEnRevision = None

    def getFechaHoraActual(self) -> datetime:
        return datetime.now()

    def tomarSelEventoSis(self, id_evento: int) -> None:
        # se necesita buscar el evento elegio entre los autodetectados
        self.eventoSisActual = self.getEventoAutodetectado(id=id_evento)
        self.estado_BloqueadoEnRevision = self.buscarEstadoBloqueadoEnRevision()
        self.fechaHoraActual = self.getFechaHoraActual()
        self.bloquearEventoSis()

    def getEventoAutodetectado(self, id: int):
        for evento in self.eventosAutodetectados:
            if id == evento.id:
                return evento

    def bloquearEventoSis(self) -> None:
        self.eventoSisActual.bloquear(fecha_actual=self.fechaHoraActual, estado=self.estado_BloqueadoEnRevision)

    def ordenarEventosSisPorFyH(self) -> None:
        self.eventosAutodetectados.sort(key=lambda evento: evento.fechaHoraOcurrencia)
    
    def buscarEstadoBloqueadoEnRevision(self) -> Estado:
        for estado in self.estados:
            if estado.esAmbitoEventoSis():
                if estado.esBloqueadoEnRevision():
                    self.bloquearEventoSis()
                    return estado

    def buscarEventosAutodetectados(self, eventos: list) -> list:
        for evento in eventos:
                if evento.estadoActual.esAutodetectado:
                    self.eventosAutodetectados.append(evento)
        self.ordenarEventosSisPorFyH()
        return self.eventosAutodetectados


def opciones_sismografo(request: HttpRequest) -> HttpResponse:
    """
    Vista para mostrar las opciones del sistema

    Args:
        request (HttpRequest): Peticion HTTP enviada por el usuario desde el frontend

    Returns:
        HttpResponse: Respuesta en JSON enviada al usuario desde el backend
        ó respuesta en HTTP enviada al usuario desde el backend (en caso de pedir el html)
    """

    return render(request, 'opciones.html')


class InterfazResultRevManual(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gestor = GestorResultRevManual()

    def get(self, request: HttpRequest) -> HttpResponse:
        action = request.GET.get("action")

        # SE DEFINEN ACA PORQUE DE OTRA FORMA LA VISTA RECARGA T0DO AL INICIAR Y SE PERDERIAN EN LA EJECUCION...
        autodetectado = Estado(ambito="EventoSismico", nombreEstado="Autodetectado")
        sin_alarma = Estado(ambito="SerieTemporal", nombreEstado="SinAlarma")
        bloquedo_en_revision = Estado(ambito='EventoSismico', nombreEstado='BloqueadoEnRevision')

        self.gestor.estados.append(autodetectado)
        self.gestor.estados.append(sin_alarma)
        self.gestor.estados.append(bloquedo_en_revision)

        if action == 'tomar_sel_evento_sismico':
            id_evento = request.GET.get("id_evento")
            self.gestor.tomarSelEventoSis(id_evento=id_evento)
            

        if action == "get_eventos_sismicos":
            tipo_dato_evento = TipoDeDato("altura_terreno", "metros", 150)
            
            empleado = Empleado(apellido='Doe', nombre='John', telefono='3516565784', mail='johndoe123@gmail.com')
            user = Usuario(contrasenia='123456789', nombreUsuario='John Doe', empleado=empleado)
            sesion = Sesion(usuario=user)

            estacion1 = EstacionSismologica(codigoEstacion=1, documentoCertificacionAdq=None, fechaSolicitudCertificacion=None, latitud=-34.6037, longitud=-58.3816, nombre='Estacion Cordoba', nroCertificacionAdquisicion=10)
            estacion2 = EstacionSismologica(codigoEstacion=2, documentoCertificacionAdq=None, fechaSolicitudCertificacion=None, latitud=31.5370, longitud=-68.5360, nombre='Estacion San Juan', nroCertificacionAdquisicion=11)

            sismografo1 = Sismografo(estacionSismologica=estacion1, fechaAdquisicion=datetime.strptime("12/10/1998 12:30", "%d/%m/%Y %H:%M"), identificadorSismografo=1234, nroSerie=9089989898)
            sismografo2 = Sismografo(estacionSismologica=estacion2, fechaAdquisicion=datetime.strptime("12/10/1999 10:12", "%d/%m/%Y %H:%M"), identificadorSismografo=1235, nroSerie=9089989899)

            fecha_inicio_1 = datetime.strptime("12/12/2004 12:45", "%d/%m/%Y %H:%M")
            fecha_fin_1 = datetime.strptime("12/12/2004 12:50", "%d/%m/%Y %H:%M")
            fecha_inicio_2 = datetime.strptime("15/07/2010 09:30", "%d/%m/%Y %H:%M")
            fecha_fin_2 = datetime.strptime("15/07/2010 09:45", "%d/%m/%Y %H:%M")

            magnitud1 = MagnitudRichter("escala base", 7.1)
            magnitud2 = MagnitudRichter("escala base", 6.3)

            origen1 = OrigenDeGeneracion("Capital zona rural", "Cordoba")
            origen2 = OrigenDeGeneracion("Zona costera", "San Juan")

            alcance1 = AlcanceSismo(nombre="Zonas aledañas camino Alta Gracia", descripcion="Zonas aledañas")
            alcance2 = AlcanceSismo(nombre="Zonas aledañas tiramay", descripcion="Zonas aledañas")

            clasificacion1 = ClasificacionSismo(12.3, 15.6, "distancia")
            clasificacion2 = ClasificacionSismo(20.4, 10.1, "distancia")

            cambio1 = CambioEstado(fechaHoraInicio=fecha_inicio_1, fechaHoraFin=None, estado=autodetectado, responsableInspeccion=empleado)
            cambio2 = CambioEstado(fechaHoraInicio=fecha_inicio_2, fechaHoraFin=None, estado=autodetectado, responsableInspeccion=empleado)

            muestra1 = MuestraSismica(fecha_inicio_1)
            muestra1.crearDetalleMuestra(valor=120.54, tipo_dato=tipo_dato_evento)
            muestra2 = MuestraSismica(fecha_inicio_2)
            muestra2.crearDetalleMuestra(valor=1200.54, tipo_dato=tipo_dato_evento)

            serie1 = SerieTemporal(condicionAlarma="temblar", fechaHoraInicioRegistroMuestras=fecha_inicio_1, fechaHoraRegistros=fecha_fin_1, frecuenciaMuestreo=1.5, estado=sin_alarma, muestrasSismica=[muestra1])
            serie2 = SerieTemporal(condicionAlarma="temblar", fechaHoraInicioRegistroMuestras=fecha_inicio_2, fechaHoraRegistros=fecha_fin_2, frecuenciaMuestreo=2.5, estado=sin_alarma, muestrasSismica=[muestra2])

            evento1 = EventoSismico(id=1, fechaHoraFin=fecha_fin_1, fechaHoraOcurrencia=fecha_inicio_1, latitudEpicentro=-34.6037, longitudEpicentro=-58.3816, latitudHipocentro=-30.6070, longitudHipocentro=-50.1045, magnitud=magnitud1, origenGeneracion=origen1, alcanceSismo=alcance1, estadoActual=autodetectado, clasificacion=clasificacion1, cambiosEstado=[cambio1], seriesTemporales=[serie1])
            evento2 = EventoSismico(id=2, fechaHoraFin=fecha_fin_2, fechaHoraOcurrencia=fecha_inicio_2, latitudEpicentro=-31.5370, longitudEpicentro=-68.5360, latitudHipocentro=-32.0000, longitudHipocentro=-67.5000, magnitud=magnitud2, origenGeneracion=origen2, alcanceSismo=alcance2, estadoActual=autodetectado, clasificacion=clasificacion2, cambiosEstado=[cambio2], seriesTemporales=[serie2])

            eventos = [evento1, evento2]
            
            eventos_autodetectados = self.gestor.buscarEventosAutodetectados(eventos=eventos)
            eventos_autodetectados_para_frontend = [x.as_dict() for x in eventos_autodetectados]

            # mostrarEventosSismicos()
            return JsonResponse(eventos_autodetectados_para_frontend, safe=False)

        return render(request, "reg_revision.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        return JsonResponse({"error": "Método no permitido"}, status=405)