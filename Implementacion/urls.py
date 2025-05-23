from Main.views import InterfazResultRevManual, opciones_sismografo
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('opciones/registrar_resultado_revision_manual/', InterfazResultRevManual.as_view(), name='registrar_resultado_revision_manual'),
    path('opciones/', opciones_sismografo, name='opciones'),
]