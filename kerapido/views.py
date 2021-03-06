from datetime import datetime, date, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as do_logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.db.models import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from kerapido.forms import MyForm, UpdateBusiness
from kerapido.models import User, Negocio, Oferta_Laboral, Categoria_Negocio, Municipio, Frecuencia, \
    Servicio, Macro, Categoria_Producto, Producto, ComentarioEvaluacion, Pedido, Tarifa_Entrega, PerfilPersonaEncargada, \
    PerfilAfiliado, Notification, Factura_KeRapido


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

# ----------UI-----------#
def principal(request):
    macro_categorias = Macro.objects.all()
    bussiness = Negocio.objects.all()[:6]
    ofertas = Oferta_Laboral.objects.all()
    productos = Producto.objects.all()
    if request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        send_mail(subject, message, email, ['info@kerapido.net'], fail_silently=False)
        messages.success(request, 'Su mensaje ha sido enviado satisfactoriamente. Gracias!')
        return redirect('/')
    context = {'macro_categorias': macro_categorias, 'bussiness': bussiness, 'ofertas': ofertas,
               'prodductos': productos}
    return render(request, "index.html", context)


def terminos_servicio(request):
    context = {}
    return render(request, "terminos_servicio.html", context)


def error404(request):
    context = {}
    return render(request, "control_panel/pages/404.html", context)


def terminos_condiciones(request):
    context = {}
    return render(request, "control_panel/pages/terminos_condiicones.html", context)


def detalles_oferta(request, id_oferta):
    oferta = get_object_or_404(Oferta_Laboral, pk=id_oferta)
    context = {'oferta': oferta}
    return render(request, "oferta_detalles.html", context)


def ofertas_laborales(request):
    ofertas = Oferta_Laboral.objects.all()
    context = {'ofertas': ofertas}
    return render(request, "ofertas.html", context)


def nuestros_afiliados(request):
    negocios_afiliados = Negocio.objects.filter(is_closed=False)
    paginator = Paginator(negocios_afiliados, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'negocios_afiliados': page_obj}
    return render(request, "nuestros_afiliados.html", context)


def nuestros_afiliados_detalles(request, id_afiliado):
    negocio_afiliado = get_object_or_404(Negocio, pk=id_afiliado)
    context = {'negocio_afiliado': negocio_afiliado}
    return render(request, "nuestros_afiliados_detalles.html", context)


def error_404_view(request, exception):
    return render(request, 'control_panel/pages/404.html', status=404)


def error_500_view(request):
    return render(request, 'control_panel/pages/500.html', status=500)


# --------------Panel de control----------------#
# ----------------------------------------------#

def register_affiliate(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')
        terms = request.POST.get('terminos', 'off')

        print(terms)

        if User.objects.filter(telefono__icontains=phone).exists():
            messages.warning(request, 'El teléfono ya existe')
            return redirect('register_affiliate')
        elif User.objects.filter(email=email).exists():
            messages.warning(request, 'El correo ya existe')
            return redirect('register_affiliate')
        elif User.objects.filter(username=username).exists():
            messages.warning(request, 'El nombre de usuario ya existe')
            return redirect('register_affiliate')
        elif password != confirm:
            messages.warning(request, 'Las contraseñas no existen')
            return redirect('register_affiliate')
        elif terms == u'off':
            messages.warning(request, 'Debe aceptar los términos y condiciones')
            return redirect('register_affiliate')
        else:
            with transaction.atomic():
                user = User.objects.create_user(
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
                PerfilAfiliado.objects.create(afiliado_id=user.pk)
                mensaje_notificacion = user.first_name + ' se registró como AFILIADO.'
                if mensaje_notificacion != '':
                    notificacion = Notification(mensaje=mensaje_notificacion,
                                                estado='No-Leida', tipo='Usuario')
                    notificacion.save()
                messages.success(request, 'Gracias por registrarse en KeRápido,en menos de 72 horas podra acceder al '
                                          'panel')
                return redirect('login')
    context = {}
    return render(request, "control_panel/pages/registrar.html", context)


def base(request):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
        business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        services = Servicio.objects.all()
        context = {'business': business, 'services': services, 'business_persona': business_persona}
        return render(request, "control_panel/base.html", context)
    return redirect('login')


def admin_panel(request):
    if request.user.is_authenticated:
        notificaciones = []
        cant_notificaciones = 0
        business = Negocio.objects.filter(usuario_negocio=request.user)
        services = Servicio.objects.all()
        cant_pedidos = len(Pedido.objects.all())
        cant_afiliados = len(User.objects.filter(is_afiliado=True))
        cant_negocios = len(Negocio.objects.all())
        cant_clientes = len(User.objects.filter(is_cliente=True))
        cant_servicios = len(services)
        cant_personal_encargado = len(User.objects.filter(is_persona_encargada=True))
        cant_categ_neg = len(Categoria_Negocio.objects.all())
        today = date.today()
        ayer = today - timedelta(days=1)
        ultima_semana = today - timedelta(days=7)
        mes_anterior = today.month - 1
        anno_anterior = today.year - 1
        pedidos_general = []
        comision_hoy_general = 0
        comision_ayer_general = 0
        comision_ultima_semana_general = 0
        comision_ultimo_mes_general = 0
        comision_anno_general = 0
        comision_general = 0
        business_persona = QuerySet
        persona_encargada = QuerySet
        ultimos_pedidos = []

        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)

        if request.user.is_superuser:
            pedidos_general = Pedido.objects.all()
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            notificaciones = list(notificaciones)
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            pedidos_general = Pedido.objects.all()
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            pedidos_general = Pedido.objects.filter(negocio_id=persona_encargada.negocio_pertenece.id)
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        if request.user.is_superuser or request.user.is_administrador:
            pedidos_general = Pedido.objects.all()
            ultimos_pedidos = pedidos_general.order_by('-fecha_reservacion')[:5]
        elif request.user.is_persona_encargada:
            pedidos_general = Pedido.objects.filter(negocio_id=persona_encargada.negocio_pertenece.id)
            ultimos_pedidos = pedidos_general.order_by('-fecha_reservacion')[:5]
        else:
            pedidos_general = Pedido.objects.filter(negocio__usuario_negocio_id=request.user.id)
            ultimos_pedidos = pedidos_general.order_by('-fecha_reservacion')[:5]

        for ph in pedidos_general:
            fecha = ph.fecha_reservacion
            if fecha == today:
                comision_hoy_general += ph.porciento_pagar
            if fecha == ayer:
                comision_ayer_general += ph.porciento_pagar
            if fecha == ultima_semana:
                comision_ultima_semana_general += ph.porciento_pagar
            if fecha.month == mes_anterior:
                comision_ultimo_mes_general += ph.porciento_pagar
            if fecha.year == anno_anterior:
                comision_anno_general += ph.porciento_pagar
                # print(comision_anno_general)
            else:
                comision_hoy_general += 0
                comision_ayer_general += 0
                comision_ultima_semana_general += 0
                comision_ultimo_mes_general += 0
                comision_anno_general += 0

        for pe in pedidos_general:
            comision_general += pe.porciento_pagar

        context = {'business': business, 'services': services,
                   'notificaciones': notificaciones, 'cant_notificaciones': cant_notificaciones,
                   'cantidad_pedidos': cant_pedidos, 'cantidad_afiliados': cant_afiliados,
                   'cantidad_negocios': cant_negocios, 'cantidad_clientes': cant_clientes,
                   'cantidad_servicios': cant_servicios,
                   'ultimos_pedidos': ultimos_pedidos,
                   'cantidad_encargados': cant_personal_encargado, 'cantidad_categ_neg': cant_categ_neg,
                   'comision_hoy_general': comision_hoy_general, 'comision_ayer_general': comision_ayer_general,
                   'comision_ultima_semana_general': comision_ultima_semana_general,
                   'comision_ultimo_mes_general': comision_ultimo_mes_general,
                   'comision_anno_general': comision_anno_general,
                   'comision_general': comision_general,
                   'business_persona': business_persona,
                   'pedidos': pedidos_general}
        return render(request, "control_panel/index.html", context)
    return redirect('login')


def login_admin(request):
    if request.POST:
        form = AuthenticationForm(request.POST)
        nombreuser = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=nombreuser):
            user_exists = User.objects.get(username=nombreuser)
            if user_exists:
                if not user_exists.is_cliente:
                    if user_exists.is_active:
                        user = authenticate(username=nombreuser, password=password)
                        if user is not None:
                            login(request, user)
                            tiene_negocio = Negocio.objects.filter(usuario_negocio=user)
                            if tiene_negocio or user.is_superuser or user.is_administrador:
                                return redirect('panel')
                            elif user.is_persona_encargada:
                                persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=user)
                                tiene_negocio_persona = Negocio.objects.filter(
                                    pk=persona_encargada.negocio_pertenece.id)
                                if tiene_negocio_persona:
                                    return redirect('panel')
                            else:
                                return redirect('add_bussiness')
                        else:
                            messages.warning(request, 'Error de autenticación')
                            return redirect('login')
                    else:
                        messages.warning(request, 'Usted no tiene acceso al sistema')
                        return redirect('login')
                else:
                    messages.warning(request, 'Usted no tiene acceso al sistema')
                    return redirect('login')
            else:
                messages.warning(request, 'El usuario no exixte')
                return redirect('login')
        else:
            messages.warning(request, 'El usuario no exixte')
            return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, "control_panel/pages/autenticar.html", {'form': form})


