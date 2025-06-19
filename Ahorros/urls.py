from django.urls import path
from .views import AhorroListCreateView, AhorroDetailView, PagoMensualListCreateView, PagoMensualDetailView, ahorros_dashboard, detalle_ahorro, crear_ahorro, crear_pago, grafico_pagos_ahorros

urlpatterns = [
    path('ahorros/', AhorroListCreateView.as_view(), name='ahorro-list-create'),
    path('ahorros/<int:pk>/', AhorroDetailView.as_view(), name='ahorro-detail'),

    path('pagos/', PagoMensualListCreateView.as_view(), name='pago-list-create'),
    path('pagos/<int:pk>/', PagoMensualDetailView.as_view(), name='pago-detail'),

    path('', ahorros_dashboard, name='ahorros_dashboard'),
    path('<int:pk>/', detalle_ahorro, name='detalle_ahorro'),
    path('crear/', crear_ahorro, name='crear_ahorro'),
    path('<int:ahorro_id>/pago/', crear_pago, name='crear_pago'),
    path('vista/grafico-ahorros/', grafico_pagos_ahorros, name='grafico_ahorros'),
]