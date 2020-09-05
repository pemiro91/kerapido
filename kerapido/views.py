from datetime import datetime
from itertools import product

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as do_logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
#
# def principal(request):
#     context = {}
#     return render(request, "master/index.html", context)
from django.urls import reverse

from kerapido.models import User, Negocio, Oferta_Laboral, Categoria_Negocio, Municipio, Frecuencia, \
    Servicio, Macro, Categoria_Producto, Producto, ComentarioEvaluacion


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
    macro_categorias = Macro.objects.all()
    bussiness = Negocio.objects.all()[:6]
    ofertas = Oferta_Laboral.objects.all()
    productos = Producto.objects.all()
    if request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        send_mail(subject, message, 'habanatrans16@gmail.com', ['pemiro91@gmail.com'], fail_silently=False)
        messages.success(request, 'Su mensaje ha sido enviado satisfactoriamente. Gracias!')
        # return redirect('/')
    context = {'macro_categorias': macro_categorias, 'bussiness': bussiness, 'ofertas': ofertas,
               'prodductos': productos}
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
                tiene_negocio = Negocio.objects.filter(usuario_negocio=user)
                if tiene_negocio:
                    return redirect('panel')
                else:
                    return redirect('add_bussiness')
        else:
            messages.warning(request, 'username or password not correct')
            return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, "control_panel/pages/sign-in.html", {'form': form})


def base(request):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        services = Servicio.objects.all()
        context = {'business': business, 'services': services}
        return render(request, "control_panel/base.html", context)
    return redirect('login')


def admin_panel(request):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        services = Servicio.objects.all()
        context = {'business': business, 'services': services}
        return render(request, "control_panel/index.html", context)
    return redirect('login')


def logout(request):
    do_logout(request)
    return redirect('login')


def profile(request):
    if request.user.is_authenticated:
        bussiness = Negocio.objects.filter(usuario_negocio=request.user)
        context = {'negocios': bussiness}
        return render(request, "control_panel/pages/perfil.html", context)
    return redirect('login')


def register_afiliado(request):
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
    if request.user.is_authenticated:
        services = Servicio.objects.all()
        business = Negocio.objects.filter(usuario_negocio=request.user)
        context = {'services': services, 'business': business}
        return render(request, "control_panel/pages/listado_servicios.html", context)
    return redirect('login')


def add_services(request):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        if request.method == 'POST':
            name_service = request.POST.get('name_service')
            description_service = request.POST.get('description_service')
            color_service = request.POST.get('color_service')
            Servicio.objects.create(nombre=name_service, descripcion=description_service, color=color_service)
            return redirect('services')
        context = {'business': business}
        return render(request, "control_panel/pages/agregar_servicios.html", context)
    return redirect('login')


def update_service(request, id_service):
    if request.user.is_authenticated:
        service = Servicio.objects.get(id=id_service)
        business = Negocio.objects.filter(usuario_negocio=request.user)
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
                return redirect('services')
        context = {'service': service, 'business': business}
        return render(request, "control_panel/pages/editar_servicios.html", context)
    return redirect('login')


def delete_service(request, id_service):
    if request.user.is_authenticated:
        p = Servicio.objects.get(id=id_service)
        p.delete()
        return redirect('services')
    return redirect('login')


def reservations(request):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        context = {'business': business}
        return render(request, "control_panel/pages/listado_reservaciones.html", context)
    return redirect('login')


def nuestros_afiliados(request):
    context = {}
    return render(request, "nuestros_afiliados.html", context)


def users(request):
    if request.user.is_authenticated:
        usuarios = User.objects.all().exclude(is_superuser=True).exclude(username=request.user.username)
        business = Negocio.objects.filter(usuario_negocio=request.user)
        context = {'usuarios': usuarios, 'business': business}
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


def update_user(request, id_user):
    if request.user.is_authenticated:
        user_custom = User.objects.get(id=id_user)
        business = Negocio.objects.filter(usuario_negocio=request.user)
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
                return redirect('users')
        context = {'user': user_custom, 'business': business}
        return render(request, "control_panel/pages/editar_usuario.html", context)
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


