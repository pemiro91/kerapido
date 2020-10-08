from abc import ABC

from django.contrib.auth import authenticate
from django.db.models import Avg, Func
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED
)

from kerapido.serializers import *


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Por favor introduzca un usuario o contraseña válido'}, status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Aún no se ha verificado su cuenta'}, status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    context = {'token': token.key, 'usuario': {'id': user.id, 'username': user.username, 'telefono': user.telefono}}
    return Response(context, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
def getNegociosApi(request):
    negocio = Negocio.objects.all()
    serializer = NegocioSerializer(negocio, many=True)
    return Response({'list_business': serializer.data}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
def getNegocioApi(request, pk):
    negocio = Negocio.objects.filter(pk=pk)
    # negocio = get_object_or_404(Negocio, pk=pk)
    serializer = NegocioSerializer(negocio, many=True)
    return Response({'business': serializer.data}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
def getProductoApi(request, pk):
    producto = Producto.objects.filter(negocio=pk)
    serializer = ProductoSerializer(producto, many=True)
    return Response({'list_dishes': serializer.data}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
def getCategoriaApi(request, pk):
    categoria = Categoria_Producto.objects.filter(negocio=pk)
    serializer = Categoria_ProductoSerializer(categoria, many=True)
    return Response({'list_categorias': serializer.data}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def postReservaApi(request):
    serializer = PedidoSerializer(data=request.data)
    reservaciones = request.data.get("reservaciones")
    for reser in reservaciones:
        print(reser)
    # Producto.objects.filter(id=id_producto)
    # serializer.is_valid(raise_exception=True)
    # serializer.save()
    return Response({'message': 'Reserva realizada satisfactoriamente'}, status=HTTP_201_CREATED)


@csrf_exempt
@api_view(["GET"])
def getReservasApiForID(request, pk):
    reservas = Pedido.objects.filter(cliente_auth=pk)
    serializer = PedidoSerializer(reservas, many=True)
    return Response({'list_reservas': serializer.data}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
def getServicioApiForID(request, pk):
    servicio = Servicio.objects.filter(negocio=pk)
    serializer = ServicioSerializer(servicio, many=True)
    return Response({'list_servicio': serializer.data}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
def getTarifaEntregaApiForID(request, pk):
    tarifa = Tarifa_Entrega.objects.filter(negocio=pk)
    serializer = Tarifa_EntregaSerializer(tarifa, many=True)
    return Response({'list_tarifa': serializer.data}, status=HTTP_200_OK)


class Round(Func, ABC):
    function = 'ROUND'
    arity = 2


@csrf_exempt
@api_view(["POST"])
def postComentarioApi(request, id_negocio):
    cliente = request.data.get("cliente")
    is_commet = ComentarioEvaluacion.objects.filter(cliente=cliente)
    if is_commet:
        return Response({'error': 'Usted ya ha comentado'}, status=HTTP_200_OK)
    else:
        serializer = ComentarioEvaluacionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        evaluacion = ComentarioEvaluacion.objects.filter(negocio=id_negocio)
        comentarios = ComentarioEvaluacion.objects.filter(negocio=id_negocio)
        serializer_commets = ComentarioEvaluacionSerializer(comentarios, many=True)
        stars_average = list(evaluacion.aggregate(average=Round(Avg('rating'), 2)).values())[0]
        Negocio.objects.filter(pk=id_negocio).update(rating=stars_average)
        return Response({'message': 'Comentario enviado satisfactoriamente', 'evaluacion': stars_average,
                         'list_comments': serializer_commets.data},
                        status=HTTP_201_CREATED)


@csrf_exempt
@api_view(["GET"])
def getComentarioApi(request, pk):
    comments = ComentarioEvaluacion.objects.filter(negocio=pk)
    serializer = ComentarioEvaluacionSerializer(comments, many=True)
    stars_average = list(comments.aggregate(average=Round(Avg('rating'), 2)).values())[0]
    return Response({'list_comments': serializer.data, 'evaluacion': stars_average}, status=HTTP_200_OK)
