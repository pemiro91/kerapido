import datetime
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

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
    is_afiliado = models.BooleanField(default=False)
    is_persona_encargada = models.BooleanField(default=False)
    is_administrador = models.BooleanField(default=False)
    fecha_alta = models.DateTimeField(default=timezone.now)


class Servicio(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.nombre


class Categoria_Negocio(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.FloatField(max_length=55)

    def str(self): return str(self.nombre)


class Negocio(models.Model):
    usuario_negocio = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logo/%Y/%m/%d', null=True, blank=True)
    portada = models.ImageField(upload_to='portada/%Y/%m/%d', null=True, blank=True)
    provincia = models.CharField(max_length=255, null=True, blank=True)
    municipio = models.CharField(max_length=255, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    telefono1 = models.CharField(max_length=255, null=True, blank=True)
    telefono2 = models.CharField(max_length=255, null=True, blank=True)
    horario = models.CharField(max_length=255, null=True, blank=True)
    slogan = models.CharField(max_length=255, null=True, blank=True)
    servicios = models.ManyToManyField(Servicio)
    rating = models.FloatField(null=True, blank=True)
    categoria = models.ForeignKey(Categoria_Negocio, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.nombre


class Categoria_Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.FloatField(max_length=55)

    def str(self): return str(self.nombre)


class Producto(models.Model):
    imagen = models.ImageField(upload_to='imagen_plato/%Y/%m/%d', null=True, blank=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    precio = models.CharField(max_length=255)
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria_Producto, on_delete=models.CASCADE)

    def str(self):
        return str(self.nombre)


class Reservacion_Simple(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, name='plato')
    cantidad_producto = models.IntegerField(name='cantidad_producto')

    def str(self): return str(self.producto)


class Reservacion_Generada(models.Model):
    cliente_auth = models.ForeignKey(User, on_delete=models.CASCADE, name='cliente_auth')
    total_pagar = models.FloatField(max_length=255)
    fecha_reservacion = models.DateField(default=datetime.date.today)
    cliente_entrega = models.CharField(max_length=255)
    telefono_entrega = models.CharField(max_length=255)
    direccion_entrega = models.CharField(max_length=255)
    reservaciones = models.ManyToManyField(Reservacion_Simple)
    estado = models.CharField(max_length=50, default='Pendiente', name='estado')
    fecha_estado = models.DateField(default=datetime.date.today)


class ComentarioEvaluacion(models.Model):
    rating = models.FloatField(null=True, blank=True)
    comentario = models.CharField(max_length=255, null=True, blank=True)
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE, blank=True, null=True)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    fecha_comentario = models.DateField(default=datetime.date.today)

    def __unicode__(self):
        return self.comentario

    @property
    def category_name(self):
        return self.cliente.username


class Evaluacion(models.Model):
    puntuacion = models.FloatField(max_length=255)
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE)


class Tarifa_Entrega(models.Model):
    lugar_destino = models.CharField(max_length=255)
    precio = models.FloatField(max_length=55)
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE, name='negocio')

    def str(self): return str(self.lugar_destino)


class Provincia(models.Model):
    nombre = models.CharField(max_length=255)

    def str(self): return str(self.nombre)


class Municipio(models.Model):
    nombre = models.CharField(max_length=255)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, name='provincia')

    def str(self): return str(self.nombre)


class Oferta_Laboral(models.Model):
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE, name='negocio')
    descripcion = models.CharField(max_length=255)

    def str(self): return str(self.descripcion)
