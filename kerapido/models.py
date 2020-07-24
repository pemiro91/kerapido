from django.db import models
import uuid
from .validators import validate_file_extension
from django.contrib.auth.models import AbstractUser
import datetime
from Ke_Rapido import settings

ESTADO_ENTREGA = (
    ('Pendiente', 'Pendiente'),
    ('Cancelado', 'Cancelado'),
    ('Entregado', 'Entregado')
)


# Create your models here.
def images_directory_path(instance, filename):
    return '/'.join(['images', str(instance.title), str(uuid.uuid4().hex + ".png")])


class User(AbstractUser):
    telefono = models.CharField(max_length=255, null=True, blank=True)
    is_cliente = models.BooleanField(default=False)
    is_negocio = models.BooleanField(default=False)
    is_administrador = models.BooleanField(default=False)

    def get_perfil_negocio(self):
        perfil_negocio = None
        if hasattr(self, 'perfilnegocio'):
            perfil_negocio = self.perfil_negocio
        return perfil_negocio


class PerfilNegocio(models.Model):
    usuario = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='logo/%Y/%m/%d', null=True, blank=True)
    especialidad = models.CharField(max_length=255, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    provincia = models.CharField(max_length=255, null=True, blank=True)
    municipio = models.CharField(max_length=255, null=True, blank=True)
    persona_encargada = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.id


class ComentarioEvaluacion(models.Model):
    rating = models.PositiveIntegerField(null=True, blank=True)
    comentario = models.CharField(max_length=255, null=True, blank=True)
    negocio = models.ForeignKey(PerfilNegocio, on_delete=models.CASCADE)


class Plato(models.Model):
    imagen = models.ImageField(upload_to='imagen_plato/%Y/%m/%d', null=True, blank=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    precio = models.CharField(max_length=255)
    negocio = models.ForeignKey(PerfilNegocio, on_delete=models.CASCADE)

    def str(self):
        return str(self.nombre)


class Tarifa(models.Model):
    lugar_destino = models.CharField(max_length=255)
    precio = models.FloatField(max_length=55)
    negocio = models.ForeignKey(PerfilNegocio, on_delete=models.CASCADE, name='negocio')

    def str(self): return str(self.lugar_destino)


class Agrego(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.FloatField(max_length=255)
    negocio = models.ForeignKey(PerfilNegocio, on_delete=models.CASCADE, name='negocio')

    def str(self): return str(self.nombre)


class Reservacion_Simple(models.Model):
    cantidad_producto = models.IntegerField(name='cantidad_producto')
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE, name='plato')
    agregos = models.CharField(max_length=255, null=True, blank=True, name='agregos')

    def str(self): return str(self.plato)


class Reservacion_Generada(models.Model):
    cliente_auth = models.ForeignKey(User, on_delete=models.CASCADE, name='cliente_auth')
    total = models.FloatField(max_length=255)
    fecha_reservacion = models.DateField(default=datetime.date.today)
    cliente_entrega = models.CharField(max_length=255)
    telefono_entrega = models.CharField(max_length=255)
    direccion_entrega = models.CharField(max_length=255)
    reservaciones = models.ManyToManyField(Reservacion_Simple)
    estado = models.CharField(max_length=50, default='Pendiente', name='estado')
    fecha_estado = models.DateField(default=datetime.date.today)
