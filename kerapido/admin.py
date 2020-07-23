from django.contrib import admin

# Register your models here.
from kerapido.models import Plato, User, Reservacion_Simple, Agrego, Tarifa

admin.site.register(User)
admin.site.register(Plato)
admin.site.register(Agrego)
admin.site.register(Tarifa)
admin.site.register(Reservacion_Simple)
