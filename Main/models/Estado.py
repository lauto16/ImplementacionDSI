from django.db import models

class Estado(models.Model):
    """
    Esta clase se usa para persistir los estados de los eventos sismicos, ya que
    django no soporta claves foraneas de tablas variables o de objetos abstractos /
    objetos que no sean models
    """

    ambito = models.CharField(max_length=100)
    nombreEstado = models.CharField(max_length=100, primary_key=True)

