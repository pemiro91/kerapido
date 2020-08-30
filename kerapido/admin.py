from django.contrib import admin

# Register your models here.
from kerapido.models import Producto, User, Reservacion_Simple, Categoria_Producto, Servicio, Tarifa_Entrega, \
    Oferta_Laboral, Negocio, Categoria_Negocio

admin.site.register(User)
admin.site.register(Producto)
admin.site.register(Categoria_Producto)
admin.site.register(Servicio)
admin.site.register(Tarifa_Entrega)
admin.site.register(Oferta_Laboral)
admin.site.register(Reservacion_Simple)
admin.site.register(Negocio)
admin.site.register(Categoria_Negocio)
