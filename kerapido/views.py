from django.shortcuts import render, redirect
from kerapido.models import Fotos
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login


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
    return render(request, "base.html", context)


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
    return render(request, "control_panel/pages/examples/login.html", {'form': form})


def register_member(request):
    context = {}
    return render(request, "control_panel/pages/examples/register.html", context)


def admin_panel(request):
    context = {}
    return render(request, "control_panel/index_panel.html", context)


def form_general(request):
    context = {}
    return render(request, "control_panel/pages/forms/general.html", context)


def form_editors(request):
    context = {}
    return render(request, "control_panel/pages/forms/editors.html", context)


def form_advanced(request):
    context = {}
    return render(request, "control_panel/pages/forms/advanced.html", context)
