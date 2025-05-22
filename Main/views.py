from .evento_sismico import EventoSismico, MagnitudRichter, OrigenDeGeneracion, AlcanceSismo, Estado
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from datetime import datetime


def registrar_resultado_revision_manual(request: HttpRequest) -> HttpResponse:
    """
    Guarda los resultados de la revision manual de un sismografo.
    Args:
        request (HttpRequest): Peticion HTTP enviada por el usuario desde el frontend

    Returns:
        HttpResponse: Respuesta en JSON enviada al usuario desde el backend
        ó respuesta en HTTP enviada al usuario desde el backend (en caso de pedir el html)
    """

    if request.method == "GET":
        action = request.GET.get("action")

        if action == "get_eventos_sismicos":
            # eventos de prueba ----------------------------------------------------------

            # estado para ambos eventos
            no_revisado = Estado(ambito='EventoSismico', nombreEstado='NoRevisado')

            fecha_inicio_evento1 = datetime.strptime("12/12/2004 12:45", "%d/%m/%Y %H:%M")
            fecha_fin_evento1 = datetime.strptime("12/12/2004 12:50", "%d/%m/%Y %H:%M")
            magnitud_evento1 = MagnitudRichter('escala base', 7.1)
            origen_de_generacion_evento1 = OrigenDeGeneracion('Capital zona rural', 'Cordoba')
            alcance_evento1 = AlcanceSismo(nombre='Zonas aledañas camino Alta Gracia', descripcion='Zonas aledañas')

            evento1 = EventoSismico(
                id=1,
                fechaHoraFin=fecha_fin_evento1,
                fechaHoraOcurrencia=fecha_inicio_evento1,
                latitudEpicentro=-34.6037,
                longitudEpicentro=-58.3816,
                latitudHipocentro=-30.6070,
                longitudHipocentro=-50.1045,
                magnitud=magnitud_evento1,
                origenGeneracion= origen_de_generacion_evento1,
                alcanceSismo=alcance_evento1,
                estadoActual = no_revisado
            )

            fecha_inicio_evento2 = datetime.strptime("15/07/2010 09:30", "%d/%m/%Y %H:%M")
            fecha_fin_evento2 = datetime.strptime("15/07/2010 09:45", "%d/%m/%Y %H:%M")
            magnitud_evento2 = MagnitudRichter('escala base', 6.3)
            origen_de_generacion_evento2 = OrigenDeGeneracion('Zona costera', 'San Juan')
            alcance_evento2 = AlcanceSismo(nombre='Zonas aledañas tiramay', descripcion='Zonas aledañas')

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
                estadoActual = no_revisado
        )

            eventos = [evento1.as_dict(), evento2.as_dict()]
            return JsonResponse(eventos, safe=False)

        else:
            return render(request, "reg_revision.html")

    return JsonResponse({"error": "Método no permitido"}, status=405)
