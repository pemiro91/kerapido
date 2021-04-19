from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from kerapido.models import Pedido, Reservacion_Simple, Producto, User, Categoria_Producto, Servicio, \
    ComentarioEvaluacion, Tarifa_Entrega, Negocio, Categoria_Negocio, Frecuencia


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'telefono', 'is_cliente')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, )

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'telefono', 'is_cliente',
                  'is_active')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'


class Categoria_NegocioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria_Negocio
        fields = '__all__'


class FrecuenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frecuencia
        fields = '__all__'


class NegocioSerializer(WritableNestedModelSerializer):
    servicios = ServicioSerializer(many=True)
    categorias = Categoria_NegocioSerializer(many=True)
    frecuencia = FrecuenciaSerializer(many=True)

    class Meta:
        model = Negocio
        fields = ('usuario_negocio', 'nombre', 'logo', 'portada', 'eslogan', 'categorias',
                  'servicios', 'horario', 'frecuencia', 'direccion', 'municipio', 'email',
                  'telefono1', 'telefono2', 'rating', 'is_closed')


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
    producto_name = serializers.CharField(source='producto.nombre', required=False)
    producto_imagen = serializers.ImageField(source='producto.imagen', required=False)
    producto_precio = serializers.FloatField(source='producto.precio', required=False)

    class Meta:
        model = Reservacion_Simple
        fields = ('id', 'cantidad_producto', 'producto', 'producto_name', 'producto_imagen', 'producto_precio')


class PedidoSerializer(WritableNestedModelSerializer):
    reservaciones = ReservacionSimpleSerializer(many=True)
    negocio_logo = serializers.ImageField(source='negocio.logo', required=False)
    negocio_name = serializers.CharField(source='negocio.nombre', required=False)
    tarifa_precio = serializers.FloatField(source='tarifa.precio', required=False)
    tarifa_lugar_destino = serializers.CharField(source='tarifa.lugar_destino', required=False)

    class Meta:
        model = Pedido
        fields = ('negocio', 'negocio_logo', 'cliente_auth', 'total_pagar', 'cliente_entrega', 'telefono_entrega',
                  'porciento_pagar',
                  'tarifa', 'tarifa_precio', 'tarifa_lugar_destino', 'servicio', 'direccion_entrega',
                  'total_pagar_user',
                  'estado', 'negocio_name', 'reservaciones')
