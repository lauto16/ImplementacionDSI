from django.db import models

class MagnitudRichter(models.Model):
    descripcionMagnitud = models.CharField(max_length=200)
    numero = models.FloatField()

