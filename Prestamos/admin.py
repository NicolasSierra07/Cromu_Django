from django.contrib import admin
from .models import Prestamo, PagoCuota

class PrestamoAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(nombre=request.user)

class PagoCuotaAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(prestamo__nombre=request.user)

admin.site.register(Prestamo, PrestamoAdmin)
admin.site.register(PagoCuota, PagoCuotaAdmin)