def logout(request):
    do_logout(request)
    return redirect('login')


def profile(request):
    if request.user.is_authenticated:
        bussiness = Negocio.objects.filter(usuario_negocio=request.user)
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        business_persona = QuerySet
        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        if request.method == "POST":
            nombre = request.POST.get('first_name')
            apellidos = request.POST.get('last_name')
            telefono = request.POST.get('phone')
            correo = request.POST.get('email')
            usuario = request.POST.get('username')
            User.objects.filter(pk=request.user.id).update(
                first_name=nombre,
                last_name=apellidos,
                email=correo,
                telefono=telefono,
                username=usuario
            )
            messages.success(request, 'Información actualizada correctamente')
            return redirect('login')
        context = {'business': bussiness, 'business_persona': business_persona,
                   'notificaciones': notificaciones, 'cant_notificaciones': cant_notificaciones}
        return render(request, "control_panel/pages/perfil.html", context)
    return redirect('login')


def change_password(request):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        business_persona = QuerySet
        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        if request.method == "POST":
            old_password = request.POST.get('oldPassword')
            new_password = request.POST.get('newPassword')
            confirmed_new_password = request.POST.get('newPasswordConfirm')
            U = User.objects.get(username=request.user.username)
            if not U.check_password(old_password):
                error = "Contraseña Incorrecta."
                return render(request, "control_panel/pages/perfil.html", {'error': error})
            if confirmed_new_password != new_password:
                error = "Las Contraseñas No Coinciden."
                return render(request, "control_panel/pages/perfil.html", {'error': error})
            U.set_password(new_password)
            U.save()
            messages.success(request, 'Se cambió la contraseña satisfactoriamente')
            return redirect('login')
        context = {'business': business, 'business_persona': business_persona, 'notificaciones': notificaciones,
                   'cant_notificaciones': cant_notificaciones}
        return render(request, "control_panel/pages/perfil.html", context)
    return redirect('login')


# -------------------Módulo Servicios---------------#

def services(request):
    if request.user.is_authenticated:
        servicios = Servicio.objects.all()
        business = Negocio.objects.filter(usuario_negocio=request.user)
        business_persona = QuerySet
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        context = {'services': servicios, 'business': business, 'business_persona': business_persona,
                   'notificaciones': notificaciones, 'cant_notificaciones': cant_notificaciones}
        return render(request, "control_panel/module_services/listado_servicios.html", context)
    return redirect('login')


def add_services(request):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        business_persona = QuerySet
        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        if request.method == 'POST':
            name_service = request.POST.get('name_service')
            description_service = request.POST.get('description_service')
            color_service = request.POST.get('color_service')
            Servicio.objects.create(nombre=name_service, descripcion=description_service, color=color_service)
            messages.success(request, 'Servicio agregado correctamente')
            return redirect('services')
        context = {'business': business, 'business_persona': business_persona,
                   'notificaciones': notificaciones, 'cant_notificaciones': cant_notificaciones}
        return render(request, "control_panel/module_services/agregar_servicios.html", context)
    return redirect('login')


