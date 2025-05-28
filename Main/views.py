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
import json
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

    def getEventos(self):
        return list(EventoSismico.objects.all())
    
    def getEventoPorId(self, id: int):
        return EventoSismico.objects.get(id=id)

    def separarTexto(self, texto: str) -> tuple[str, str]:
        partes = texto.split('-', 1)
        nombre = partes[0].strip()
        descripcion = partes[1].strip()
        return nombre, descripcion

    def validarDatosSismicos(self, texto: str) -> bool:
        if "-" not in texto:
            return False
        partes = texto.split("-", 1)
        nombre = partes[0].strip()
        descripcion = partes[1].strip()
        return bool(nombre) and bool(descripcion)

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

        datos_entrega = []
        for i in range(len(self.ordenadoPorES)):
            datosSerieTemporal = {
                "nombreEstacion": self.ordenadoPorES[i]["estacionSismologica"].nombre,
                "muestra": self.ordenadoPorES[i]["datosMuestras"],
            }
            datos_entrega.append(datosSerieTemporal)
        self.sismograma = self.llamarCUGenerarSismograma()

        diccionario_retorno = self.mostrarVisualizarMapaYDatos(
            datos_entrega, datosEvenSis, self.sismograma
        )
        return diccionario_retorno

    def getEventoAutodetectado(self, id: int):
        for evento in self.eventos:
            if id == evento.id:
                if evento.estadoActual.esAutodetectado():
                    print(evento.estadoActual.esAutodetectado)
                    return evento

    def bloquearEventoSis(self) -> None:
        self.eventoSisActual.bloquear(
            fecha_actual=self.fechaHoraActual, estado=self.estado_BloqueadoEnRevision
        )

    def ordenarEventosSisPorFyH(self) -> None:
        self.eventosAutodetectados.sort(key=lambda evento: evento.fechaHoraOcurrencia)

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
    
    def buscarEstadoRechazado(self) -> Estado:
        print('ESTADOS: ', self.estados)
        for estado in self.estados:
            if estado.esAmbitoEventoSis():
                if estado.esRechazado():
                    return estado

    def tomarOpcionAccion(self, accion, evento_id):
        if accion == "rechazar":
            self.eventoSisActual = self.getEventoPorId(id=evento_id)
            self.fechaHoraActual = self.getFechaHoraActual()
            self.estado_Rechazado = self.buscarEstadoRechazado()
            self.eventoSisActual.rechazar(
                fecha_actual=self.fechaHoraActual, estado=self.estado_Rechazado)
            self.empleado = self.sesion.buscarUsuarioLogueado()

            self.crearCambioEstado(empleado=self.empleado, fecha_actual=self.fechaHoraActual, estado=self.estado_Rechazado)
            self.finCU()
            print(self.eventoSisActual.as_dict())
        elif accion == '':
            # caso alternativo
            pass
    
    def crearCambioEstado(self, fecha_actual, estado, empleado: Empleado)-> None:
        self.eventoSisActual.crearCambioEstado(fecha_actual=fecha_actual, estado=estado, empleado=empleado)
    
    def finCU(self):
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

    def tomarConfirmacionVisualizacion(self, respuesta: str):
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

    def get(self, request: HttpRequest) -> HttpResponse:
        action = request.GET.get("action")

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
            return JsonResponse(res, safe=False)

        if action == "get_eventos_sismicos":
            # mostrarEventosSismicos()
            evento1 = self.gestor.getEventoAutodetectado(id=1) 
            evento2 = self.gestor.getEventoAutodetectado(id=2)
            eventos = [evento1, evento2]

            return JsonResponse([x.as_dict() for x in eventos if x is not None], safe=False)

        if action == "tomar_confirmacion_visualizacion":
            respuesta = request.GET.get("respuesta")
            respuesta_confirmacion = self.gestor.tomarConfirmacionVisualizacion(
                respuesta=respuesta
            )
            if respuesta_confirmacion:
                # ofrecerModificarEvento() (se ejecuta en el frontend)
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
            action_to_do = data.get('actionToDo')

            if action_to_do is None:
                return JsonResponse({'success': False, 'error': 'Seleccione una accion para hacer'})

            if action == 'save':

                alcance = data.get("alcance")
                origen = data.get("origen")
                magnitud = data.get("magnitud")

                if not self.gestor.validarDatosSismicos(texto=alcance):
                    return JsonResponse(
                        {
                            "success": False,
                            "error": "El alcance debe separar por un guion el nombre y la descripción",
                        }
                    )

                if not self.gestor.validarDatosSismicos(texto=origen):
                    return JsonResponse(
                        {
                            "success": False,
                            "error": "El origen debe separar por un guion el nombre y la descripción",
                        }
                    )
                
                nombre_alcance, descripcion_alcance = self.gestor.separarTexto(alcance)
                nombre_origen, descripcion_origen = self.gestor.separarTexto(origen)

                if not isinstance(magnitud, float):
                    try:
                        magnitud = float(magnitud)
                    except:
                        return JsonResponse(
                            {
                                "success": False,
                                "error": "La magnitud debe ser un número decimal",
                            }
                    )

                # curso alternativo: El analista de sismos modifica los datos del evento sismico
                evento_modificado = None
                try:
                    evento_modificado = EventoSismico.objects.get(id=id_evento)
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

            elif action == 'dontSave':
                pass

            self.gestor.tomarOpcionAccion(accion=action_to_do, evento_id=id_evento)

            return JsonResponse({'success': True, 'message': 'Se aplico la accion seleccionada', 'accion_realizada': action_to_do, 'se_guardo': action})
                
        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "message": "Error al decodificar el JSON"},
                status=400,
            )
