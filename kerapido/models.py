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


class Negocio(AbstractUser):
    logo = models.ImageField(upload_to='logo/%Y/%m/%d', null=True, blank=True)
    persona_encargada = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    especialidad = models.CharField(max_length=255)
    provincia = models.CharField(max_length=255)
    municipio = models.CharField(max_length=255)
    localidad = models.CharField(max_length=255)
    rating = models.FloatField(max_length=20)


class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    tipo_producto = models.CharField(max_length=255)
    agregos = models.CharField(max_length=255)
    precio = models.FloatField(max_length=50)
    negocio = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, name='negocio')

    def __str__(self):
        return self.nombre


class Fotos(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, name='producto', related_name='photos')
    file = models.FileField(upload_to='photos/%Y/%m/%d', validators=[validate_file_extension])
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Reservation(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, name='producto')
    cantidad_producto = models.IntegerField(name='cantidad_producto')
    fecha_reservacion = models.DateField(default=datetime.datetime.now, name='fecha_reservacion')


class Estado_Reservation(models.Model):
    reservacion = models.ForeignKey(Reservation, on_delete=models.CASCADE, name='reservacion')
    estado = models.CharField(max_length=50, choices=ESTADO_ENTREGA, name='estado')
    fecha_estado = models.DateField()
    negocio = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, name='negocio')

    def __str__(self): return str(self.reservacion)