def update_service(request, id_service):
    if request.user.is_authenticated:
        service = Servicio.objects.get(id=id_service)
        business = Negocio.objects.filter(usuario_negocio=request.user)
        business_persona = QuerySet
        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        if request.method == 'POST':
            name_service = request.POST.get('name_service')
            description_service = request.POST.get('description_service')
            color_service = request.POST.get('color_service')
            with transaction.atomic():
                Servicio.objects.filter(pk=id_service).update(
                    nombre=name_service,
                    descripcion=description_service,
                    color=color_service
                )
                messages.success(request, 'Servicio actualizado correctamente')
                return redirect('services')
        context = {'service': service, 'business': business, 'business_persona': business_persona,
                   'notificaciones': notificaciones, 'cant_notificaciones': cant_notificaciones}
        return render(request, "control_panel/module_services/editar_servicios.html", context)
    return redirect('login')


def delete_service(request, id_service):
    if request.user.is_authenticated:
        p = Servicio.objects.get(id=id_service)
        p.delete()
        messages.success(request, 'Servicio eliminado correctamente')
        return redirect('services')
    return redirect('login')


# -------------------Módulo Reservaciones---------------#

def reservations(request, id_bussiness):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        business_persona = QuerySet
        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        pedidos = Pedido.objects.filter(negocio=id_bussiness)
        context = {'business': business, 'negocio': negocio, 'pedidos': pedidos, 'business_persona': business_persona,
                   'notificaciones': notificaciones, 'cant_notificaciones': cant_notificaciones}
        return render(request, "control_panel/module_reservation/listado_reservaciones.html", context)
    return redirect('login')


def change_state_reservation(request, id_bussiness, id_reservation):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        business_persona = QuerySet
        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        if request.method == 'POST':
            state = request.POST.get('state')
            Pedido.objects.filter(pk=id_reservation).update(estado=state, fecha_estado=date.today())
            messages.success(request, 'Estado cambiado correctamente')
            return redirect(reverse('reservations', args=(id_bussiness,)))
        context = {'business': business, 'negocio': negocio, 'business_persona': business_persona}
        return render(request, "control_panel/module_reservation/listado_reservaciones.html", context)
    return redirect('login')


def factura(request, id_pedido):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        business_persona = QuerySet
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        pedido = get_object_or_404(Pedido, pk=id_pedido)
        context = {'business': business, 'pedido': pedido, 'business_persona': business_persona,
                   'notificaciones': notificaciones, 'cant_notificaciones': cant_notificaciones}
        return render(request, "control_panel/module_reservation/factura.html", context)
    return redirect('login')


def reservations_admin(request):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        business_persona = QuerySet
        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        pedidos = Pedido.objects.all()
        context = {'business': business, 'pedidos': pedidos, 'business_persona': business_persona,
                   'notificaciones': notificaciones, 'cant_notificaciones': cant_notificaciones}
        return render(request, "control_panel/module_reservation/listado_reservaciones_admin.html", context)
    return redirect('login')


# -------------------Módulo Usuarios---------------#

def users(request):
    if request.user.is_authenticated:
        personas_afiliadas = QuerySet
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        if request.user.is_afiliado:
            perfilAfiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.pk)
            personas_afiliadas = PerfilPersonaEncargada.objects.filter(afiliado_pertenece_id=perfilAfiliado.pk)
        business_persona = QuerySet
        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        usuarios = User.objects.all().exclude(is_superuser=True).exclude(username=request.user.username)
        titulo_table = "LISTADO DE USUARIOS"
        business = Negocio.objects.filter(usuario_negocio=request.user)
        context = {'usuarios': usuarios, 'business': business, 'personas_afiliadas': personas_afiliadas,
                   'business_persona': business_persona, 'notificaciones': notificaciones,
                   'cant_notificaciones': cant_notificaciones, 'titulo_table': titulo_table}
        return render(request, "control_panel/module_users/listado_usuarios.html", context)
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


def update_user(request, id_user):
    if request.user.is_authenticated:
        user_custom = User.objects.get(id=id_user)
        business = Negocio.objects.filter(usuario_negocio=request.user)
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        business_persona = QuerySet
        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            password = request.POST.get('password')
            with transaction.atomic():
                user_custom.set_password(password)
                user_custom.save()
                User.objects.filter(pk=id_user).update(
                    first_name=first_name,
                    last_name=last_name,
                    telefono=phone,
                    email=email
                )
                messages.success(request, 'Usuario modificado correctamente')
                return redirect('users')
        context = {'user': user_custom, 'business': business, 'business_persona': business_persona,
                   'notificaciones': notificaciones, 'cant_notificaciones': cant_notificaciones}
        return render(request, "control_panel/module_users/editar_usuario.html", context)
    return redirect('login')


def delete_user(request, id_user):
    if request.user.is_authenticated:
        p = User.objects.get(id=id_user)
        p.delete()
        messages.success(request, 'Usuario eliminado correctamente')
        return redirect('users')
    return redirect('login')


def add_person(request):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        business_persona = QuerySet
        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            bussiness = request.POST.get('bussiness')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password1')
            confirm = request.POST.get('confirm')

            if User.objects.filter(username=username).exists():
                print("User exist")
                messages.warning(request, 'El nombre de usuario ya existe')
                return redirect('add_person_of_business')
            elif password != confirm:
                print("Error Password")
                messages.warning(request, 'Las contraseñas no coinciden')
                return redirect('add_person_of_business')
            else:
                with transaction.atomic():
                    user = User.objects.create_user(
                        first_name=first_name,
                        last_name=last_name,
                        telefono=phone,
                        email=email,
                        username=username,
                        password=password,
                        is_afiliado=False,
                        is_persona_encargada=True,
                        is_administrador=False,
                        is_cliente=False,
                        is_active=False
                    )
                    PerfilPersonaEncargada.objects.create(
                        persona_encargada_id=user.pk,
                        negocio_pertenece_id=bussiness
                    )
                    messages.success(request, 'Persona encargada agregada correctamente')
                return redirect('users')
        context = {'business': business, 'business_persona': business_persona, 'notificaciones': notificaciones,
                   'cant_notificaciones': cant_notificaciones}
        return render(request, "control_panel/module_users/agregar_persona_encargada.html", context)
    return redirect('login')


