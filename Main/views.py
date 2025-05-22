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
from django.shortcuts import render
from datetime import datetime


def registrar_resultado_revision_manual(request: HttpRequest) -> HttpResponse:
    """
    Vista que guarda los resultados de la revision manual de un sismografo.
    Args:
        request (HttpRequest): Peticion HTTP enviada por el usuario desde el frontend

    Returns:
        HttpResponse: Respuesta en JSON enviada al usuario desde el backend
        ó respuesta en HTTP enviada al usuario desde el backend (en caso de pedir el html)
    """

    if request.method == "GET":
        action = request.GET.get("action")

        if action == "get_eventos_sismicos":
            # eventos de prueba ---------------------------------------------------------

            # estado para ambos eventos
            no_revisado = Estado(ambito="EventoSismico", nombreEstado="NoRevisado")

            # sesion - usuario - empleado
            empleado = Empleado(apellido='Doe',nombre='John', telefono='3516565784', mail='johndoe123@gmail.com')
            user = Usuario(contrasenia='123456789', nombreUsuario='John Doe', empleado=empleado)
            sesion = Sesion(usuario=user)

            # sismografos
            estacion_sismologica_evento1 = EstacionSismologica(codigoEstacion=1, documentoCertificacionAdq=None, fechaSolicitudCertificacion=None, latitud=-34.6037, longitud=-58.3816, nombre='Estacion Cordoba', nroCertificacionAdquisicion=10)
            estacion_sismologica_evento2 = EstacionSismologica(codigoEstacion=2, documentoCertificacionAdq=None, fechaSolicitudCertificacion=None, latitud=31.5370, longitud=-68.5360, nombre='Estacion San Juan', nroCertificacionAdquisicion=11)
        
            sismografo_evento1 = Sismografo(estacionSismologica=estacion_sismologica_evento1, fechaAdquisicion=datetime.strptime("12/10/1998 12:30", "%d/%m/%Y %H:%M"), identificadorSismografo=1234, nroSerie=9089989898)
            sismografo_evento2 = Sismografo(estacionSismologica=estacion_sismologica_evento2,fechaAdquisicion=datetime.strptime("12/10/1999 10:12", "%d/%m/%Y %H:%M"), identificadorSismografo=1235, nroSerie=9089989899)

            fecha_inicio_evento1 = datetime.strptime(
                "12/12/2004 12:45", "%d/%m/%Y %H:%M"
            )
            fecha_fin_evento1 = datetime.strptime("12/12/2004 12:50", "%d/%m/%Y %H:%M")
            magnitud_evento1 = MagnitudRichter("escala base", 7.1)
            origen_de_generacion_evento1 = OrigenDeGeneracion(
                "Capital zona rural", "Cordoba"
            )
            alcance_evento1 = AlcanceSismo(
                nombre="Zonas aledañas camino Alta Gracia", descripcion="Zonas aledañas"
            )
            clasificacion_sismo_evento1 = ClasificacionSismo(12.3, 15.6, "distancia")
            cambio_estado_evento1 = CambioEstado(
                fechaHoraInicio=fecha_inicio_evento1,
                fechaHoraFin=None,
                estado=no_revisado,
                responsableInspeccion=empleado
            )
            estado_serie_temporal = Estado(
                ambito="SerieTemporal", nombreEstado="SinAlarma"
            )
            muestra_sismica_evento1 = MuestraSismica(fecha_inicio_evento1)
            tipo_dato_evento = TipoDeDato("altura_terreno", "metros", 150)
            muestra_sismica_evento1.crearDetalleMuestra(
                valor=120.54, tipo_dato=tipo_dato_evento
            )
            lista_muestras_sismicas_evento1 = [muestra_sismica_evento1]
            serie_temporal_evento1 = SerieTemporal(
                condicionAlarma="temblar",
                fechaHoraInicioRegistroMuestras=fecha_inicio_evento1,
                fechaHoraRegistros=fecha_fin_evento1,
                frecuenciaMuestreo=1.5,
                estado=estado_serie_temporal,
                muestrasSismica=lista_muestras_sismicas_evento1,
            )

            lista_series_temporales_evento1 = [serie_temporal_evento1]

            evento1 = EventoSismico(
                id=1,
                fechaHoraFin=fecha_fin_evento1,
                fechaHoraOcurrencia=fecha_inicio_evento1,
                latitudEpicentro=-34.6037,
                longitudEpicentro=-58.3816,
                latitudHipocentro=-30.6070,
                longitudHipocentro=-50.1045,
                magnitud=magnitud_evento1,
                origenGeneracion=origen_de_generacion_evento1,
                alcanceSismo=alcance_evento1,
                estadoActual=no_revisado,
                clasificacion=clasificacion_sismo_evento1,
                cambiosEstado=[cambio_estado_evento1],
                seriesTemporales=lista_series_temporales_evento1,
            )

            fecha_inicio_evento2 = datetime.strptime(
                "15/07/2010 09:30", "%d/%m/%Y %H:%M"
            )
            fecha_fin_evento2 = datetime.strptime("15/07/2010 09:45", "%d/%m/%Y %H:%M")
            magnitud_evento2 = MagnitudRichter("escala base", 6.3)
            origen_de_generacion_evento2 = OrigenDeGeneracion(
                "Zona costera", "San Juan"
            )
            alcance_evento2 = AlcanceSismo(
                nombre="Zonas aledañas tiramay", descripcion="Zonas aledañas"
            )
            clasificacion_sismo_evento2 = ClasificacionSismo(20.4, 10.1, "distancia")
            cambio_estado_evento2 = CambioEstado(
                fechaHoraInicio=fecha_inicio_evento2,
                fechaHoraFin=None,
                estado=no_revisado,
                responsableInspeccion=empleado
            )

            muestra_sismica_evento2 = MuestraSismica(fecha_inicio_evento2)
            muestra_sismica_evento2.crearDetalleMuestra(
                valor=1200.54, tipo_dato=tipo_dato_evento
            )

            lista_muestras_sismicas_evento2 = [muestra_sismica_evento2]
            serie_temporal_evento2 = SerieTemporal(
                condicionAlarma="temblar",
                fechaHoraInicioRegistroMuestras=fecha_inicio_evento2,
                fechaHoraRegistros=fecha_fin_evento2,
                frecuenciaMuestreo=2.5,
                estado=estado_serie_temporal,
                muestrasSismica=lista_muestras_sismicas_evento2,
            )

            lista_series_temporales_evento2 = [serie_temporal_evento2]

            evento2 = EventoSismico(
                id=2,
                fechaHoraFin=fecha_fin_evento2,
                fechaHoraOcurrencia=fecha_inicio_evento2,
                latitudEpicentro=-31.5370,
                longitudEpicentro=-68.5360,
                latitudHipocentro=-32.0000,
                longitudHipocentro=-67.5000,
                magnitud=magnitud_evento2,
                origenGeneracion=origen_de_generacion_evento2,
                alcanceSismo=alcance_evento2,
                estadoActual=no_revisado,
                clasificacion=clasificacion_sismo_evento2,
                cambiosEstado=[cambio_estado_evento2],
                seriesTemporales=lista_series_temporales_evento2,
                
            )

            eventos = [evento1.as_dict(), evento2.as_dict()]

            return JsonResponse(eventos, safe=False)

        else:
            return render(request, "reg_revision.html")

    return JsonResponse({"error": "Método no permitido"}, status=405)
