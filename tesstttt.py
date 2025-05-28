tipo_dato_evento = TipoDeDato("altura_terreno", "metros", 150)

empleado = Empleado(apellido='Doe', nombre='John',
                    telefono='3516565784', mail='johndoe123@gmail.com')
user = Usuario(contrasenia='123456789',
               nombreUsuario='John Doe', empleado=empleado)
sesion = Sesion(usuario=user)
estacion1 = EstacionSismologica(codigoEstacion=1, documentoCertificacionAdq=None, fechaSolicitudCertificacion=None,
                                latitud=-34.6037, longitud=-58.3816, nombre='Estacion Cordoba', nroCertificacionAdquisicion=10)
estacion2 = EstacionSismologica(codigoEstacion=2, documentoCertificacionAdq=None, fechaSolicitudCertificacion=None,
                                latitud=31.5370, longitud=-68.5360, nombre='Estacion San Juan', nroCertificacionAdquisicion=11)
fecha_inicio_1 = datetime.strptime(
    "12/12/2004 12:45", "%d/%m/%Y %H:%M")
fecha_fin_1 = datetime.strptime(
    "12/12/2004 12:50", "%d/%m/%Y %H:%M")
fecha_inicio_2 = datetime.strptime(
    "15/07/2010 09:30", "%d/%m/%Y %H:%M")
fecha_fin_2 = datetime.strptime(
    "15/07/2010 09:45", "%d/%m/%Y %H:%M")
magnitud1 = MagnitudRichter("escala base", 7.1)
magnitud2 = MagnitudRichter("escala base", 6.3)
origen1 = OrigenDeGeneracion("Capital zona rural", "Cordoba")
origen2 = OrigenDeGeneracion("Zona costera", "San Juan")
alcance1 = AlcanceSismo(
    nombre="Zonas aledañas camino Alta Gracia", descripcion="Zonas aledañas")
alcance2 = AlcanceSismo(
    nombre="Zonas aledañas tiramay", descripcion="Zonas aledañas")
clasificacion1 = ClasificacionSismo(12.3, 15.6, "distancia")
clasificacion2 = ClasificacionSismo(20.4, 10.1, "distancia")
cambio1 = CambioEstado(fechaHoraInicio=fecha_inicio_1, fechaHoraFin=None,
                       estado=autodetectado, responsableInspeccion=empleado)
cambio2 = CambioEstado(fechaHoraInicio=fecha_inicio_2, fechaHoraFin=None,
                       estado=autodetectado, responsableInspeccion=empleado)
muestra1 = MuestraSismica(fecha_inicio_1)
muestra1.crearDetalleMuestra(
    valor=120.54, tipo_dato=tipo_dato_evento)
muestra2 = MuestraSismica(fecha_inicio_2)
muestra2.crearDetalleMuestra(
    valor=1200.54, tipo_dato=tipo_dato_evento)
serie1 = SerieTemporal(condicionAlarma="temblar", fechaHoraInicioRegistroMuestras=fecha_inicio_1,
                       fechaHoraRegistros=fecha_fin_1, frecuenciaMuestreo=1.5, estado=sin_alarma, muestrasSismica=[muestra1])
serie2 = SerieTemporal(condicionAlarma="temblar", fechaHoraInicioRegistroMuestras=fecha_inicio_2,
                       fechaHoraRegistros=fecha_fin_2, frecuenciaMuestreo=2.5, estado=sin_alarma, muestrasSismica=[muestra2])
series1 = []
series2 = []
series1.append(serie1)
series2.append(serie2)
sismografo1 = Sismografo(estacionSismologica=estacion1, fechaAdquisicion=datetime.strptime(
    "12/10/1998 12:30", "%d/%m/%Y %H:%M"), identificadorSismografo=1234, nroSerie=9089989898, seriesTemporales=series1)
sismografo2 = Sismografo(estacionSismologica=estacion2, fechaAdquisicion=datetime.strptime(
    "12/10/1999 10:12", "%d/%m/%Y %H:%M"), identificadorSismografo=1235, nroSerie=9089989899, seriesTemporales=series2)
self.gestor.sismografos.append(sismografo1)
self.gestor.sismografos.append(sismografo2)
evento1 = EventoSismico(id=1, fechaHoraFin=fecha_fin_1, fechaHoraOcurrencia=fecha_inicio_1, latitudEpicentro=-34.6037, longitudEpicentro=-58.3816, latitudHipocentro=-30.6070, longitudHipocentro=-
                        50.1045, magnitud=magnitud1, origenGeneracion=origen1, alcanceSismo=alcance1, estadoActual=autodetectado, clasificacion=clasificacion1, cambiosEstado=[cambio1], seriesTemporales=[serie1])
evento2 = EventoSismico(id=2, fechaHoraFin=fecha_fin_2, fechaHoraOcurrencia=fecha_inicio_2, latitudEpicentro=-31.5370, longitudEpicentro=-68.5360, latitudHipocentro=-32.0000, longitudHipocentro=-
                        67.5000, magnitud=magnitud2, origenGeneracion=origen2, alcanceSismo=alcance2, estadoActual=autodetectado, clasificacion=clasificacion2, cambiosEstado=[cambio2], seriesTemporales=[serie2])
eventos = [evento1, evento2]
eventos_autodetectados = self.gestor.buscarEventosAutodetectados(
    eventos=eventos)
#self.gestor.eventosAutodetectados = eventos_autodetectados
eventos_autodetectados_para_frontend = [
    x.as_dict() for x in eventos_autodetectados]
# Guardar datos base
tipo_dato_evento.save()
empleado.save()
user.empleado = empleado
user.save()
sesion.usuario = user
sesion.save()
estacion1.save()
estacion2.save()
magnitud1.save()
magnitud2.save()
origen1.save()
origen2.save()
alcance1.save()
alcance2.save()
clasificacion1.save()
clasificacion2.save()
# Guardar cambios de estado
cambio1.responsableInspeccion = empleado
cambio1.estado = autodetectado
cambio1.save()
cambio2.responsableInspeccion = empleado
cambio2.estado = autodetectado
cambio2.save()
# Guardar muestras y detalles
muestra1.save()
muestra1.crearDetalleMuestra(valor=120.54, tipo_dato=tipo_dato_evento)
muestra2.save()
muestra2.crearDetalleMuestra(valor=1200.54, tipo_dato=tipo_dato_evento)
# Guardar series temporales
serie1.estado = sin_alarma
serie1.save()
serie1.muestrasSismica.add(muestra1)
serie2.estado = sin_alarma
serie2.save()
serie2.muestrasSismica.add(muestra2)
# Guardar sismógrafos
sismografo1.estacionSismologica = estacion1
sismografo1.save()
sismografo1.seriesTemporales.add(serie1)
sismografo2.estacionSismologica = estacion2
sismografo2.save()
sismografo2.seriesTemporales.add(serie2)
# Guardar eventos
evento1.magnitud = magnitud1
evento1.origenGeneracion = origen1
evento1.alcanceSismo = alcance1
evento1.estadoActual = autodetectado
evento1.clasificacion = clasificacion1
evento1.save()
evento1.cambiosEstado.add(cambio1)
evento1.seriesTemporales.add(serie1)
evento2.magnitud = magnitud2
evento2.origenGeneracion = origen2
evento2.alcanceSismo = alcance2
evento2.estadoActual = autodetectado
evento2.clasificacion = clasificacion2
evento2.save()
evento2.cambiosEstado.add(cambio2)
evento2.seriesTemporales.add(serie2)