def update_person(request, id_user):
    if request.user.is_authenticated:
        user_custom = User.objects.get(id=id_user)
        business = Negocio.objects.filter(usuario_negocio=request.user)
        business_persona = QuerySet
        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            bussiness = request.POST.get('bussiness')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            password = request.POST.get('password')
            with transaction.atomic():
                user_custom.set_password(password)
                user_custom.save()
                User.objects.filter(pk=id_user).update(
                    first_name=first_name,
                    last_name=last_name,
                    telefono=phone,
                    email=email
                )
                PerfilPersonaEncargada.objects.filter(persona_encargada_id=id_user).update(
                    negocio_pertenece_id=bussiness
                )
                messages.success(request, 'Persona encargada modificada correctamente')
                return redirect('users')
        context = {'user': user_custom, 'business': business, 'notificaciones': notificaciones,
                   'cant_notificaciones': cant_notificaciones, 'business_persona': business_persona}
        return render(request, "control_panel/module_users/editar_usuario.html", context)
    return redirect('login')


def rol_admin(request, id_user):
    if request.user.is_authenticated:
        User.objects.filter(pk=id_user).update(is_administrador=True, is_afiliado=False)
        usuario = get_object_or_404(User, pk=id_user)
        mensaje_notificacion = usuario.username + ' ahora está registrado como ADMINISTRADOR.'
        if mensaje_notificacion != '':
            notificacion = Notification(mensaje=mensaje_notificacion, negocio=None, usuario=request.user,
                                        estado='No-Leida', tipo='Usuario')
            notificacion.save()
        messages.success(request, 'El rol de administrador fue asignado satisfactoriamente al usuario seleccioando')
        return redirect('users')
    return redirect('login')


def users_rol(request, id_rol):
    if request.user.is_authenticated:
        personas_afiliadas = QuerySet
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        if request.user.is_afiliado:
            perfilAfiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.pk)
            personas_afiliadas = PerfilPersonaEncargada.objects.filter(afiliado_pertenece_id=perfilAfiliado.pk)
        business_persona = QuerySet
        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        business = Negocio.objects.filter(usuario_negocio=request.user)

        if id_rol == 1:
            titulo_table = "LISTADO DE AFILIADOS"
            users_for_rol = User.objects.filter(is_afiliado=True).exclude(is_superuser=True).exclude(
                username=request.user.username)
        elif id_rol == 2:
            titulo_table = "LISTADO DE CLIENTES"
            users_for_rol = User.objects.filter(is_cliente=True).exclude(is_superuser=True).exclude(
                username=request.user.username)
        elif id_rol == 3:
            titulo_table = "LISTADO DE PERSONAS ENCARGADAS"
            users_for_rol = User.objects.filter(is_persona_encargada=True).exclude(is_superuser=True).exclude(
                username=request.user.username)
        else:
            titulo_table = "LISTADO DE USUARIOS"
            users_for_rol = User.objects.all().exclude(is_superuser=True).exclude(username=request.user.username)
        context = {'usuarios': users_for_rol, 'business': business, 'personas_afiliadas': personas_afiliadas,
                   'business_persona': business_persona, 'notificaciones': notificaciones,
                   'cant_notificaciones': cant_notificaciones, 'id_rol': id_rol, 'titulo_table': titulo_table}
        return render(request, "control_panel/module_users/listado_usuarios.html", context)
    return redirect('login')


# -------------------Módulo Categoria Negocio---------------#

def categories(request):
    if request.user.is_authenticated:
        category = Categoria_Negocio.objects.all()
        business = Negocio.objects.filter(usuario_negocio=request.user)
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        context = {'categories': category, 'business': business, 'notificaciones': notificaciones,
                   'cant_notificaciones': cant_notificaciones}
        return render(request,
                      "control_panel/module_category_businesses/listado_categoria.html", context)
    return redirect('login')


def add_category(request):
    if request.user.is_authenticated:
        macro = Macro.objects.all()
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        if request.method == 'POST':
            name_category = request.POST.get('name_category')
            description_category = request.POST.get('description_category')
            macro_field = request.POST.get('macro')
            Categoria_Negocio.objects.create(nombre=name_category, descripcion=description_category,
                                             macro_id=macro_field)
            return redirect('categories')
        context = {'macros': macro, 'notificaciones': notificaciones, 'cant_notificaciones': cant_notificaciones}
        return render(request,
                      "control_panel/module_category_businesses/agregar_categoria_negocio.html", context)
    return redirect('login')


def update_category(request, id_category):
    if request.user.is_authenticated:
        category = Categoria_Negocio.objects.get(id=id_category)
        macro = Macro.objects.all()
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        if request.method == 'POST':
            name_category = request.POST.get('name_category')
            description_category = request.POST.get('description_category')
            macro_field = request.POST.get('macro')
            Categoria_Negocio.objects.filter(id=id_category).update(
                nombre=name_category,
                descripcion=description_category,
                macro_id=macro_field
            )
            return redirect('categories')
        context = {'category': category, 'notifcaciones': notificaciones, 'cant_notificaciones': cant_notificaciones}
        return render(request,
                      "control_panel/module_category_businesses/editar_categoria.html", context)
    return redirect('login')


def delete_category(request, id_category):
    if request.user.is_authenticated:
        p = Categoria_Negocio.objects.get(id=id_category)
        p.delete()
        return redirect('categories')
    return redirect('login')


# -------------------Módulo Negocio---------------#

def businesses(request):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocios = Negocio.objects.all()
        Pedido.objects.filter()

        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        context = {'negocios': negocios, 'business': business, 'notificaciones': notificaciones,
                   'cant_notificaciones': cant_notificaciones}
        return render(request, "control_panel/module_businesses/listado_negocios.html", context)
    return redirect('login')


