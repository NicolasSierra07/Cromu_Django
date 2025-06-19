from django.urls import path
from .views import PrestamoListCreateView, PrestamoDetailView, PagoCuotaListCreateView, PagoCuotaDetailView, prestamos_dashboard, detalle_prestamo, crear_prestamo, crear_cuota, grafico_pagos_prestamos

urlpatterns = [
    path('prestamos/', PrestamoListCreateView.as_view(), name='prestamo-list-create'),
    path('prestamos/<int:pk>/', PrestamoDetailView.as_view(), name='prestamo-detail'),
    path('pagos/', PagoCuotaListCreateView.as_view(), name='pago-list-create'),
    path('pagos/<int:pk>/', PagoCuotaDetailView.as_view(), name='pago-detail'),

    path('vista/prestamos/', prestamos_dashboard, name='vista_prestamos'),
    path('vista/prestamos/<int:pk>/', detalle_prestamo, name='vista_prestamo_detalle'),
    path('vista/prestamos/nuevo/', crear_prestamo, name='vista_prestamo_crear'),
    path('vista/prestamos/<int:prestamo_id>/cuota/', crear_cuota, name='vista_cuota_crear'),
    path('vista/grafico-prestamos/', grafico_pagos_prestamos, name='grafico_prestamos'),
]