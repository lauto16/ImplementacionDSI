# IMPORTS DE MODELOS
from Main.models import (
    Empleado,
    Sesion,
    Estado,
    Sismografo,
    EventoSismico,
)
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from datetime import datetime
from django.views import View
import json


class GestorResultRevManual:

    def __init__(self, interfaz) -> None:
        self.eventos = self.getEventos()
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
        self.estado_Rechazado = None
        self.empleado = None
        self.sesion = Sesion.objects.get(id=1)
        self.datos_eventos_autodetectados = []

    def getEventos(self):
        return list(EventoSismico.objects.all())

    def getEventoPorId(self, id: int):
        return EventoSismico.objects.get(id=id)

    def separarTexto(self, texto: str) -> tuple[str, str]:
        partes = texto.split("-", 1)
        nombre = partes[0].strip()
        descripcion = partes[1].strip()
        return nombre, descripcion

    def validarDatosSismicos(self, valor, type: str) -> bool:
        print(valor, type)
        if type == "texto":
            if "-" not in valor:
                return False

            partes = valor.split("-", 1)
            nombre = partes[0].strip()
            descripcion = partes[1].strip()
            return bool(nombre) and bool(descripcion)

        elif type == "magnitud":
            if isinstance(valor, float):
                return True
            try:
                valor = float(valor)
                return True
            except:
                return False

    def getFechaHoraActual(self) -> datetime:
        return timezone.now()

    def getEventoAutodetectado(self, id: int) -> EventoSismico:
        for evento in self.eventosAutodetectados:
            if evento.id == id:
                return evento

    def tomarSelEventoSis(self, id_evento: int) -> None:
        # se necesita buscar el evento elegio entre los autodetectados
        self.eventosAutodetectados = self.buscarEventosAutodetectados()
        self.eventoSisActual = self.getEventoAutodetectado(id=id_evento)

        # luego de obtener los datos de nuevo (la request borra los objetos) continuamos con el CU
        self.estado_BloqueadoEnRevision = self.buscarEstadoBloqueadoEnRevision()
        self.fechaHoraActual = self.getFechaHoraActual()
        self.bloquearEventoSis()
        self.buscarDatosEventoSis()

        datosEvenSis = {
            "alcanceEventoSis": self.alcanceEventoSis,
            "clasificacionEventoSis": self.clasificacionEventoSis,
            "origenGeneracionEventoSis": self.origenGeneracionEventoSis,
        }

        datosSeriesTemporales = self.buscarSerieTemporal()
        self.ordenarPorEstacion(datosSeriesTemporales=datosSeriesTemporales)
        self.sismograma = self.llamarCUGenerarSismograma()

        # estructurar datos para el frontend
        datos_entrega = []
        for i in range(len(self.ordenadoPorES)):
            datosSerieTemporal = {
                "nombreEstacion": self.ordenadoPorES[i]["estacionSismologica"].nombre,
                "muestra": self.ordenadoPorES[i]["datosMuestras"],
            }
            datos_entrega.append(datosSerieTemporal)

        diccionario_retorno = self.mostrarVisualizarMapaYDatos(
            datos_entrega, datosEvenSis, self.sismograma
        )
        return diccionario_retorno

    def getEventosAutodetectados(self) -> list:
        for evento in self.eventos:
            if evento.esAutodetectado():
                self.eventosAutodetectados.append(evento)
        self.ordenarEventosSisPorFyH()
        self.datos_eventos_autodetectados = [
            x.obtenerDatos() for x in self.eventosAutodetectados if x is not None
        ]
        return self.datos_eventos_autodetectados

    def bloquearEventoSis(self) -> None:
        self.eventoSisActual.bloquear(
            fecha_actual=self.fechaHoraActual, estado=self.estado_BloqueadoEnRevision
        )

    def ordenarEventosSisPorFyH(self) -> None:
        self.datos_eventos_autodetectados = sorted(
            self.datos_eventos_autodetectados,
            key=lambda x: datetime.strptime(
                x["fechaHoraOcurrencia"], "%Y-%m-%d %H:%M:%S"
            ),
        )

    def buscarEstadoBloqueadoEnRevision(self) -> Estado:
        for estado in self.estados:
            if estado.esAmbitoEventoSis():
                if estado.esBloqueadoEnRevision():
                    return estado

    def buscarEventosAutodetectados(self) -> list:
        for evento in self.eventos:
            if evento.estadoActual.esAutodetectado:
                self.eventosAutodetectados.append(evento)
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

    def buscarEstadoRechazado(self) -> Estado:
        for estado in self.estados:
            if estado.esAmbitoEventoSis():
                if estado.esRechazado():
                    return estado

    def tomarOpcionAccion(self, accion, evento_id, alcance, origen, magnitud, save):
        if not (
            self.validarDatosSismicos(alcance, type="texto")
            and self.validarDatosSismicos(origen, type="texto")
            and self.validarDatosSismicos(magnitud, type="magnitud")
        ):
            return JsonResponse({"succcess": False, "error": "ERROR DE TIPO"})

        nombre_alcance, descripcion_alcance = self.separarTexto(alcance)
        nombre_origen, descripcion_origen = self.separarTexto(origen)

        # flujo alternativo: El analista de sismos modifica los datos del evento sismico
        if save:
            print('dsajidsakjdasjkdsajkpo')
            evento_modificado = None
            try:
                evento_modificado = EventoSismico.objects.get(id=evento_id)
                print(evento_modificado)
            except EventoSismico.DoesNotExist:
                return JsonResponse(
                    {"success": False, "message": "El evento sismico no existe"}
                )

            evento_modificado.magnitud.numero = magnitud
            evento_modificado.magnitud.save()

            evento_modificado.alcanceSismo.nombre = nombre_alcance
            evento_modificado.alcanceSismo.descripcion = descripcion_alcance
            evento_modificado.alcanceSismo.save()

            evento_modificado.origenGeneracion.nombre = nombre_origen
            evento_modificado.origenGeneracion.descripcion = descripcion_origen
            evento_modificado.origenGeneracion.save()

            evento_modificado.save()

        self.eventoSisActual = self.getEventoPorId(id=evento_id)
        self.fechaHoraActual = self.getFechaHoraActual()

        if accion == "rechazar":
            self.estado_Rechazado = self.buscarEstadoRechazado()
            self.eventoSisActual.rechazar(fecha_actual=self.fechaHoraActual)
            self.empleado = self.sesion.buscarUsuarioLogueado()
            self.crearCambioEstado(
                empleado=self.empleado,
                fecha_actual=self.fechaHoraActual,
                estado=self.estado_Rechazado,
            )

        elif accion == "confirmar":
            # caso alternativo: Si la opción seleccionada es Confirmar evento, se actualiza el estado del evento sísmico a confirmado, registrando la fecha y hora actual como fecha de confirmación.
            self.estado_Confirmado = self.buscarEstadoConfirmado()
            self.eventoSisActual.confirmar(
                fecha_actual=self.fechaHoraActual,
                estado=self.estado_Confirmado,
                empleado=self.empleado,
            )

        self.finCU()

    def buscarEstadoConfirmado(self) -> Estado:
        for estado in self.estados:
            if estado.esAmbitoEventoSis():
                if estado.esConfirmado():
                    return estado

    def crearCambioEstado(self, fecha_actual, estado, empleado: Empleado) -> None:
        self.eventoSisActual.crearCambioEstado(
            fecha_actual=fecha_actual, estado=estado, empleado=empleado
        )

    def finCU(self):
        print(self.eventoSisActual)
        return "FIN CU"

    def mostrarVisualizarMapaYDatos(
        self, datos_entrega, datosEvenSis, sismograma
    ) -> dict:
        return {
            "datos_entrega": datos_entrega,
            "datosEvenSis": datosEvenSis,
            "sismograma": sismograma,
        }

    def ofrecerModificarEvento(self):
        return True

    def tomarConfirmacionVisualizacion(self):
        response = self.ofrecerModificarEvento()
        if response:
            return True
        return False


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

    def mostrarEventosSis(self, data) -> JsonResponse:
        return JsonResponse(data, safe=False)

    def mostrarVisualizarMapaYDatos(self, data) -> JsonResponse:
        return JsonResponse(data, safe=False)

    def get(self, request: HttpRequest) -> HttpResponse:
        action = request.GET.get("action")

        # representa al metodo tomarSelEventoSis()
        if action == "tomar_sel_evento_sismico":
            id_evento = request.GET.get("id_evento")
            diccionario_retorno = self.gestor.tomarSelEventoSis(
                id_evento=int(id_evento)
            )
            res = {
                "serieTemp": diccionario_retorno["datos_entrega"],
                "datosEvenSis": diccionario_retorno["datosEvenSis"],
                "sismograma": diccionario_retorno["sismograma"],
            }
            # solicitarConfirmacionVisualizacion() (se ejecuta en el frontend)
            return self.mostrarVisualizarMapaYDatos(res)

        # representa a el metodo getEventosSismicos()
        if action == "get_eventos_sismicos":
            eventos_autodetectados = self.gestor.getEventosAutodetectados()
            return self.mostrarEventosSis(eventos_autodetectados)

        # representa a el metodo tomarConfirmacionVisualizacion()
        if action == "tomar_confirmacion_visualizacion":
            respuesta_confirmacion = self.gestor.tomarConfirmacionVisualizacion()
            if respuesta_confirmacion:
                # ofrecerModificarEvento() y pedirAccion() (se ejecutan en el frontend)
                return JsonResponse(
                    {"success": True, "action": "ofrecerModificarEvento"}
                )

        return render(request, "reg_revision.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        # tomarModificacionDatos
        try:
            data = json.loads(request.body)
            id_evento = data.get("id_evento")
            action = data.get("action")
            action_to_do = data.get("actionToDo")

            alcance = data.get("alcance")
            origen = data.get("origen")
            magnitud = data.get("magnitud")

            if action_to_do is None:
                return JsonResponse(
                    {"success": False, "error": "Seleccione una accion para hacer"}
                )

            if action == "save":
                self.gestor.tomarOpcionAccion(
                    accion=action_to_do,
                    evento_id=id_evento,
                    save=True,
                    alcance=alcance,
                    origen=origen,
                    magnitud=magnitud,
                )

            else:
                self.gestor.tomarOpcionAccion(
                    accion=action_to_do,
                    evento_id=id_evento,
                    save=False,
                    alcance=alcance,
                    origen=origen,
                    magnitud=magnitud,
                )

            return JsonResponse(
                {
                    "success": True,
                    "message": "Se aplico la accion seleccionada",
                    "accion_realizada": action_to_do,
                    "se_guardo": action,
                }
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "message": "Error al decodificar el JSON"},
                status=400,
            )
