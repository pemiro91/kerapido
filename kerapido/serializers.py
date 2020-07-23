from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from kerapido.models import Reservacion_Generada, Reservacion_Simple, Plato, User, Agrego, Tarifa, ComentarioEvaluacion


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


class NegocioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('logo', 'persona_encargada', 'telefono', 'direccion', 'especialidad', 'provincia', 'municipio',
                  'rating', 'first_name', 'email', 'is_negocio')


class ComentarioEvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComentarioEvaluacion
        fields = '__all__'


class PlatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plato
        fields = '__all__'


class AgregoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agrego
        fields = '__all__'


class TarifaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarifa
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
