from django.urls import path
from .views import AhorroListCreateView, AhorroDetailView

urlpatterns = [
    path('ahorros/', AhorroListCreateView.as_view(), name='ahorro-list-create'),
    path('ahorros/<int:pk>/', AhorroDetailView.as_view(), name='ahorro-detail'),
]