def add_bussiness(request):
    if request.user.is_authenticated:
        municipios = Municipio.objects.all()
        frecuencia = Frecuencia.objects.all()
        servicios_mostrar = Servicio.objects.all()
        categorias = Categoria_Negocio.objects.all()
        macro = Macro.objects.all()
        macro_negocio = []
        fecha = datetime.now()
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = PerfilAfiliado.objects.get(id=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        if request.method == 'POST':
            name_bussiness = request.POST.get('name_bussiness')
            logo_bussiness = request.FILES['logo_bussiness']
            portada_bussiness = request.FILES['portada_bussiness']
            slogan_bussiness = request.POST.get('slogan_bussiness')
            category_bussiness = request.POST.getlist('category_bussiness')
            services_bussiness = request.POST.getlist('services_bussiness')
            hour_init = request.POST.get('hour_init_bussiness')
            hour_end = request.POST.get('hour_end_bussiness')
            post_frecuencia = request.POST.getlist('frecuencia_bussiness')
            address_bussiness = request.POST.get('address_bussiness')
            municipio = request.POST.get('municipio_bussiness')
            phone_bussiness_o = request.POST.get('phone_bussiness_o')
            phone_bussiness = request.POST.get('phone_bussiness')
            email_bussiness = request.POST.get('email_bussiness')

            horario = str(hour_init) + ' - ' + str(hour_end)

            negocio = Negocio.objects.create(
                is_closed=False,
                usuario_negocio=request.user,
                nombre=name_bussiness,
                logo=logo_bussiness,
                portada=portada_bussiness,
                eslogan=slogan_bussiness,
                horario=horario,
                direccion=address_bussiness,
                municipio_id=municipio,
                telefono1=phone_bussiness_o,
                telefono2=phone_bussiness,
                email=email_bussiness,
            )
            for category in category_bussiness:
                categoria = Categoria_Negocio.objects.get(nombre=category)
                negocio.categorias.add(categoria)
                macro_negocio.append(categoria.macro)

            for service in services_bussiness:
                servicio = Servicio.objects.get(nombre=service)
                negocio.servicios.add(servicio)

            for frecu in post_frecuencia:
                frecuen = Frecuencia.objects.get(nombre=frecu)
                negocio.frecuencia.add(frecuen)

            macro_negocio = list(set(macro_negocio))

            for m in macro_negocio:
                macro1 = Macro.objects.get(nombre=m)
                negocio.macro.add(macro1)

            mensaje_notificacion = 'Se agregó un nuevo negocio con el nombre: ' + negocio.nombre
            if mensaje_notificacion != '':
                notificacion = Notification(mensaje=mensaje_notificacion, negocio=negocio,
                                            estado='No-Leida', tipo='Negocio')
                notificacion.save()
            messages.success(request, 'El negocio se agregó satisfactoriamente')

            return redirect(reverse('my_bussiness', args=(negocio.id,)))

        context = {'municipios': municipios, 'frecuencia': frecuencia, 'servicios_mostrar': servicios_mostrar,
                   'categorias': categorias, 'macros': macro, 'macro_negocio': macro_negocio, 'fecha_ahora': fecha,
                   'notificaciones': notificaciones, 'cant_notificaciones': cant_notificaciones}
        return render(request, "control_panel/module_businesses/agregar_negocio.html", context)
    return redirect('login')


def editar_negocio(request, id_bussiness):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        update_form = UpdateBusiness(request.POST or None, request.FILES or None, instance=negocio)
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        if update_form.is_valid():
            edit = update_form.save(commit=False)
            edit.save()
            return redirect('panel')
        context = {'business': business, 'negocio': negocio, 'update_form': update_form,
                   'notificaciones': notificaciones, 'cant_notificaciones': cant_notificaciones}
        return render(request, "control_panel/module_businesses/update_negocio.html", context)
    return redirect('login')


def update_bussiness(request, id_bussiness):
    if request.user.is_authenticated:
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        servicios = Servicio.objects.all()
        servicios_marcados = list(negocio.servicios.all())
        categorias_marcadas = list(negocio.categorias.all())
        frecuencias_marcadas = list(negocio.frecuencia.all())
        categorias = Categoria_Negocio.objects.all()
        frecuencias = Frecuencia.objects.all()
        macro = Macro.objects.all()
        servicios_no_marcados = []
        categoria_no_marcados = []
        frecuencia_no_marcados = []
        hr_init = negocio.horario.split('-')[0]
        hr_end = negocio.horario.split('-')[1]
        lunes = False
        martes = False
        miercoles = False
        jueves = False
        viernes = False
        sabado = False
        domingo = False
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        for i in servicios:
            if (i not in servicios_no_marcados) and (i not in servicios_marcados):
                servicios_no_marcados.append(i)

        for i in categorias:
            if (i not in categoria_no_marcados) and (i not in categorias_marcadas):
                categoria_no_marcados.append(i)

        for i in frecuencias:
            if (i not in frecuencia_no_marcados) and (i not in frecuencias_marcadas):
                frecuencia_no_marcados.append(i)

        for neg in negocio.frecuencia.all():
            if neg.nombre == 'Lunes':
                lunes = True
            if neg.nombre == 'Martes':
                martes = True
            if neg.nombre == 'Miércoles':
                miercoles = True
            if neg.nombre == 'Jueves':
                jueves = True
            if neg.nombre == 'Viernes':
                viernes = True
            if neg.nombre == 'Sábado':
                sabado = True
            if neg.nombre == 'Domingo':
                domingo = True

        update_form = UpdateBusiness(request.POST or None, request.FILES or None, instance=negocio)

        if request.method == 'POST':
            with transaction.atomic():
                category_bussiness = request.POST.getlist('category_bussiness')
                services_bussiness = request.POST.getlist('services_bussiness')
                hour_init = request.POST.get('hour_init_bussiness')
                hour_end = request.POST.get('hour_end_bussiness')
                post_frecuencia = request.POST.getlist('frecuencia_bussiness')
                address_bussiness = request.POST.get('address_bussiness')
                municipio = request.POST.get('municipio_bussiness')
                phone_bussiness_o = request.POST.get('phone_bussiness_o')
                phone_bussiness = request.POST.get('phone_bussiness')

                horario = str(hour_init) + ' - ' + str(hour_end)

                Negocio.objects.filter(pk=id_bussiness).update(
                    usuario_negocio=request.user,
                    horario=horario,
                    direccion=address_bussiness,
                    municipio_id=municipio,
                    telefono1=phone_bussiness_o,
                    telefono2=phone_bussiness
                )
                negocio.categorias.set(Categoria_Negocio.objects.filter(nombre__in=category_bussiness))
                negocio.servicios.set(Servicio.objects.filter(nombre__in=services_bussiness))
                negocio.frecuencia.set(Frecuencia.objects.filter(nombre__in=post_frecuencia))

                if update_form.is_valid():
                    edit = update_form.save(commit=False)
                    edit.save()

                return redirect('panel')

        context = {'negocio': negocio,
                   'lunes': lunes, 'martes': martes, 'miercoles': miercoles,
                   'jueves': jueves, 'viernes': viernes,
                   'sabado': sabado, 'domingo': domingo,
                   'hr_init': hr_init, 'hr_end': hr_end,
                   'update_form': update_form,
                   'servicios': servicios,
                   'servicios_marcados': servicios_marcados,
                   'servicios_no_marcados': servicios_no_marcados,
                   'frecuencias_marcadas': frecuencias_marcadas,
                   'frecuencia_no_marcados': frecuencia_no_marcados,
                   'categoria_no_marcados': categoria_no_marcados,
                   'categorias_marcadas': categorias_marcadas, 'categorias': categorias, 'macros': macro,
                   'notificaciones': notificaciones, 'cant_notificaciones': cant_notificaciones}
        return render(request, "control_panel/module_businesses/editar_negocio.html", context)
    return redirect('login')


def delete_bussiness(request, id_bussiness):
    if request.user.is_authenticated:
        p = Negocio.objects.get(id=id_bussiness)
        p.delete()
        return redirect('bussiness')
    return redirect('login')


def delete_bussiness_panel(request, id_bussiness):
    if request.user.is_authenticated:
        p = Negocio.objects.get(id=id_bussiness)
        p.delete()
        return redirect('panel')
    return redirect('login')


def my_bussiness(request, id_bussiness):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        productos = Producto.objects.filter(negocio=negocio.id)
        ofertas_laborales = Oferta_Laboral.objects.filter(negocio=negocio.id)
        comentarios = ComentarioEvaluacion.objects.filter(negocio=negocio.id)
        business_persona = QuerySet
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)

        context = {'business': business, 'negocio': negocio,
                   'productos_negocio': productos,
                   'ofertas_laborales': ofertas_laborales,
                   'comentarios_negocio': comentarios, 'business_persona': business_persona,
                   'notificaciones': notificaciones, 'cant_notificaciones': cant_notificaciones}
        return render(request, "control_panel/module_businesses/mi_negocio.html", context)
    return redirect('login')


