from rest_framework import generics
from .models import Prestamo, PagoCuota
from .serializers import PrestamoSerializer, PagoCuotaSerializer

class PrestamoListCreateView(generics.ListCreateAPIView):
    serializer_class = PrestamoSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Prestamo.objects.all()
        return Prestamo.objects.filter(nombre=user)

    def perform_create(self, serializer):
        serializer.save(nombre=self.request.user)

class PrestamoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PrestamoSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Prestamo.objects.all()
        return Prestamo.objects.filter(nombre=user)

#######################################################################################

class PagoCuotaListCreateView(generics.ListCreateAPIView):
    serializer_class = PagoCuotaSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return PagoCuota.objects.all()
        return PagoCuota.objects.filter(prestamo__nombre=user)

class PagoCuotaDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PagoCuotaSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return PagoCuota.objects.all()
        return PagoCuota.objects.filter(prestamo__nombre=user)
