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
from kerapido import views
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.principal, name="index"),
    path('user', views.login_admin, name="login"),
    path('logout', views.logout, name="logout"),
    path('profile', views.profile, name="my_business"),
    path('register_business', views.register_business, name="register_business"),

    path('upload_images', views.upload_images, name='base'),
    path('panel', views.admin_panel, name="panel"),
    path('ofertas', views.ofertas_laborales, name="ofertas"),
    path('oferta/<int:id_negocio>', views.detalles_oferta, name="detalles_oferta"),
    path('categories', views.categories, name="categories"),
    path('reservations', views.reservations, name="reservations"),
    path('nuestros_afiliados', views.nuestros_afiliados, name="nuestros_afiliados"),
    path('users', views.users, name="users"),
    path('terminos', views.terminos_servicio, name="terminos_servicio"),
    path('general', views.general, name="general"),
    path('icon', views.icon, name="icon"),
    path('modals', views.modals, name="modals"),
    path('sliders', views.sliders, name="sliders"),
    # path('timeline', views.timeline, name="timeline"),

    path('terminos_condiciones', views.terminos_condiciones, name="terminos_condiciones"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = 'views.error404'