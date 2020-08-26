from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from kerapido.models import Reservacion_Generada, Reservacion_Simple, Producto, User, Categoria_Producto, Servicio, \
    ComentarioEvaluacion, Tarifa_Entrega, Negocio


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',  'password', 'telefono', 'is_cliente')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_cliente = True
        user.is_active = False
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
        fields = ('usuario_negocio', 'nombre', 'logo', 'portada', 'slogan', 'direccion', 'provincia', 'municipio',
                  'telefono1', 'telefono2', 'horario', 'servicios', 'rating')


class ComentarioEvaluacionSerializer(serializers.ModelSerializer):
    cliente_username = serializers.ReadOnlyField(source='cliente.username')

    class Meta:
        model = ComentarioEvaluacion
        read_only_fields = ('id', 'cliente_username')
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
