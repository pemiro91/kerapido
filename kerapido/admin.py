from django.contrib import admin

# Register your models here.
from kerapido.models import Plato, User, Reservacion_Simple

admin.site.register(User)
admin.site.register(Plato)
admin.site.register(Reservacion_Simple)
