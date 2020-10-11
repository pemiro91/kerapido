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
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from kerapido import views
from kerapido import views as myapp_views
from kerapido.api import *
from django.conf.urls import handler404, handler500

urlpatterns = [
    # ------------- Landing Page -------------#
    path('', views.principal, name="index"),
    path('ofertas', views.ofertas_laborales, name="ofertas"),
    path('ofertas/<int:id_oferta>', views.detalles_oferta, name="detalles_oferta"),
    path('nuestros_afiliados', views.nuestros_afiliados, name="nuestros_afiliados"),
    path('nuestros_afiliados/<int:id_afiliado>', views.nuestros_afiliados_detalles, name="detalles_afiliado"),
    path('terminos', views.terminos_servicio, name="terminos_servicio"),
    path('terminos_condiciones', views.terminos_condiciones, name="terminos_condiciones"),

    # ------------- Panel Control -------------#
    path('admin/', admin.site.urls),
    path('user', views.login_admin, name="login"),
    path('logout', views.logout, name="logout"),
    path('profile', views.profile, name="my_profile"),
    path('register_affiliate', views.register_affiliate, name="register_affiliate"),
    path('panel', views.admin_panel, name="panel"),

    path('services', views.services, name="services"),
    path('add_services', views.add_services, name="add_services"),
    path('update_service/<int:id_service>', views.update_service, name="update_service"),
    path('delete_service/<int:id_service>', views.delete_service, name="delete_service"),

    path('reservations/<int:id_bussiness>', views.reservations, name="reservations"),
    path('reservations/change_state_reservation/<int:id_bussiness>/<int:id_reservation>',
         views.change_state_reservation, name="change_state_reservation"),
    path('factura/<int:id_pedido>', views.factura, name="factura"),
    path('reservations_admin', views.reservations_admin, name="reservations_admin"),

    path('users', views.users, name="users"),
    path('activate_user/<int:id_user>', views.activate_user, name="activate_user"),
    path('blocked_user/<int:id_user>', views.blocked_user, name="blocked_user"),
    path('update_user/<int:id_user>', views.update_user, name="update_user"),
    path('delete_user/<int:id_user>', views.delete_user, name="delete_user"),
    path('add_person/', views.add_person, name="add_person_of_business"),
    path('update_person/<int:id_user>', views.update_person, name="update_person"),
    path('rol_admin/<int:id_user>', views.rol_admin, name="rol_admin"),
    path('users_rol/<int:id_rol>', views.users_rol, name="users_rol"),

    path('products/<int:id_bussiness>', views.products, name="products"),
    path('add_product/<int:id_bussiness>', views.add_product, name="add_product"),
    path('edit_product/<int:id_bussiness>/<int:id_product>', views.editar_product, name="edit_product"),
    path('delete_product/<int:id_product>', views.delete_product, name="delete_product"),

    path('category_products/<int:id_bussiness>', views.categoria_productos, name="category_products"),
    path('add_category_product/<int:id_bussiness>', views.agregar_categoria_productos, name="add_category_product"),
    path('edit_category_product/<int:id_bussiness>/<int:id_category>', views.editar_categoria_producto,
         name="edit_category_product"),
    path('delete_category/<int:id_category>', views.delete_categoria, name="delete_category"),

    path('offers/<int:id_bussiness>', views.offers, name="offers"),
    path('add_offer/<int:id_bussiness>', views.add_offer, name="add_offer"),
    path('update_offer/<int:id_bussiness>/<int:id_offer>', views.update_offer, name="update_offer"),
    path('delete_offer/<int:id_offer>', views.delete_offer, name="delete_offer"),

    path('rates/<int:id_bussiness>', views.rates, name="rates"),
    path('add_rate/<int:id_bussiness>', views.add_rate, name="add_rate"),
    path('update_rate/<int:id_bussiness>/<int:id_rate>', views.update_rate, name="update_rate"),
    path('delete_rate/<int:id_rate>', views.delete_rate, name="delete_rate"),

    path('bussiness', views.businesses, name="bussiness"),
    path('my_bussiness/<int:id_bussiness>', views.my_bussiness, name="my_bussiness"),
    path('add_bussiness', views.add_bussiness, name="add_bussiness"),
    path('update_bussiness/<int:id_bussiness>', views.update_bussiness, name="update_bussiness"),
    path('delete_bussiness/<int:id_rate>', views.delete_bussiness, name="delete_bussiness"),
    path('factura_bussiness/<int:id_bussiness>', views.factura_bussiness, name="factura_bussiness"),
    path('activate_business/<int:id_bussiness>', views.activate_business, name="activate_business"),
    path('blocked_business/<int:id_bussiness>', views.blocked_business, name="blocked_business"),

    path('categories', views.categories, name="categories"),
    path('add_category', views.add_category, name="add_category"),
    path('update_category/<int:id_category>', views.update_category, name="update_category"),
    path('delete_category/<int:id_category>', views.delete_category, name="delete_category"),

    # ------------- Notifications -------------#
    path('notifications_center', views.messages_center, name="notifications_center"),
    path('delete_notification/<int:id_message>', views.delete_message, name="delete_notification"),
    path('mark_read/<int:id_message>', views.mask_as_read, name="mark_as_read"),
    path('mark_no_read/<int:id_message>', views.mask_as_no_read, name="mark_as_no_ead"),

    # ------------- Api -------------#
    path('api/account/register', UserCreate.as_view()),
    path('api/login', login),
    path('api-auth/', include('rest_framework.urls')),
    path('api/negocios/', getNegociosApi),
    path('api/negocios/<int:pk>/', getNegocioApi),
    path('api/productos/<int:pk>/', getProductoApi),
    path('api/servicio/<int:pk>/', getServicioApiForID),
    path('api/reservar/', postReservaApi),
    path('api/reservas/<int:pk>/', getReservasApiForID),
    path('api/tarifas/<int:pk>/', getTarifaEntregaApiForID),
    path('api/comment/<int:id_negocio>/', postComentarioApi),
    path('api/comments/<int:pk>/', getComentarioApi),
]

handler404 = myapp_views.error_404_view
handler500 = myapp_views.error_500_view

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