def activate_business(request, id_bussiness):
    if request.user.is_authenticated:
        Negocio.objects.filter(id=id_bussiness).update(is_closed=False, fecha_alta=date.today())
        return redirect('panel')
    return redirect('login')


def blocked_business(request, id_bussiness):
    if request.user.is_authenticated:
        Negocio.objects.filter(id=id_bussiness).update(is_closed=True, fecha_alta=date.today())
        return redirect('panel')
    return redirect('login')


def comments(request, id_bussiness):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocios = Negocio.objects.all()
        Pedido.objects.filter()
        comentarios = ComentarioEvaluacion.objects.filter(negocio__id=id_bussiness)

        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        context = {'negocios': negocios, 'business': business, 'notificaciones': notificaciones,
                   'cant_notificaciones': cant_notificaciones, 'comentarios': comentarios}
        return render(request, "control_panel/module_businesses/comentarios.html", context)
    return redirect('login')


def get_next_weekday(startdate, weekday):
    """
    @startdate: given date, in format '2013-05-25'
    @weekday: week day as a integer, between 0 (Monday) to 6 (Sunday)
    """
    d = datetime.strptime(startdate, '%Y-%m-%d')
    t = timedelta((7 + weekday - d.weekday()) % 7)
    return d + t


def factura_bussiness(request, id_bussiness):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocios = Negocio.objects.all()
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        today = date.today()
        offset = (today.weekday() - 6) % 7
        last_sunday = today - timedelta(days=offset)
        next_saturday = get_next_weekday(str(today), 5)
        print(last_sunday)
        print(next_saturday.date())
        pedidos_for_date = Pedido.objects.filter(negocio=negocio).filter(fecha_reservacion__range=[last_sunday,
                                                                                                   next_saturday.date()])
        from django.db.models import Sum
        total_pagar = pedidos_for_date.aggregate(Sum('porciento_pagar'))

        if request.method == 'POST':
            note_factura_negocio = request.POST.get('note_factura_negocio')
            Factura_KeRapido.objects.create(
                total_porciento_pagar=total_pagar['porciento_pagar__sum'],
                negocio=negocio,
                nota=note_factura_negocio
            )
            mensaje_notificacion = ' KeRápido envió la factura de esta semana al negocio: ' + negocio.nombre
            if mensaje_notificacion != '':
                notificacion = Notification(mensaje=mensaje_notificacion, usuario=request.user, negocio=negocio,
                                            estado='No-Leida', tipo='Factura')
                notificacion.save()
            messages.success(request, 'Factura enviada satisfactoriamente')
            return redirect('bussiness')
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))
        fecha_emision = datetime.now()
        # return redirect(reverse('bussiness', args=(negocio.id,)))
        context = {'negocios': negocios, 'negocio': negocio, 'business': business, 'notificaciones': notificaciones,
                   'cant_notificaciones': cant_notificaciones, 'fecha_emision': fecha_emision,
                   'pedidos_for_date': pedidos_for_date, 'total_pagar': total_pagar}
        return render(request, "control_panel/module_businesses/factura_negocio.html", context)
    return redirect('login')


# -------------------Módulo Categoria Productos---------------#

def categoria_productos(request, id_bussiness):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        categorias = Categoria_Producto.objects.filter(negocio=negocio).order_by('-nombre').reverse()
        business_persona = QuerySet
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        context = {'business': business, 'negocio': negocio, 'categorias': categorias,
                   'business_persona': business_persona, 'notificaciones': notificaciones,
                   'cant_notificaciones': cant_notificaciones}
        return render(request,
                      "control_panel/module_category_products/listado_categoria_productos.html", context)
    return redirect('login')


def agregar_categoria_productos(request, id_bussiness):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        business_persona = QuerySet
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        if request.method == 'POST':
            name_category = request.POST.get('name_category')
            description_category = request.POST.get('description_category')
            Categoria_Producto.objects.create(nombre=name_category, descripcion=description_category, negocio=negocio)
            messages.success(request, 'Categoria agregada correctamente')
            return redirect(reverse('category_products', args=(id_bussiness,)))
        context = {'business': business, 'negocio': negocio, 'business_persona': business_persona,
                   'notificaciones': notificaciones, 'cant_notificaciones': cant_notificaciones}
        return render(request,
                      "control_panel/module_category_products/agregar_categoria_producto.html", context)
    return redirect('login')


