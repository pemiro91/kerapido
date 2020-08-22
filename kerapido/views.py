from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as do_logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
#
# def principal(request):
#     context = {}
#     return render(request, "master/index.html", context)
from django.utils import timezone

from kerapido.models import User, Negocio, Oferta_Laboral, Categoria_Negocio


# Create your views here.
# def upload_images(request):
#     if request.POST:
#         for file in request.FILES.getlist('images'):
#             instance = Fotos(
#                 title="Pacho",
#                 file=file
#             )
#             instance.save()
#     context = {}
#     return render(request, "control_panel/base.html", context)


def principal(request):
    categories = Categoria_Negocio.objects.all()
    bussiness = Negocio.objects.all()[:6]
    ofertas = Oferta_Laboral.objects.all()
    if request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        send_mail(subject, message, 'habanatrans16@gmail.com', ['pemiro91@gmail.com'], fail_silently=False)
        messages.success(request, 'Su mensaje ha sido enviado satisfactoriamente. Gracias!')
        # return redirect('/')
    context = {'categories': categories, 'bussiness': bussiness, 'ofertas': ofertas}
    return render(request, "index.html", context)


def login_admin(request):
    if request.POST:
        form = AuthenticationForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('panel')
        else:
            messages.warning(request, 'username or password not correct')
            return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, "control_panel/pages/sign-in.html", {'form': form})


def admin_panel(request):
    context = {}
    return render(request, "control_panel/index.html", context)


def logout(request):
    do_logout(request)
    return redirect('login')


def profile(request):
    if request.user.is_authenticated:
        bussiness = Negocio.objects.filter(usuario_negocio=request.user)
        context = {'negocios': bussiness}
        return render(request, "control_panel/pages/perfil.html", context)
    return redirect('login')


def register_business(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        if User.objects.filter(username=username).exists():
            messages.warning(request, 'El nombre de usuario ya existe')
            return redirect('register_business')
        elif password != confirm:
            messages.warning(request, 'Las contraseñas no existen')
            return redirect('register_business')
        else:
            User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                telefono=phone,
                email=email,
                username=username,
                password=password,
                is_afiliado=True,
                is_persona_encargada=False,
                is_administrador=False,
                is_cliente=False,
                is_active=False
            )
            messages.success(request, 'Gracias por registrarse en KeRápido,en menos de 72 horas podra acceder al panel')
            return redirect('login')
    context = {}
    return render(request, "control_panel/pages/sign-up.html", context)


def detalles_oferta(request, id_oferta):
    oferta = get_object_or_404(Oferta_Laboral, pk=id_oferta)
    context = {'oferta': oferta}
    return render(request, "oferta_detalles.html", context)


def ofertas_laborales(request):
    ofertas = Oferta_Laboral.objects.all()
    context = {'ofertas': ofertas}
    return render(request, "ofertas.html", context)


def servicios(request):
    context = {}
    return render(request, "control_panel/pages/listado_categorias.html", context)


def reservations(request):
    context = {}
    return render(request, "control_panel/pages/listado_reservaciones.html", context)


def nuestros_afiliados(request):
    context = {}
    return render(request, "nuestros_afiliados.html", context)


def users(request):
    if request.user.is_authenticated:
        usuarios = User.objects.all()
        context = {'usuarios': usuarios}
        return render(request, "control_panel/pages/listado_usuarios.html", context)
    return redirect('login')


def activate_user(request, id_user):
    if request.user.is_authenticated:
        User.objects.filter(pk=id_user).update(is_active=True, fecha_alta=datetime.now())
        return redirect('users')
    return redirect('login')


def blocked_user(request, id_user):
    if request.user.is_authenticated:
        User.objects.filter(pk=id_user).update(is_active=False, fecha_alta=datetime.now())
        return redirect('users')
    return redirect('login')


def delete_user(request, id_user):
    if request.user.is_authenticated:
        p = User.objects.get(id=id_user)
        p.delete()
        return redirect('users')
    return redirect('login')


# ----------UI-----------#
def terminos_servicio(request):
    context = {}
    return render(request, "terminos_servicio.html", context)


def menu(request):
    context = {}
    return render(request, "control_panel/pages/menu.html", context)


def negocios(request):
    context = {}
    return render(request, "control_panel/pages/listado_negocios.html", context)


def modals(request):
    context = {}
    return render(request, "control_panel/pages/UI/modals.html", context)


def sliders(request):
    context = {}
    return render(request, "control_panel/pages/UI/sliders.html", context)


def error404(request):
    context = {}
    return render(request, "control_panel/pages/404.html", context)


def terminos_condiciones(request):
    context = {}
    return render(request, "control_panel/pages/terminos_condiicones.html", context)
