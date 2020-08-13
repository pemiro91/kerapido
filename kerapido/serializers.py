from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from kerapido.models import Reservacion_Generada, Reservacion_Simple, Producto, User, Categoria_Producto, Servicio, \
    ComentarioEvaluacion, Tarifa_Entrega, Negocio


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'password', 'telefono', 'is_cliente')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_cliente = True
        user.save()
        return user


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'


class NegocioSerializer(WritableNestedModelSerializer):
    servicios = ServicioSerializer(many=True)

    class Meta:
        model = Negocio
        fields = ('afiliado', 'nombre', 'logo', 'portada', 'persona_encargada', 'direccion', 'provincia', 'municipio',
                  'rating', 'first_name', 'email', 'is_negocio', 'telefono1', 'telefono2', 'horario', 'servicios')


class ComentarioEvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComentarioEvaluacion
        fields = '__all__'


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'


class Categoria_ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria_Producto
        fields = '__all__'





class Tarifa_EntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarifa_Entrega
        fields = '__all__'


class ReservacionSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservacion_Simple
        fields = '__all__'


class ReservacionGeneradaSerializer(WritableNestedModelSerializer):
    reservaciones = ReservacionSimpleSerializer(many=True)

    class Meta:
        model = Reservacion_Generada
        fields = ('cliente_auth', 'total', 'cliente_entrega', 'telefono_entrega', 'direccion_entrega', 'reservaciones')
