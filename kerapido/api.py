from abc import ABC

from django.contrib.auth import authenticate
from django.db.models import Avg, Func
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_409_CONFLICT,
    HTTP_401_UNAUTHORIZED
)
from rest_framework.views import APIView

from kerapido.serializers import *


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            user.set_password(request.data.get("password"))
            user.save()
            context = {'id': user.id, 'username': user.username, 'password': user.password, 'telefono': user.telefono,
                       'first_name': user.first_name, 'last_name': user.last_name,
                       'email': user.email}
            return Response(context, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def loginApp(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Por favor introduzca un usuario o contraseña válido'}, status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'error': 'Error de autenticación'}, status=HTTP_404_NOT_FOUND)
    if not user.is_active:
        return Response({'error': 'Aún no se ha verificado su cuenta'}, status=HTTP_401_UNAUTHORIZED)
    token, _ = Token.objects.get_or_create(user=user)
    context = {'token': token.key, 'usuario': {'id': user.id, 'username': user.username, 'telefono': user.telefono,
                                               'first_name': user.first_name, 'last_name': user.last_name,
                                               'email': user.email}}
    return Response(context, status=HTTP_200_OK)


class NegocioList(APIView):
    permission_classes = (AllowAny,)

    def get_object(self, pk):
        try:
            return Negocio.objects.get(pk=pk)
        except Negocio.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        negocios = Negocio.objects.filter(is_closed=False)
        serializer = NegocioSerializer(negocios, many=True)
        return Response({'list_business': serializer.data}, status=HTTP_200_OK)


class NegocioDetail(APIView):
    permission_classes = (AllowAny,)

    def get_object(self, pk):
        try:
            return Negocio.objects.get(pk=pk)
        except Negocio.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        negocio = self.get_object(pk)
        serializer = NegocioSerializer(negocio)
        return Response(serializer.data)


class ProductoList(APIView):
    permission_classes = (AllowAny,)

    def get_object(self, pk):
        try:
            return Negocio.objects.get(pk=pk)
        except Negocio.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        producto = Producto.objects.filter(negocio=pk)
        serializer = ProductoSerializer(producto, many=True)
        return Response({'list_dishes': serializer.data}, status=HTTP_200_OK)


class CategoriaList(APIView):
    permission_classes = (AllowAny,)

    def get_object(self, pk):
        try:
            return Negocio.objects.get(pk=pk)
        except Negocio.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        categoria = Categoria_Producto.objects.filter(negocio=pk)
        serializer = Categoria_ProductoSerializer(categoria, many=True)
        return Response({'list_categorias': serializer.data}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def postReservaApi(request):
    global list_reserva
    serializer = PedidoSerializer(data=request.data)
    reservaciones = request.data.get("reservaciones")
    list_product = []
    for reser in reservaciones:
        producto = Producto.objects.get(id=reser['producto'])
        if reser['cantidad_producto'] > producto.cantidad_producto:
            list_product.append(producto.nombre)
    if len(list_product) != 0:
        return Response({'message': list_product}, status=HTTP_404_NOT_FOUND)
    else:
        for reser in reservaciones:
            producto = Producto.objects.get(id=reser['producto'])
            count_final = producto.cantidad_producto - reser['cantidad_producto']
            print(count_final)
            Producto.objects.filter(id=reser['producto']).update(cantidad_producto=count_final)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            list_reserva = ['Reserva realizada satisfactoriamente']
        return Response({'message': list_reserva}, status=HTTP_201_CREATED)


@csrf_exempt
@api_view(["GET"])
def getReservasApiForID(request, pk):
    reservas = Pedido.objects.filter(cliente_auth=pk)
    serializer = PedidoSerializer(reservas, many=True)
    return Response({'list_reservas': serializer.data}, status=HTTP_200_OK)


class ServicioList(APIView):
    permission_classes = (AllowAny,)

    def get_object(self, pk):
        try:
            return Negocio.objects.get(pk=pk)
        except Negocio.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        servicio = Servicio.objects.filter(negocio=pk)
        serializer = ServicioSerializer(servicio, many=True)
        return Response({'list_servicio': serializer.data}, status=HTTP_200_OK)


class TarifaEntregaList(APIView):
    permission_classes = (AllowAny,)

    def get_object(self, pk):
        try:
            return Negocio.objects.get(pk=pk)
        except Negocio.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
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
    negocio = request.data.get("negocio")
    is_commet = ComentarioEvaluacion.objects.filter(negocio=negocio, cliente=cliente)
    if is_commet:
        return Response({'message': 'Usted ya ha comentado'}, status=HTTP_409_CONFLICT)
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


class ComentarioList(APIView):
    permission_classes = (AllowAny,)

    def get_object(self, pk):
        try:
            return Negocio.objects.get(pk=pk)
        except Negocio.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        comments = ComentarioEvaluacion.objects.filter(negocio=pk)
        serializer = ComentarioEvaluacionSerializer(comments, many=True)
        stars_average = list(comments.aggregate(average=Round(Avg('rating'), 2)).values())[0]
        return Response({'list_comments': serializer.data, 'evaluacion': stars_average}, status=HTTP_200_OK)
