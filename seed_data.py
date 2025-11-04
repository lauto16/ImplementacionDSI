from Main.models import (
    OrigenDeGeneracion,
    ClasificacionSismo,
    MagnitudRichter,
    AlcanceSismo,
    Estado,
    TipoDeDato,
    EstacionSismologica,
    Empleado,
    Usuario,
    CambioEstado,
    DetalleMuestraSismica,
    MuestraSismica,
    SerieTemporal,
    Sismografo,
    EventoSismico,
)
from django.utils import timezone
from random import uniform, choice
from datetime import datetime
import os
import django
# Configurar entorno
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_proyecto.settings')
django.setup()


# Limpieza opcional de tablas (solo en entorno de desarrollo)


def clear_all():
    models = [
        EventoSismico, Sismografo, SerieTemporal, MuestraSismica, DetalleMuestraSismica,
        CambioEstado, Usuario, Empleado, Estado, EstacionSismologica, TipoDeDato,
        AlcanceSismo, MagnitudRichter, ClasificacionSismo, OrigenDeGeneracion
    ]
    for m in models:
        m.objects.all().delete()
    print("🧹 Tablas limpiadas")


def seed():
    print("🌱 Cargando datos iniciales...")

    # ==== Origen de Generación ====
    og1 = OrigenDeGeneracion.objects.create(
        nombre="Tectónico", descripcion="Sismo originado por movimientos de placas"
    )
    og2 = OrigenDeGeneracion.objects.create(
        nombre="Volcánico", descripcion="Sismo asociado a actividad volcánica"
    )

    # ==== Clasificación Sismo ====
    c1 = ClasificacionSismo.objects.create(
        nombre="Superficial", kmProfundidadDesde=0, kmProfundidadHasta=70
    )
    c2 = ClasificacionSismo.objects.create(
        nombre="Intermedio", kmProfundidadDesde=70, kmProfundidadHasta=300
    )

    # ==== Magnitud ====
    m1 = MagnitudRichter.objects.create(
        numero=4.5, descripcionMagnitud="Moderado")
    m2 = MagnitudRichter.objects.create(
        numero=6.2, descripcionMagnitud="Fuerte")

    # ==== Alcance ====
    a1 = AlcanceSismo.objects.create(
        nombre="Local", descripcion="Percibido en una zona reducida")
    a2 = AlcanceSismo.objects.create(
        nombre="Regional", descripcion="Percibido en varias provincias")

    # ==== Estados ====
    e1 = Estado.objects.create(
        nombreEstado="Autodetectado", ambito="EventoSismico")
    e2 = Estado.objects.create(
        nombreEstado="Confirmado", ambito="EventoSismico")
    e3 = Estado.objects.create(
        nombreEstado="Rechazado", ambito="EventoSismico")

    # ==== Tipo de Dato ====
    td1 = TipoDeDato.objects.create(
        denominacion="Aceleración", nombreUnidadMedida="m/s^2", valorUmbral=0.5
    )
    td2 = TipoDeDato.objects.create(
        denominacion="Velocidad", nombreUnidadMedida="m/s", valorUmbral=1.0
    )

    # ==== Estación Sismológica ====
    es1 = EstacionSismologica.objects.create(
        codigoEstacion="ES001",
        nombre="Estación Central",
        latitud=-31.4,
        longitud=-64.2,
        documentoCertificacionAdq="Certificado 2025",
        nroCertificacionAdquisicion="A-001",
        fechaSolicitudCertificacion=timezone.now(),
    )

    # ==== Empleados / Usuarios ====
    emp1 = Empleado.objects.create(
        nombre="Carlos", apellido="Gómez", mail="cgomez@example.com", telefono="3515551234"
    )
    emp2 = Empleado.objects.create(
        nombre="Laura", apellido="Pérez", mail="lperez@example.com", telefono="3515555678"
    )

    user1 = Usuario.objects.create(
        empleado=emp1, contrasenia="1234", nombreUsuario="cgomez")
    user2 = Usuario.objects.create(
        empleado=emp2, contrasenia="abcd", nombreUsuario="lperez")

    # ==== Cambios de Estado ====
    ce1 = CambioEstado.objects.create(
        fechaHoraInicio=timezone.now(), estado=e1, responsableInspeccion=emp1
    )
    ce2 = CambioEstado.objects.create(
        fechaHoraInicio=timezone.now(), estado=e2, responsableInspeccion=emp2
    )

    # ==== Datos de Muestras ====
    dm1 = DetalleMuestraSismica.objects.create(valor=0.45, tipoDeDato=td1)
    dm2 = DetalleMuestraSismica.objects.create(valor=1.23, tipoDeDato=td2)

    ms1 = MuestraSismica.objects.create(fechaHoraMuestra=timezone.now())
    ms1.detalleMuestraSismica.add(dm1, dm2)

    # ==== Serie Temporal ====
    st1 = SerieTemporal.objects.create(
        condicionAlarma="Alarma leve",
        frecuenciaMuestreo=2.5,
        fechaHoraInicioRegistroMuestras=timezone.now(),
        fechaHoraRegistros=timezone.now(),
        estado=e1,
    )
    st1.muestraSismica.add(ms1)

    st2 = SerieTemporal.objects.create(
        condicionAlarma="Alarma fuerte",
        frecuenciaMuestreo=5.0,
        fechaHoraInicioRegistroMuestras=timezone.now(),
        fechaHoraRegistros=timezone.now(),
        estado=e2,
    )

    # ==== Sismógrafo ====
    s1 = Sismografo.objects.create(
        identificadorSismografo="SIS-001",
        nroSerie="N-001",
        estacionSismologica=es1,
        fechaAdquisicion=timezone.now(),
    )
    s1.serieTemporal.add(st1, st2)

    # ==== Evento Sísmico ====
    ev = EventoSismico.objects.create(
        idCompuesto="EV001",
        fechaHoraOcurrencia=timezone.now(),
        latitudEpicentro=-31.41,
        longitudEpicentro=-64.19,
        latitudHipocentro=-31.45,
        longitudHipocentro=-64.20,
        magnitud=m1,
        origenGeneracion=og1,
        alcanceSismo=a1,
        estadoActual=e1,
        clasificacion=c1,
        fechaHoraFin=timezone.now(),
    )
    ev.cambiosEstado.add(ce1, ce2)
    ev.serieTemporal.add(st1, st2)

    print("✅ Datos iniciales cargados correctamente.")


if __name__ == "__main__":
    clear_all()
    seed()
