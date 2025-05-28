"""from .evento_sismico import (
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
)"""

# IMPORTS DE MODELOS
from Main.models import (
    TipoDeDato,
    Empleado,
    Usuario,
    Sesion,
    EstacionSismologica,
    MagnitudRichter,
    OrigenDeGeneracion,
    AlcanceSismo,
    ClasificacionSismo,
    CambioEstado,
    Estado,
    MuestraSismica,
    DetalleMuestraSismica,
    SerieTemporal,
    Sismografo,
    EventoSismico,
)

from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views import View
from django.shortcuts import render
from datetime import datetime
from django.utils import timezone


class GestorResultRevManual:

    def __init__(self, interfaz) -> None:
        self.eventos = list(EventoSismico.objects.all())
        self.eventosAutodetectados = []
        self.estados = list(Estado.objects.all())
        self.eventoSisActual = None
        self.fechaHoraActual = None
        self.estado_BloqueadoEnRevision = None
        self.sismografos = list(Sismografo.objects.all())
        self.interfaz = interfaz
        self.alcanceEventoSis = None
        self.clasificacionEventoSis = None
        self.origenGeneracionEventoSis = None
        self.ordenadoPorES = None

    def getFechaHoraActual(self) -> datetime:
        return timezone.now()

    def tomarSelEventoSis(self, id_evento: int) -> None:
        # se necesita buscar el evento elegio entre los autodetectados
        self.eventosAutodetectados = self.buscarEventosAutodetectados()
        self.eventoSisActual = self.getEventoAutodetectado(id=id_evento)
        self.fechaHoraActual = self.getFechaHoraActual()
        self.estado_BloqueadoEnRevision = self.buscarEstadoBloqueadoEnRevision()
        self.bloquearEventoSis()
        self.buscarDatosEventoSis()
        datosEvenSis = {
            "alcanceEventoSis": self.alcanceEventoSis,
            "clasificacionEventoSis": self.clasificacionEventoSis,
            "origenGeneracionEventoSis": self.origenGeneracionEventoSis,
        }
        # se hace al final -> self.mostrarDatosEventoSis()
        datosSeriesTemporales = self.buscarSerieTemporal()
        self.ordenarPorEstacion(datosSeriesTemporales=datosSeriesTemporales)

        print(f'ORDENADO POR ES: {self.ordenadoPorES}')

        datos_entrega = []
        for i in range(len(self.ordenadoPorES)):
            datosSerieTemporal = {
                'nombreEstacion': self.ordenadoPorES[i]["estacionSismologica"].nombre,
                'muestra': self.ordenadoPorES[i]["datosMuestras"],
            }
            datos_entrega.append(datosSerieTemporal)
        self.llamarCUGenerarSismograma()
        self.mostrarVisualizarMapaYDatos()
        return datos_entrega, datosEvenSis

    def getEventoAutodetectado(self, id: int):
        for evento in self.eventosAutodetectados:
            if id == evento.id:
                return evento

    def bloquearEventoSis(self) -> None:
        self.eventoSisActual.bloquear(
            fecha_actual=self.fechaHoraActual, estado=self.estado_BloqueadoEnRevision
        )

    def ordenarEventosSisPorFyH(self) -> None:
        self.eventosAutodetectados.sort(
            key=lambda evento: evento.fechaHoraOcurrencia)

    def buscarEstadoBloqueadoEnRevision(self) -> Estado:
        for estado in self.estados:
            if estado.esAmbitoEventoSis():
                if estado.esBloqueadoEnRevision():
                    return estado

    def buscarEventosAutodetectados(self) -> list:
        for evento in self.eventos:
            if evento.estadoActual.esAutodetectado:
                self.eventosAutodetectados.append(evento)
        self.ordenarEventosSisPorFyH()
        return self.eventosAutodetectados

    def buscarDatosEventoSis(self):
        self.alcanceEventoSis = self.eventoSisActual.getAlcance()
        self.clasificacionEventoSis = self.eventoSisActual.getClasificacion()
        self.origenGeneracionEventoSis = self.eventoSisActual.getOrigenGeneracion()

    def buscarSerieTemporal(self):
        return self.eventoSisActual.buscarSerieTemporal(sismografos=self.sismografos)

    def ordenarPorEstacion(self, datosSeriesTemporales: list) -> None:
        # Ordenar ES por nombre de A-Z
        self.ordenadoPorES = sorted(
            datosSeriesTemporales,
            key=lambda dato: dato["estacionSismologica"].nombre.lower(),
        )

    def llamarCUGenerarSismograma(self):
        return "Se llamó al CU generar Sismograma"

    def mostrarVisualizarMapaYDatos(self):
        pass


def opciones_sismografo(request: HttpRequest) -> HttpResponse:
    """
    Vista para mostrar las opciones del sistema

    Args:
        request (HttpRequest): Peticion HTTP enviada por el usuario desde el frontend

    Returns:
        HttpResponse: Respuesta en JSON enviada al usuario desde el backend
        ó respuesta en HTTP enviada al usuario desde el backend (en caso de pedir el html)
    """

    return render(request, "opciones.html")


class InterfazResultRevManual(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gestor = GestorResultRevManual(interfaz=self)

    def get(self, request: HttpRequest) -> HttpResponse:
        action = request.GET.get("action")

        if action == "tomar_sel_evento_sismico":
            id_evento = request.GET.get("id_evento")
            serieTemporal, datosSis = self.gestor.tomarSelEventoSis(
                id_evento=int(id_evento)
            )
            res = {"serieTemp": serieTemporal, "datosEvenSis": datosSis}
            print(res)
            return JsonResponse(res, safe=False)

        if action == "get_eventos_sismicos":
            # mostrarEventosSismicos()
            evento1 = EventoSismico.objects.get(id=1)
            evento2 = EventoSismico.objects.get(id=2)
            return JsonResponse([evento1.as_dict(), evento2.as_dict()], safe=False)

        return render(request, "reg_revision.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        return JsonResponse({"error": "Método no permitido"}, status=405)
