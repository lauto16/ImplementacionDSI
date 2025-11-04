import os
import django
from datetime import datetime


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Implementacion.settings')
django.setup()

from Main.models.EstadoEventoSismico import Autodetectado, Confirmado, Rechazado, BloqueadoEnRevision
from Main.models.EventoSismico import EventoSismico
from Main.models.Empleado import Empleado

evento_sismico = EventoSismico.objects.get(idCompuesto='-31.41;-64.19')
empleado = Empleado.objects.get(mail='cgomez@example.com')

print(evento_sismico.estadoActual)
evento_sismico.bloquear(fecha_actual=datetime(2025, 10, 28, 0, 0), empleado=empleado)
print(evento_sismico.estadoActual)
evento_sismico.rechazar(fecha_actual=datetime(2025, 10, 28, 0, 0), empleado=empleado)
print(evento_sismico.estadoActual)