def products(request, id_bussiness):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        productos = Producto.objects.filter(negocio=negocio)
        context = {'business': business, 'productos': productos, 'negocio': negocio}
        return render(request, "control_panel/pages/listado_producto.html", context)
    return redirect('login')


def add_product(request, id_bussiness):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        categorias = Categoria_Producto.objects.filter(negocio=id_bussiness)
        if request.method == 'POST':
            image_product = request.FILES['image_product']
            name_product = request.POST.get('name_product')
            description_product = request.POST.get('description_product')
            price_product = request.POST.get('price_product')
            category_product = request.POST.get('category_product')
            Producto.objects.create(imagen=image_product,
                                    nombre=name_product, descripcion=description_product, precio=price_product,
                                    negocio=negocio, categoria_id=category_product)
            return redirect(reverse('products', args=(id_bussiness,)))
        context = {'business': business, 'negocio': negocio, 'categorias': categorias}
        return render(request, "control_panel/pages/agregar_producto.html", context)
    return redirect('login')


def editar_product(request, id_bussiness, id_product):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        producto = get_object_or_404(Producto, pk=id_product)
        categorias = Categoria_Producto.objects.filter(negocio=id_bussiness)
        if request.method == 'POST':
            name_product = request.POST.get('name_product')
            description_product = request.POST.get('description_product')
            price_product = request.POST.get('price_product')
            category_product = request.POST.get('category_product')
            Producto.objects.filter(id=id_product).update(
                nombre=name_product,
                descripcion=description_product,
                precio=price_product,
                categoria_id=category_product
            )
            return redirect(reverse('products', args=(id_bussiness,)))
        context = {'business': business, 'negocio': negocio, 'producto': producto, 'categorias': categorias}
        return render(request, "control_panel/pages/editar_producto.html", context)
    return redirect('login')


def delete_product(request, id_product):
    if request.user.is_authenticated:
        p = Producto.objects.get(id=id_product)
        p.delete()
        return redirect(reverse('products', args=(p.negocio.id,)))
    return redirect('login')


def categoria_productos(request, id_bussiness):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        categorias = Categoria_Producto.objects.filter(negocio=negocio).order_by('-nombre').reverse()
        context = {'business': business, 'negocio': negocio, 'categorias': categorias}
        return render(request, "control_panel/pages/listado_categoria_productos.html", context)
    return redirect('login')


def agregar_categoria_productos(request, id_bussiness):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        if request.method == 'POST':
            name_category = request.POST.get('name_category')
            description_category = request.POST.get('description_category')
            Categoria_Producto.objects.create(nombre=name_category, descripcion=description_category, negocio=negocio)
            return redirect(reverse('category_products', args=(id_bussiness,)))
        context = {'business': business, 'negocio': negocio}
        return render(request, "control_panel/pages/agregar_categoria_producto.html", context)
    return redirect('login')


def editar_categoria_producto(request, id_bussiness, id_category):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        categoria = get_object_or_404(Categoria_Producto, pk=id_category)
        if request.method == 'POST':
            name_category = request.POST.get('name_category')
            description_category = request.POST.get('description_category')
            Categoria_Producto.objects.filter(id=id_category).update(
                nombre=name_category,
                descripcion=description_category
            )
            return redirect(reverse('category_products', args=(id_bussiness,)))
        context = {'business': business, 'negocio': negocio, 'categoria': categoria}
        return render(request, "control_panel/pages/editar_categoria_producto.html", context)
    return redirect('login')


def delete_categoria(request, id_category):
    if request.user.is_authenticated:
        p = Categoria_Producto.objects.get(id=id_category)
        p.delete()
        return redirect(reverse('category_products', args=(p.negocio.id,)))
    return redirect('login')


def businesses(request):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocios = Negocio.objects.all()
        context = {'negocios': negocios, 'business': business}
        return render(request, "control_panel/pages/listado_negocios.html", context)
    return redirect('login')