def editar_categoria_producto(request, id_bussiness, id_category):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        categoria = get_object_or_404(Categoria_Producto, pk=id_category)
        business_persona = QuerySet
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        if request.method == 'POST':
            name_category = request.POST.get('name_category')
            description_category = request.POST.get('description_category')
            Categoria_Producto.objects.filter(id=id_category).update(
                nombre=name_category,
                descripcion=description_category
            )
            messages.success(request, 'Categoria modificada correctamente')
            return redirect(reverse('category_products', args=(id_bussiness,)))
        context = {'business': business, 'negocio': negocio, 'categoria': categoria,
                   'business_persona': business_persona, 'notificaciones': notificaciones,
                   'cant_notificaciones': cant_notificaciones}
        return render(request,
                      "control_panel/module_category_products/editar_categoria_producto.html", context)
    return redirect('login')


def delete_categoria(request, id_category):
    if request.user.is_authenticated:
        p = Categoria_Producto.objects.get(id=id_category)
        p.delete()
        messages.success(request, 'Categoría eliminada correctamente')
        return redirect(reverse('category_products', args=(p.negocio.id,)))
    return redirect('login')


# -------------------Módulo Productos---------------#

def products(request, id_bussiness):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        productos = Producto.objects.filter(negocio=negocio)
        business_persona = QuerySet
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        context = {'business': business, 'productos': productos, 'negocio': negocio,
                   'business_persona': business_persona, 'notificaciones': notificaciones,
                   'cant:notificaciones': cant_notificaciones}
        return render(request, "control_panel/module_products/listado_producto.html", context)
    return redirect('login')


def add_product(request, id_bussiness):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        categorias = Categoria_Producto.objects.filter(negocio=id_bussiness)
        business_persona = QuerySet
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))
        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        add_form = MyForm(request.POST or None, request.FILES or None)
        if add_form.is_valid():
            imagen = add_form.cleaned_data['imagen']
            nombre = add_form.cleaned_data['nombre']
            cantidad_producto = add_form.cleaned_data['cantidad_producto']
            descripcion = add_form.cleaned_data['descripcion']
            precio = add_form.cleaned_data['precio']
            categoria = add_form.cleaned_data['categoria']

            p = Producto(imagen=imagen, nombre=nombre, cantidad_producto=cantidad_producto,
                         descripcion=descripcion, precio=precio, categoria=categoria,
                         negocio=negocio)
            p.save()
            messages.success(request, 'Producto agregado correctamente')
            return redirect(reverse('products', args=(negocio.id,)))

        context = {'business': business, 'negocio': negocio, 'categorias': categorias,
                   'business_persona': business_persona, 'cant_notificaciones': cant_notificaciones,
                   'notificaciones': notificaciones, 'add_form': add_form}
        return render(request, "control_panel/module_products/agregar_producto.html", context)
    return redirect('login')


def editar_product(request, id_bussiness, id_product):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        producto = get_object_or_404(Producto, pk=id_product)
        business_persona = QuerySet
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        update_form = MyForm(request.POST or None, request.FILES or None, instance=producto)
        if update_form.is_valid():
            edit = update_form.save(commit=False)
            edit.save()
            messages.success(request, 'Producto modificado correctamente')
            return redirect(reverse('products', args=(id_bussiness,)))
        context = {'business': business, 'negocio': negocio, 'producto': producto, 'update_form': update_form,
                   'business_persona': business_persona, 'cant_notificaciones': cant_notificaciones,
                   'notificaciones': notificaciones}
        return render(request, "control_panel/module_products/editar_producto.html", context)
    return redirect('login')


def delete_product(request, id_product):
    if request.user.is_authenticated:
        p = Producto.objects.get(id=id_product)
        p.delete()
        messages.success(request, 'Producto eliminado correctamente')
        return redirect(reverse('products', args=(p.negocio.id,)))
    return redirect('login')


# -------------------Módulo Ofertas---------------#

def offers(request, id_bussiness):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        ofertas = Oferta_Laboral.objects.filter(negocio=negocio)
        business_persona = QuerySet
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        context = {'business': business, 'negocio': negocio, 'ofertas': ofertas, 'business_persona': business_persona,
                   'cant_notificaciones': cant_notificaciones, 'notificaciones': notificaciones}
        return render(request, "control_panel/module_offers/listado_ofertas.html", context)
    return redirect('login')


def add_offer(request, id_bussiness):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        business_persona = QuerySet
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))
        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        if request.method == 'POST':
            description_corta = request.POST.get('description_corta')
            description_offer = request.POST.get('description_offer')
            nombre_contacto = request.POST.get('nombre_contacto')
            correo = request.POST.get('correo')
            telefono1 = request.POST.get('telefono1')
            telefono2 = request.POST.get('telefono2')

            Oferta_Laboral.objects.create(descripcion_corta=description_corta,
                                          descripcion=description_offer,
                                          nombre_contacto=nombre_contacto,
                                          negocio=negocio,
                                          correo=correo,
                                          telefono1=telefono1,
                                          telefono2=telefono2)

            messages.success(request, 'Oferta agregada correctamente')
            return redirect(reverse('offers', args=(id_bussiness,)))
        context = {'business': business, 'negocio': negocio, 'business_persona': business_persona,
                   'cant_notificaciones': cant_notificaciones, 'notificaciones': notificaciones}
        return render(request, "control_panel/module_offers/agregar_oferta.html", context)
    return redirect('login')


def update_offer(request, id_bussiness, id_offer):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        offer = get_object_or_404(Oferta_Laboral, pk=id_offer)
        business_persona = QuerySet
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        if request.method == 'POST':
            descripcion_corta = request.POST.get('description_corta')
            description_offer = request.POST.get('description_offer')
            nombre_contacto = request.POST.get('nombre_contacto')
            correo = request.POST.get('correo')
            telefono1 = request.POST.get('telefono1')
            telefono2 = request.POST.get('telefono2')

            Oferta_Laboral.objects.filter(id=id_offer).update(descripcion_corta=descripcion_corta,
                                                              descripcion=description_offer,
                                                              nombre_contacto=nombre_contacto,
                                                              negocio=negocio, correo=correo,
                                                              telefono1=telefono1,
                                                              telefono2=telefono2)

            messages.success(request, 'Oferta modificada correctamente')
            return redirect(reverse('offers', args=(id_bussiness,)))
        context = {'business': business, 'negocio': negocio, 'offer': offer, 'business_persona': business_persona,
                   'notificaciones': notificaciones, 'cant_notificaciones': cant_notificaciones}
        return render(request, "control_panel/module_offers/editar_oferta.html", context)
    return redirect('login')


