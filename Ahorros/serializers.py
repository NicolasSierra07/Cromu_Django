from rest_framework import serializers
from .models import Ahorro

class AhorroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ahorro
        fields = '__all__'
        read_only_fields = ['fecha_creacion']