def add_bussiness(request):
    if request.user.is_authenticated:
        municipios = Municipio.objects.all()
        frecuencia = Frecuencia.objects.all()
        servicios_mostrar = Servicio.objects.all()
        categorias = Categoria_Negocio.objects.all()
        macro = Macro.objects.all()
        if request.method == 'POST':
            name_bussiness = request.POST.get('name_bussiness')
            logo_bussiness = request.FILES['logo_bussiness']
            portada_bussiness = request.FILES['portada_bussiness']
            slogan_bussiness = request.POST.get('slogan_bussiness')
            category_bussiness = request.POST.getlist('category_bussiness')
            services_bussiness = request.POST.getlist('services_bussiness')
            hour_init = request.POST.get('hour_init')
            hour_end = request.POST.get('hour_end')
            post_frecuencia = request.POST.getlist('frecuencia')
            address_bussiness = request.POST.get('address_bussiness')
            municipio = request.POST.get('municipio')
            phone_bussiness_o = request.POST.get('phone_bussiness_o')
            phone_bussiness = request.POST.get('phone_bussiness')

            horario = str(hour_init) + ' - ' + str(hour_end)

            negocio = Negocio.objects.create(
                usuario_negocio=request.user,
                nombre=name_bussiness,
                logo=logo_bussiness,
                portada=portada_bussiness,
                eslogan=slogan_bussiness,
                horario=horario,
                direccion=address_bussiness,
                municipio=municipio,
                telefono1=phone_bussiness_o,
                telefono2=phone_bussiness
            )
            for category in category_bussiness:
                categoria = Categoria_Negocio.objects.get(nombre=category)
                negocio.categorias.add(categoria)

            for service in services_bussiness:
                servicio = Servicio.objects.get(nombre=service)
                negocio.servicios.add(servicio)

            for frecu in post_frecuencia:
                frecuen = Frecuencia.objects.create(nombre=frecu)
                negocio.frecuencia.add(frecuen)

            return redirect(reverse('my_bussiness', args=(negocio.id,)))

        context = {'municipios': municipios, 'frecuencia': frecuencia, 'servicios_mostrar': servicios_mostrar,
                   'categorias': categorias, 'macros': macro}
        return render(request, "control_panel/pages/agregar_negocio.html", context)
    return redirect('login')


def update_bussiness(request, id_bussiness):
    if request.user.is_authenticated:
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        servicios = Servicio.objects.all()
        servicios_marcados = list(negocio.servicios.all())
        categorias_marcadas = list(negocio.categorias.all())
        categorias = Categoria_Negocio.objects.all()
        macro = Macro.objects.all()
        servicios_no_marcados = []
        categoria_no_marcados = []
        hr_init = negocio.horario.split('-')[0]
        hr_end = negocio.horario.split('-')[1]
        lunes = False
        martes = False
        miercoles = False
        jueves = False
        viernes = False
        sabado = False
        domingo = False
        for i in servicios:
            if (i not in servicios_no_marcados) and (i not in servicios_marcados):
                servicios_no_marcados.append(i)

        for i in categorias:
            if (i not in categoria_no_marcados) and (i not in categorias_marcadas):
                categoria_no_marcados.append(i)

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

        if request.method == 'POST':
            name_bussiness = request.POST.get('name_bussiness')
            logo_bussiness = request.FILES['logo_bussiness']
            portada_bussiness = request.FILES['portada_bussiness']
            slogan_bussiness = request.POST.get('slogan_bussiness')
            category_bussiness = request.POST.getlist('category_bussiness')
            services_bussiness = request.POST.getlist('services_bussiness')
            hour_init = request.POST.get('hour_init')
            hour_end = request.POST.get('hour_end')
            post_frecuencia = request.POST.getlist('frecuencia')
            address_bussiness = request.POST.get('address_bussiness')
            municipio = request.POST.get('municipio')
            phone_bussiness_o = request.POST.get('phone_bussiness_o')
            phone_bussiness = request.POST.get('phone_bussiness')

            horario = str(hour_init) + ' - ' + str(hour_end)

            with transaction.atomic():
                negocio = Negocio.objects.filter(pk=id_bussiness).update(
                    usuario_negocio=request.user,
                    nombre=name_bussiness,
                    logo=logo_bussiness,
                    portada=portada_bussiness,
                    eslogan=slogan_bussiness,
                    horario=horario,
                    direccion=address_bussiness,
                    municipio=municipio,
                    telefono1=phone_bussiness_o,
                    telefono2=phone_bussiness
                )

                for category in category_bussiness:
                    categoria = Categoria_Negocio.objects.get(nombre=category)
                    negocio.categorias.add(categoria)

                for service in services_bussiness:
                    servicio = Servicio.objects.get(nombre=service)
                    negocio.servicios.add(servicio)

                for frecu in post_frecuencia:
                    frecuen = Frecuencia.objects.create(nombre=frecu)
                    negocio.frecuencia.add(frecuen)

                return redirect('panel')
        context = {'negocio': negocio,
                   'lunes': lunes, 'martes': martes, 'miercoles': miercoles,
                   'jueves': jueves, 'viernes': viernes,
                   'sabado': sabado, 'domingo': domingo,
                   'hr_init': hr_init, 'hr_end': hr_end,
                   'servicios': servicios,
                   'servicios_marcados': servicios_marcados,
                   'servicios_no_marcados': servicios_no_marcados,
                   'categoria_no_marcados': categoria_no_marcados,
                   'categorias_marcadas': categorias_marcadas, 'categorias': categorias, 'macros': macro}
        return render(request, "control_panel/pages/editar_negocio.html", context)
    return redirect('login')


