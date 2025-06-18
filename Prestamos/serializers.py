from rest_framework import serializers
from .models import Prestamo, PagoCuota

class PrestamoSerializer(serializers.ModelSerializer):
    nombre = serializers.StringRelatedField()

    class Meta:
        model = Prestamo
        fields = '__all__'
        read_only_fields = ['fecha_creacion']
    
class PagoCuotaSerializer(serializers.ModelSerializer):
    prestamo = serializers.StringRelatedField()

    class Meta:
        model = PagoCuota
        fields = '__all__'
        read_only_fields = ['fecha_pago']