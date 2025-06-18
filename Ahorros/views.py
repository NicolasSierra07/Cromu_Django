from rest_framework import generics
from .models import Ahorro, PagoMensual
from .serializers import AhorroSerializer, PagoMensualSerializer

class AhorroListCreateView(generics.ListCreateAPIView):
    serializer_class = AhorroSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Ahorro.objects.all()
        return Ahorro.objects.filter(nombre=user)

    def perform_create(self, serializer):
        serializer.save(nombre=self.request.user)

class AhorroDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AhorroSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Ahorro.objects.all()
        return Ahorro.objects.filter(nombre=user)

####################################################################################

class PagoMensualListCreateView(generics.ListCreateAPIView):
    serializer_class = PagoMensualSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return PagoMensual.objects.all()
        return PagoMensual.objects.filter(ahorro__nombre=user)

class PagoMensualDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PagoMensualSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return PagoMensual.objects.all()
        return PagoMensual.objects.filter(ahorro__nombre=user)