def delete_bussiness(request, id_bussiness):
    if request.user.is_authenticated:
        p = Negocio.objects.get(id=id_bussiness)
        p.delete()
        return redirect('panel')
    return redirect('login')


def error404(request):
    context = {}
    return render(request, "control_panel/pages/404.html", context)


def terminos_condiciones(request):
    context = {}
    return render(request, "control_panel/pages/terminos_condiicones.html", context)


def mi_negocio(request, id_bussiness):
    if request.user.is_authenticated:
        business = Negocio.objects.filter(usuario_negocio=request.user)
        negocio = get_object_or_404(Negocio, pk=id_bussiness)
        productos = Producto.objects.filter(negocio=negocio.id)
        ofertas_laborales = Oferta_Laboral.objects.filter(negocio=negocio.id)
        comentarios = ComentarioEvaluacion.objects.filter(negocio=negocio.id)

        context = {'business': business, 'negocio': negocio,
                   'productos_negocio': productos,
                   'ofertas_laborales': ofertas_laborales,
                   'comentarios_negocio': comentarios}
        return render(request, "control_panel/pages/mi_negocio.html", context)
    return redirect('login')


def categories(request):
    if request.user.is_authenticated:
        category = Categoria_Negocio.objects.all()
        business = Negocio.objects.filter(usuario_negocio=request.user)
        context = {'categories': category, 'business': business}
        return render(request, "control_panel/pages/listado_categoria.html", context)
    return redirect('login')


def add_category(request):
    if request.user.is_authenticated:
        macro = Macro.objects.all()
        if request.method == 'POST':
            name_category = request.POST.get('name_category')
            description_category = request.POST.get('description_category')
            macro_field = request.POST.get('macro')
            Categoria_Negocio.objects.create(nombre=name_category, descripcion=description_category,
                                             macro_id=macro_field)
            return redirect('categories')
        context = {'macros': macro}
        return render(request, "control_panel/pages/agregar_categoria_negocio.html", context)
    return redirect('login')


def update_category(request, id_category):
    if request.user.is_authenticated:
        category = Categoria_Negocio.objects.get(id=id_category)
        macro = Macro.objects.all()
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
        context = {'category': category}
        return render(request, "control_panel/pages/editar_categoria.html", context)
    return redirect('login')


def delete_category(request, id_category):
    if request.user.is_authenticated:
        p = Categoria_Negocio.objects.get(id=id_category)
        p.delete()
        return redirect('categories')
    return redirect('login')
