from django.urls import path
from .views import PrestamoListCreateView, PrestamoDetailView

urlpatterns = [
    path('prestamos/', PrestamoListCreateView.as_view(), name='prestamo-list-create'),
    path('prestamos/<int:pk>/', PrestamoDetailView.as_view(), name='prestamo-detail'),
]