from rest_framework import generics
from .models import Prestamo, PagoCuota
from .serializers import PrestamoSerializer, PagoCuotaSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
import datetime
import io
import pandas as pd
from django.http import HttpResponse, HttpResponseForbidden
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Agg')
import base64


###################################################################################

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

#####################################################################################

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

######################################################################################

@login_required
def prestamos_dashboard(request):
    if request.user.is_superuser:
        prestamos = Prestamo.objects.all()
    else:
        prestamos = Prestamo.objects.filter(nombre=request.user)
    return render(request, 'prestamos/prestamos.html', {'prestamos': prestamos})

@login_required
def detalle_prestamo(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    if not request.user.is_superuser and prestamo.nombre != request.user:
        return HttpResponseForbidden("No tienes permiso para ver este préstamo.")

    cuotas = prestamo.cuotas.all().order_by('-año', '-mes')

    # Generar gráfico específico para este préstamo
    datos = [{'mes': cuota.mes, 'año': cuota.año} for cuota in cuotas if cuota.pagado]
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
        plt.title("Pagos Realizados para este Préstamo")
        plt.xlabel("Mes")
        plt.ylabel("Cantidad de pagos")
        plt.xticks(rotation=45)
        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        grafico_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()
        plt.close()

    return render(request, 'prestamos/detalle_prestamo.html', {
        'prestamo': prestamo,
        'cuotas': cuotas,
        'grafico_base64': grafico_base64
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def crear_prestamo(request):
    if request.method == 'POST':
        descripcion = request.POST.get('descripcion')
        monto = request.POST.get('monto')
        cantidad_meses = request.POST.get('cantidad_meses')
        usuario_id = request.POST.get('usuario')

        if descripcion and monto and cantidad_meses and usuario_id:
            usuario = User.objects.get(id=usuario_id)
            prestamo = Prestamo(
                nombre=usuario,
                descripcion=descripcion,
                monto=float(monto),
                cantidad_meses=int(cantidad_meses)
            )
            prestamo.save()
            return redirect('vista_prestamos')

    usuarios = User.objects.all()
    return render(request, 'prestamos/crear_prestamo.html', {'usuarios': usuarios})

##############################################################################

@user_passes_test(lambda u: u.is_superuser)
@login_required
def crear_cuota(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    current_year = datetime.date.today().year

    if request.method == 'POST':
        mes = request.POST.get('mes')
        anio = request.POST.get('año')
        pagado = True if request.POST.get('pagado') == 'on' else False

        if mes and anio:
            cuota = PagoCuota(prestamo=prestamo, mes=mes, año=anio, pagado=pagado)
            cuota.save()
            return redirect('vista_prestamo_detalle', prestamo_id)

    return render(request, 'prestamos/crear_cuota.html', {
        'prestamo': prestamo,
        'meses': meses,
        'current_year': current_year
    })

###############################################################################################

@login_required
def grafico_pagos_prestamos(request):
    if request.user.is_superuser:
        pagos = PagoCuota.objects.filter(pagado=True)
    else:
        pagos = PagoCuota.objects.filter(prestamo__nombre=request.user, pagado=True)

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
    resumen.plot(kind='bar', color='lightgreen')
    plt.title("Pagos Realizados - Préstamos")
    plt.xlabel("Mes")
    plt.ylabel("Número de pagos")
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type='image/png')
