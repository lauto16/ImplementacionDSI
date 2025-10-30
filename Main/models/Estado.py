from django.db import models


class Estado(models.Model):
    nombreEstado = models.CharField(max_length=100)
