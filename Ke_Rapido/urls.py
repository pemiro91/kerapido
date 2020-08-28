"""Ke_Rapido URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns

from kerapido import views
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf.urls import handler404

from kerapido.api import *

urlpatterns = [
    # ------------- Landing Page -------------#
    path('', views.principal, name="index"),
    path('ofertas', views.ofertas_laborales, name="ofertas"),
    path('ofertas/<int:id_oferta>', views.detalles_oferta, name="detalles_oferta"),

    # ------------- Panel Control -------------#
    path('admin/', admin.site.urls),
    path('user', views.login_admin, name="login"),
    path('logout', views.logout, name="logout"),
    path('profile', views.profile, name="my_profile"),
    path('register_business', views.register_business, name="register_business"),
    path('panel', views.admin_panel, name="panel"),
    path('services', views.servicios, name="services"),
    path('add_services', views.add_services, name="add_services"),
    path('reservations', views.reservations, name="reservations"),
    path('nuestros_afiliados', views.nuestros_afiliados, name="nuestros_afiliados"),
    path('users', views.users, name="users"),
    path('activate_user/<int:id_user>', views.activate_user, name="activate_user"),
    path('blocked_user/<int:id_user>', views.blocked_user, name="blocked_user"),
    path('update_user/<int:id_user>', views.update_user, name="update_user"),
    path('delete_user/<int:id_user>', views.delete_user, name="delete_user"),
    path('terminos', views.terminos_servicio, name="terminos_servicio"),
    path('table', views.menu, name="table"),
    path('bussiness', views.negocios, name="bussiness"),
    path('add_bussiness', views.add_bussiness, name="add_bussiness"),
    path('update_bussiness', views.update_bussiness, name="update_bussiness"),
    path('terminos_condiciones', views.terminos_condiciones, name="terminos_condiciones"),

    # ------------- Api -------------#
    path('api/account/register', UserCreate.as_view()),
    path('api/login', login),
    path('api-auth/', include('rest_framework.urls')),
    path('api/negocios/', getNegociosApi),
    path('api/productos/<int:pk>/', getProductoApi),
    path('api/servicio/<int:pk>/', getServicioApiForID),
    path('api/reservar/', postReservaApi),
    path('api/reservas/<int:pk>/', getReservasApiForID),
    path('api/tarifas/<int:pk>/', getTarifaEntregaApiForID),
    path('api/comment/<int:pk>/', postComentarioApi),
    path('api/comments/<int:pk>/', getComentarioApi),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
