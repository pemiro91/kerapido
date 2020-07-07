from django.shortcuts import render,redirect
from kerapido.models import Fotos


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


def admin_panel(request):
    # if request.user.is_authenticated:
        # productos = Product.objects.all()
        # cant_prod = len(productos)
        # cant_prod_disp = 0
        # vendedores = User.objects.filter(is_vendedor=True)
        # cant_vendedores: int = len(vendedores)
        # estado_reservaciones = Estado_Reservation.objects.all()
        # cant_reservaciones: int = len(estado_reservaciones)
        # reservaciones_ordenadas = Estado_Reservation.objects.order_by('-fecha_estado')[:5]
        # cant_res_ord = len(reservaciones_ordenadas)
        # reservaciones_pendientes = []
        # reservaciones_entregadas = []
        # reservaciones_canceladas = []
        # notificaciones = Notification.objects.all().exclude(usuario=request.user)[:3]
        # cant_notificaciones = len(notificaciones)
        #
        # if productos:
        #     for p in productos:
        #         cant_prod_disp += p.cantidad_disponible
        # if estado_reservaciones:
        #     for r in estado_reservaciones:
        #         if r.estado == 'Pendiente':
        #             reservacion = get_object_or_404(Reservation, pk=r.id)
        #             reservaciones_pendientes.append(reservacion)
        #         elif r.estado == 'Entregado':
        #             reservacion = get_object_or_404(Reservation, pk=r.id)
        #             reservaciones_entregadas.append(reservacion)
        #         else:
        #             reservacion = get_object_or_404(Reservation, pk=r.id)
        #             reservaciones_canceladas.append(reservacion)
        #
        # cant_reserv_pend = len(reservaciones_pendientes)
        # cant_reserv_entreg = len(reservaciones_entregadas)
        # cant_reserv_canc = len(reservaciones_canceladas)

    context = {
            # 'cant_prod_sistema': cant_prod, 'cant_reserv_pend': cant_reserv_pend,
            #        'cant_reserv_entreg': cant_reserv_entreg, 'cant_reserv_canc': cant_reserv_canc,
            #        'cant_vendedores': cant_vendedores, 'cant_prod_disp': cant_prod_disp,
            #        'cant_reservaciones': cant_reservaciones, 'reservaciones_ordenadas': reservaciones_ordenadas,
            #        'cant_res_ord': cant_res_ord, 'notificaciones': notificaciones,
            #        'cant_notificaciones': cant_notificaciones
        }
    return render(request, "control_panel/index_panel.html", context)
    # return redirect('')
