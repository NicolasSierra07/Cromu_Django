from django.db import models
from django.conf import settings
import numpy as np

class Ahorro(models.Model):
    nombre = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ahorros')
    descripcion = models.TextField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)  # Valor base
    cuota_mensual = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    dinero_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # Valor acumulado con intereses
    meses_restantes = models.IntegerField(default=12)
    fecha_creacion = models.DateField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.cuota_mensual = np.round(float(self.monto) / 12, 2)
            self.dinero_total = self.monto
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} - {self.descripcion} - {self.meses_restantes} meses restantes"

class PagoMensual(models.Model):
    ahorro = models.ForeignKey(Ahorro, on_delete=models.CASCADE, related_name='pagos')
    mes = models.CharField(max_length=20)
    año = models.IntegerField()
    pagado = models.BooleanField(default=False)
    fecha_pago = models.DateField(blank=True, null=True)
    aplicado_interes = models.BooleanField(default=False)  # Marca si ya se sumó el 0.5%

    def save(self, *args, **kwargs):
        # Si el pago es nuevo o acaba de marcarse como pagado
        if not self.pk or (self.pk and not PagoMensual.objects.get(pk=self.pk).pagado and self.pagado):
            if self.pagado and not self.aplicado_interes:
                ahorro = self.ahorro

                # Calcular el 0.5% de interés sobre el monto base
                interes = float(ahorro.monto) * 0.005
                ahorro.dinero_total = np.round(float(ahorro.dinero_total) + interes, 2)

                # Reducir meses restantes
                if ahorro.meses_restantes > 0:
                    ahorro.meses_restantes = int(np.maximum(ahorro.meses_restantes - 1, 0))

                ahorro.save()
                self.aplicado_interes = True

        super().save(*args, **kwargs)

    def __str__(self):
        estado = "Pagado" if self.pagado else "Pendiente"
        return f"{self.ahorro.nombre} - {self.mes} {self.año}: {estado}"
