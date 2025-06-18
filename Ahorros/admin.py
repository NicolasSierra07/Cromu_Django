from django.contrib import admin
from .models import Ahorro, PagoMensual

class AhorroAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(nombre=request.user)
    
class PagoMensualAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(ahorro__nombre=request.user)

admin.site.register(Ahorro, AhorroAdmin)
admin.site.register(PagoMensual, PagoMensualAdmin)
