from django.shortcuts import render, redirect
from kerapido.models import Plato
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as do_logout


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


def login_negocio(request):
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
    return render(request, "control_panel/pages/examples/sign-in.html", {'form': form})


def admin_panel(request):
    context = {}
    return render(request, "control_panel/index.html", context)


def logout(request):
    do_logout(request)
    return redirect('/')


def profile(request):
    context = {}
    return render(request, "control_panel/pages/examples/profile.html", context)


# def register_business(request):
#     context = {}
#     return render(request, "control_panel/pages/examples/sign-up.html", context)


def admin_panel_v2(request):
    context = {}
    return render(request, "control_panel/index2.html", context)


def form_general(request):
    context = {}
    return render(request, "control_panel/pages/forms/general.html", context)


def form_editors(request):
    context = {}
    return render(request, "control_panel/pages/forms/editors.html", context)


def form_advanced(request):
    context = {}
    return render(request, "control_panel/pages/forms/form-wizard.html", context)


def table_simple(request):
    context = {}
    return render(request, "control_panel/pages/tables/simple.html", context)


def table_advanced(request):
    context = {}
    return render(request, "control_panel/pages/tables/data.html", context)


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


def timeline(request):
    context = {}
    return render(request, "control_panel/pages/UI/timeline.html", context)

def register_business(request):
    context = {}
    return render(request, "control_panel/pages/examples/sign-up.html", context)