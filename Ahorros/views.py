from rest_framework import generics
from .models import Ahorro
from .serializers import AhorroSerializer

class AhorroListCreateView(generics.ListCreateAPIView):
    queryset = Ahorro.objects.all()
    serializer_class = AhorroSerializer

class AhorroDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ahorro.objects.all()
    serializer_class = AhorroSerializer