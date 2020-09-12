import datetime
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from stdimage import StdImageField

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
    descripcion = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Macro(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Categoria_Negocio(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    macro = models.ForeignKey(Macro, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Provincia(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Municipio(models.Model):
    nombre = models.CharField(max_length=255)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, name='provincia')

    def __str__(self):
        return self.nombre


class Frecuencia(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Negocio(models.Model):
    usuario_negocio = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    macro = models.ManyToManyField(Macro)
    nombre = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logo/', null=True, blank=True)
    portada = StdImageField(upload_to='portada/', variations={'thumbnail': (550, 412)}, null=True, blank=True)
    eslogan = models.CharField(max_length=255, null=True, blank=True)
    categorias = models.ManyToManyField(Categoria_Negocio)
    servicios = models.ManyToManyField(Servicio)
    horario = models.CharField(max_length=255, null=True, blank=True)
    frecuencia = models.ManyToManyField(Frecuencia)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    # provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True)
    municipio = models.CharField(max_length=255, null=True, blank=True)
    telefono1 = models.CharField(max_length=255, null=True, blank=True)
    telefono2 = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.nombre


class Categoria_Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    imagen = models.ImageField(upload_to='imagen_plato/', null=True, blank=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    precio = models.FloatField(max_length=255)
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria_Producto, related_name='categorias_ordered', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Tarifa_Entrega(models.Model):
    lugar_destino = models.CharField(max_length=255)
    precio = models.FloatField(max_length=55)
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE, name='negocio')

    def __str__(self):
        return self.lugar_destino


class Reservacion_Simple(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, name='plato')
    cantidad_producto = models.IntegerField()

    def str(self): return str(self.producto)


class Pedido(models.Model):
    cliente_auth = models.ForeignKey(User, on_delete=models.CASCADE, name='cliente_auth')
    total_pagar = models.FloatField(max_length=255)
    fecha_reservacion = models.DateTimeField(auto_now_add=True)
    cliente_entrega = models.CharField(max_length=255)
    telefono_entrega = models.CharField(max_length=255)
    direccion_entrega = models.CharField(max_length=255)
    reservaciones = models.ManyToManyField(Reservacion_Simple)
    estado = models.CharField(max_length=50, default='Pendiente', name='estado')
    fecha_estado = models.DateField(default=datetime.date.today)
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE)
    porciento_pagar = models.FloatField(max_length=255)
    tarifa = models.ForeignKey(Tarifa_Entrega, on_delete=models.CASCADE, name='tarifa', null=True, blank=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, null=True, blank=True)
    total_pagar_user = models.FloatField(max_length=255, null=True, blank=True)


class ComentarioEvaluacion(models.Model):
    rating = models.FloatField(null=True, blank=True)
    comentario = models.CharField(max_length=255, null=True, blank=True)
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE, blank=True, null=True)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    fecha_comentario = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.comentario

    @property
    def category_name(self):
        return self.cliente.username


class Evaluacion(models.Model):
    puntuacion = models.FloatField(max_length=255)
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE)


class Oferta_Laboral(models.Model):
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE, name='negocio')
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return self.descripcion
