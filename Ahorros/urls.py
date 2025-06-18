from django.urls import path
from .views import AhorroListCreateView, AhorroDetailView, PagoMensualListCreateView, PagoMensualDetailView

urlpatterns = [
    path('ahorros/', AhorroListCreateView.as_view(), name='ahorro-list-create'),
    path('ahorros/<int:pk>/', AhorroDetailView.as_view(), name='ahorro-detail'),

    path('pagos/', PagoMensualListCreateView.as_view(), name='pago-list-create'),
    path('pagos/<int:pk>/', PagoMensualDetailView.as_view(), name='pago-detail'),
]