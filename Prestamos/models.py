from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
import numpy as np

class Prestamo(models.Model):
    nombre = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prestamos')
    descripcion = models.TextField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_meses = models.IntegerField(default=12)
    cuota_mensual = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        # Solo calcular cuota si el objeto es nuevo (no tiene PK aún)
        if not self.pk and self.cantidad_meses > 0:
            self.cuota_mensual = np.round(float(self.monto) / self.cantidad_meses, 2)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nombre} - {self.fecha_creacion.strftime('%B %d, %Y')} - {self.cantidad_meses} meses restantes"

#######################################################################################

class PagoCuota(models.Model):
    prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE, related_name='cuotas')
    mes = models.CharField(max_length=20)
    año = models.IntegerField()
    pagado = models.BooleanField(default=False)
    fecha_pago = models.DateField(blank=True, null=True)

    def monto_a_pagar(self):
        return self.prestamo.cuota_mensual

    def save(self, *args, **kwargs):
        if self.pk:
            old = PagoCuota.objects.get(pk=self.pk)
            if not old.pagado and self.pagado:
                self.restar_mes()
                if not self.fecha_pago:
                    self.fecha_pago = timezone.now().date()
        elif self.pagado:
            self.restar_mes()
            if not self.fecha_pago:
                self.fecha_pago = timezone.now().date()

        super().save(*args, **kwargs)

    def restar_mes(self):
        prestamo = self.prestamo
        prestamo.cantidad_meses = int(np.maximum(prestamo.cantidad_meses - 1, 0))
        prestamo.save()

    def __str__(self):
        estado = "Pagado" if self.pagado else "Pendiente"
        return f"{self.prestamo.nombre} - {self.mes} {self.año}: {estado}"
