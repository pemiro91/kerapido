import datetime
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from Ke_Rapido import settings

ESTADO_ENTREGA = (
    ('Pendiente', 'Pendiente'),
    ('Cancelado', 'Cancelado'),
    ('Entregado', 'Entregado')
)


# Create your models here.
# def images_directory_path(instance, filename):
#     return '/'.join(['images', str(instance.title), str(uuid.uuid4().hex + ".png")])


class User(AbstractUser):
    logo = models.ImageField(upload_to='logo/%Y/%m/%d', null=True, blank=True)
    persona_encargada = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    especialidad = models.CharField(max_length=255, null=True, blank=True)
    provincia = models.CharField(max_length=255, null=True, blank=True)
    municipio = models.CharField(max_length=255, null=True, blank=True)
    is_cliente = models.BooleanField(default=False)
    is_negocio = models.BooleanField(default=False)
    is_administrador = models.BooleanField(default=False)


class ComentarioEvaluacion(models.Model):
    rating = models.PositiveIntegerField(null=True, blank=True)
    comentario = models.CharField(max_length=255, null=True, blank=True)
    negocio = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='negocio')


class Plato(models.Model):
    imagen = models.ImageField(upload_to='imagen_plato/%Y/%m/%d', null=True, blank=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    precio = models.CharField(max_length=255)
    negocio = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='negocio')

    def __str__(self): return str(self.nombre)


class Tarifa(models.Model):
    lugar_destino = models.CharField(max_length=255)
    precio = models.FloatField(max_length=55)
    negocio = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, name='negocio')

    def __str__(self): return str(self.lugar_destino)


class Agrego(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.FloatField(max_length=255)
    negocio = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, name='negocio')

    def __str__(self): return str(self.nombre)


class Reservacion_Simple(models.Model):
    cantidad_producto = models.IntegerField(name='cantidad_producto')
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE, name='plato')
    agregos = models.CharField(max_length=255, null=True, blank=True, name='agregos')

    def __str__(self): return str(self.plato)


class Reservacion_Generada(models.Model):
    cliente_auth = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, name='cliente_auth')
    total = models.FloatField(max_length=255)
    fecha_reservacion = models.DateField(default=datetime.date.today)
    cliente_entrega = models.CharField(max_length=255)
    telefono_entrega = models.CharField(max_length=255)
    direccion_entrega = models.CharField(max_length=255)
    reservaciones = models.ManyToManyField(Reservacion_Simple)
    estado = models.CharField(max_length=50, default='Pendiente', name='estado')
    fecha_estado = models.DateField(default=datetime.date.today)
