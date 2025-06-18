from django.urls import path
from .views import PrestamoListCreateView, PrestamoDetailView, PagoCuotaListCreateView, PagoCuotaDetailView

urlpatterns = [
    path('prestamos/', PrestamoListCreateView.as_view(), name='prestamo-list-create'),
    path('prestamos/<int:pk>/', PrestamoDetailView.as_view(), name='prestamo-detail'),
    path('pagos/', PagoCuotaListCreateView.as_view(), name='pago-list-create'),
    path('pagos/<int:pk>/', PagoCuotaDetailView.as_view(), name='pago-detail'),
]