def delete_offer(request, id_offer):
    if request.user.is_authenticated:
        p = Oferta_Laboral.objects.get(id=id_offer)
        p.delete()
        messages.success(request, 'Oferta eliminada correctamente')
        return redirect(reverse('offers', args=(p.negocio.id,)))
    return redirect('login')


# -------------------Módulo Tarifas---------------#

def rates(request, id_bussiness):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        tarifas = Tarifa_Entrega.objects.filter(negocio=id_bussiness)
        business_persona = QuerySet
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))
        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        context = {'business': business, 'negocio': negocio, 'tarifas': tarifas, 'business_persona': business_persona,
                   'notificaciones': notificaciones, 'cant_notificaciones': cant_notificaciones}
        return render(request, "control_panel/module_rates/listado_tarifas.html", context)
    return redirect('login')


def add_rate(request, id_bussiness):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        business_persona = QuerySet
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))
        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        municipios = Municipio.objects.all()
        if request.method == 'POST':
            lugar_destino = request.POST.get('lugar_destino')
            precio = request.POST.get('precio_rate')
            is_tarifa = Tarifa_Entrega.objects.filter(lugar_destino=lugar_destino)
            if is_tarifa:
                messages.error(request, 'Ya se encuentra ese municipio')
                return redirect(reverse('rates', args=(id_bussiness,)))
            else:
                Tarifa_Entrega.objects.create(lugar_destino=lugar_destino, precio=precio, negocio=negocio)
                messages.success(request, 'Tarifa agregada correctamente')
                return redirect(reverse('rates', args=(id_bussiness,)))
        context = {'business': business, 'negocio': negocio, 'municipios': municipios,
                   'business_persona': business_persona, 'cant_notificaciones': cant_notificaciones,
                   'notificaciones': notificaciones}
        return render(request, "control_panel/module_rates/agregar_tarifa.html", context)
    return redirect('login')


def update_rate(request, id_bussiness, id_rate):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        rate = get_object_or_404(Tarifa_Entrega, pk=id_rate)
        business_persona = QuerySet
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))
        if request.user.is_persona_encargada:
            persona_encargada = PerfilPersonaEncargada.objects.get(persona_encargada=request.user)
            business_persona = Negocio.objects.filter(pk=persona_encargada.negocio_pertenece.id)
        if request.method == 'POST':
            lugar_destino = request.POST.get('lugar_destino')
            precio = request.POST.get('precio_rate')
            Tarifa_Entrega.objects.filter(id=id_rate).update(lugar_destino=lugar_destino, precio=precio)
            messages.success(request, 'Tarifa modificada correctamente')
            return redirect(reverse('rates', args=(id_bussiness,)))
        context = {'business': business, 'negocio': negocio, 'rate': rate, 'business_persona': business_persona,
                   'cant_notificaciones': cant_notificaciones, 'notificaciones': notificaciones}
        return render(request, "control_panel/module_rates/editar_tarifa.html", context)
    return redirect('login')


def delete_rate(request, id_rate):
    if request.user.is_authenticated:
        p = Tarifa_Entrega.objects.get(id=id_rate)
        p.delete()
        messages.success(request, 'Tarifa eliminada correctamente')
        return redirect(reverse('rates', args=(p.negocio.id,)))
    return redirect('login')


# -------------------Notifications---------------#

def messages_center(request):
    if request.user.is_authenticated:
        todas_notificaciones = []
        # Notificaciones------------------------------------
        notificaciones = []
        cant_notificaciones = 0
        if request.user.is_superuser:
            todas_notificaciones = Notification.objects.all()
            notificaciones = Notification.objects.filter(estado='No-Leida').order_by('-fecha')[:5]
            cant_notificaciones = len(notificaciones)
        elif request.user.is_administrador:
            qset = (
                    Q(tipo='Usuario') |
                    Q(tipo='Negocio') |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset).exclude(
                mensaje__icontains=request.user.username).distinct()
            todas_notificaciones = notificaciones
            notificaciones = notificaciones.order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        elif request.user.is_persona_encargada:
            persona = get_object_or_404(PerfilPersonaEncargada, pk=request.user.id)
            negocio = get_object_or_404(Negocio, pk=persona.negocio_pertenece.id)
            qset1 = (
                    Q(tipo='Pedido') |
                    Q(negocio=negocio.id) |
                    Q(estado='No-Leida')
            )
            notificaciones = Notification.objects.filter(qset1).exclude(
                mensaje__icontains=request.user.username).distinct()
            todas_notificaciones = notificaciones
            notificaciones = notificaciones.order_by('-fecha')[:5]
            cant_notificaciones = len(list(notificaciones))
        else:
            afiliado = get_object_or_404(PerfilAfiliado, afiliado_id=request.user.id)
            if Negocio.objects.all().count() != 0:
                negocios = Negocio.objects.filter(usuario_negocio_id=afiliado.afiliado.id)
                for negocio in negocios:
                    if negocio:
                        qset1 = (
                                Q(tipo='Pedido') |
                                Q(negocio=negocio.id) |
                                Q(estado='No-Leida')
                        )
                        notificaciones = Notification.objects.filter(qset1).distinct().order_by('-fecha')[:5]
                        notificaciones = list(notificaciones)
                        notificaciones += notificaciones
                        cant_notificaciones = len(list(notificaciones))

        context = {'notificaciones': notificaciones, 'todas_notificaciones': todas_notificaciones,
                   'cant_notificaciones': cant_notificaciones}
        return render(request, 'control_panel/module_notifications/listado_notificaciones.html', context)
    return redirect('login')


def delete_message(request, id_message):
    if request.user.is_authenticated:
        n = Notification.objects.get(id=id_message)
        n.delete()
        return redirect('notifications_center')
    return redirect('login')


def mask_as_read(request, id_message):
    if request.user.is_authenticated:
        Notification.objects.filter(pk=id_message).update(estado='Leida')
        return redirect('notifications_center')
    return redirect('login')


def mask_as_no_read(request, id_message):
    if request.user.is_authenticated:
        Notification.objects.filter(pk=id_message).update(estado='No-Leida')
        return redirect('notifications_center')
    return redirect('login')


def apk_construccion(request):
    context = {}
    return render(request, "apk.html", context)
