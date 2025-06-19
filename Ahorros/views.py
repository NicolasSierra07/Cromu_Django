from rest_framework import generics
from .models import Ahorro, PagoMensual
from .serializers import AhorroSerializer, PagoMensualSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404, HttpResponse
from datetime import date
import io
import base64
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Usar backend para servidores
from matplotlib import pyplot as plt

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

####################################################################

@login_required
def ahorros_dashboard(request):
    user = request.user
    if user.is_superuser:
        ahorros = Ahorro.objects.select_related('nombre').all()
    else:
        ahorros = Ahorro.objects.select_related('nombre').filter(nombre=user)
    return render(request, 'ahorros/ahorros.html', {'ahorros': ahorros})

@login_required
def detalle_ahorro(request, pk):
    try:
        if request.user.is_superuser:
            ahorro = Ahorro.objects.get(pk=pk)
        else:
            ahorro = Ahorro.objects.get(pk=pk, nombre=request.user)
    except Ahorro.DoesNotExist:
        raise Http404("El ahorro no existe o no tienes permiso.")

    pagos = ahorro.pagos.all().order_by('-año', '-mes')

    # Generar gráfico personalizado para este ahorro
    pagos_filtrados = pagos.filter(pagado=True)
    datos = [{'mes': p.mes, 'año': p.año} for p in pagos_filtrados]
    df = pd.DataFrame(datos)
    grafico_base64 = None

    if not df.empty:
        df['mes'] = pd.Categorical(df['mes'], categories=[
            'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ], ordered=True)
        resumen = df.groupby('mes').size().reindex(df['mes'].cat.categories, fill_value=0)

        plt.figure(figsize=(8, 4))
        resumen.plot(kind='bar', color='skyblue')
        plt.title("Pagos realizados")
        plt.xlabel("Mes")
        plt.ylabel("Cantidad")
        plt.xticks(rotation=45)
        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)
        grafico_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return render(request, 'ahorros/detalle.html', {
        'ahorro': ahorro,
        'pagos': pagos,
        'grafico_base64': grafico_base64
    })

@user_passes_test(lambda u: u.is_superuser)
@login_required
def crear_ahorro(request):
    if request.method == 'POST':
        descripcion = request.POST.get('descripcion')
        monto = request.POST.get('monto')
        usuario_id = request.POST.get('usuario')

        if descripcion and monto and usuario_id:
            usuario = User.objects.get(id=usuario_id)
            ahorro = Ahorro(nombre=usuario, descripcion=descripcion, monto=monto)
            ahorro.save()
            return redirect('ahorros_dashboard')

    usuarios = User.objects.all()
    return render(request, 'ahorros/crear_ahorro.html', {'usuarios': usuarios})

##############################################################################################

@login_required
def crear_pago(request, ahorro_id):
    ahorro = Ahorro.objects.get(id=ahorro_id)

    if not request.user.is_superuser and ahorro.nombre != request.user:
        return redirect('ahorros_dashboard')

    if request.method == 'POST':
        mes = request.POST.get('mes')
        año = request.POST.get('año')
        pagado = 'pagado' in request.POST
        fecha_pago = date.today() if pagado else None

        PagoMensual.objects.create(
            ahorro=ahorro,
            mes=mes,
            año=año,
            pagado=pagado,
            fecha_pago=fecha_pago
        )
        return redirect('detalle_ahorro', pk=ahorro.id)

    meses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    return render(request, 'ahorros/crear_pago.html', {'ahorro': ahorro, 'meses': meses})

###############################################################################################

@login_required
def grafico_pagos_ahorros(request):
    if request.user.is_superuser:
        pagos = PagoMensual.objects.filter(pagado=True)
    else:
        pagos = PagoMensual.objects.filter(ahorro__nombre=request.user, pagado=True)

    datos = [{'mes': pago.mes, 'año': pago.año} for pago in pagos]
    df = pd.DataFrame(datos)

    if df.empty:
        return HttpResponse("No hay pagos registrados para mostrar un gráfico.")

    df['mes'] = pd.Categorical(df['mes'], categories=[
        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ], ordered=True)

    resumen = df.groupby('mes').size().reindex(df['mes'].cat.categories, fill_value=0)

    plt.figure(figsize=(10, 5))
    resumen.plot(kind='bar', color='skyblue')
    plt.title("Pagos Realizados - Ahorros")
    plt.xlabel("Mes")
    plt.ylabel("Número de pagos")
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type='image/png')
