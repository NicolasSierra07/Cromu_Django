from rest_framework import serializers
from .models import Ahorro, PagoMensual

class AhorroSerializer(serializers.ModelSerializer):
    nombre = serializers.StringRelatedField()

    class Meta:
        model = Ahorro
        fields = '__all__'
        read_only_fields = ['fecha_creacion']

class PagoMensualSerializer(serializers.ModelSerializer):
    ahorro = serializers.StringRelatedField()
    
    class Meta:
        model = PagoMensual
        fields = '__all__'