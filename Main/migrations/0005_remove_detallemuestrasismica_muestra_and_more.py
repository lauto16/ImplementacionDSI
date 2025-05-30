# Generated by Django 5.2.1 on 2025-05-28 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0004_remove_serietemporal_evento_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detallemuestrasismica',
            name='muestra',
        ),
        migrations.RemoveField(
            model_name='muestrasismica',
            name='serieTemporal',
        ),
        migrations.RemoveField(
            model_name='serietemporal',
            name='sismografo',
        ),
        migrations.AddField(
            model_name='muestrasismica',
            name='detalleMuestraSismica',
            field=models.ManyToManyField(to='Main.detallemuestrasismica'),
        ),
        migrations.AddField(
            model_name='serietemporal',
            name='muestraSismica',
            field=models.ManyToManyField(to='Main.muestrasismica'),
        ),
        migrations.AddField(
            model_name='sismografo',
            name='serieTemporal',
            field=models.ManyToManyField(to='Main.serietemporal'),
        ),
    ]
