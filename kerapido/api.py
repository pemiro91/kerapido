from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED
)

from kerapido.models import Reservacion_Generada, Plato, User, Agrego, Tarifa
from kerapido.serializers import ReservacionGeneradaSerializer, PlatoSerializer, NegocioSerializer, AgregoSerializer, \
    TarifaSerializer, UserSerializer


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
        return Response({'error': 'Please provide both username and password'}, status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    context = {'token': token.key, 'usuario': {'id': user.id, 'username': user.username}}
    return Response(context, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
def getNegociosApi(request):
    negocio = User.objects.filter(is_negocio=True)
    serializer = NegocioSerializer(negocio, many=True)
    return Response({'list_business': serializer.data}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
def getPlatoApi(request, pk):
    plato = Plato.objects.filter(negocio=pk)
    serializer = PlatoSerializer(plato, many=True)
    return Response({'list_dishes': serializer.data}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
def getAgregoApi(request, pk):
    agrego = Agrego.objects.filter(negocio=pk)
    serializer = AgregoSerializer(agrego, many=True)
    return Response(serializer.data, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def postReservaApi(request):
    serializer = ReservacionGeneradaSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'message': 'Reserva realizada satisfactoriamente'}, status=HTTP_201_CREATED)


@csrf_exempt
@api_view(["GET"])
def getReservasApiForID(request, pk):
    reservas = Reservacion_Generada.objects.filter(cliente_auth=pk)
    serializer = ReservacionGeneradaSerializer(reservas, many=True)
    return Response({'list_reservas': serializer.data}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
def getTarifaApiForID(request, pk):
    tarifas = Tarifa.objects.filter(negocio=pk)
    serializer = TarifaSerializer(tarifas, many=True)
    return Response({'list_tarifas': serializer.data}, status=HTTP_200_OK)
