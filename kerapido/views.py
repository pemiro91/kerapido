from django.shortcuts import render, redirect
from kerapido.models import Plato
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as do_logout
from django.conf.urls import handler404

# Create your views here.

def upload_images(request):
    if request.POST:
        for file in request.FILES.getlist('images'):
            instance = Fotos(
                title="Pacho",
                file=file
            )
            instance.save()
    context = {}
    return render(request, "control_panel/base.html", context)

#
# def principal(request):
#     context = {}
#     return render(request, "master/index.html", context)

def principal(request):
    context = {}
    return render(request, "index.html", context)

def login(request):
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
    return redirect('/')


def profile(request):
    context = {}
    return render(request, "control_panel/pages/mi_negocio.html", context)


# def register_business(request):
#     context = {}
#     return render(request, "control_panel/pages/examples/sign-up.html", context)


def admin_panel_v2(request):
    context = {}
    return render(request, "control_panel/index2.html", context)


def menu(request):
    context = {}
    return render(request, "control_panel/pages/menu.html", context)


def categories(request):
    context = {}
    return render(request, "control_panel/pages/listado_categorias.html", context)


def reservations(request):
    context = {}
    return render(request, "control_panel/pages/listado_reservaciones.html", context)


def table_simple(request):
    context = {}
    return render(request, "control_panel/pages/tables/simple.html", context)


def users(request):
    context = {}
    return render(request, "control_panel/pages/listado_usuarios.html", context)


# ----------UI-----------#
def buttons(request):
    context = {}
    return render(request, "control_panel/pages/UI/buttons.html", context)


def general(request):
    context = {}
    return render(request, "control_panel/pages/UI/general.html", context)


def icon(request):
    context = {}
    return render(request, "control_panel/pages/UI/icons.html", context)


def modals(request):
    context = {}
    return render(request, "control_panel/pages/UI/modals.html", context)


def sliders(request):
    context = {}
    return render(request, "control_panel/pages/UI/sliders.html", context)


def error404(request):
    context = {}
    return render(request, "control_panel/pages/404.html", context)

def register_business(request):
    context = {}
    return render(request, "control_panel/pages/sign-up.html", context)

def terminos_condiciones(request):
    context = {}
    return render(request, "control_panel/pages/terminos_condiicones.html", context)