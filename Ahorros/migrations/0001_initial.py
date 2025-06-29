# Generated by Django 5.2.3 on 2025-06-18 20:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ahorro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cuota_mensual', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('dinero_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('meses_restantes', models.IntegerField(default=12)),
                ('fecha_creacion', models.DateField(auto_now_add=True, null=True)),
                ('nombre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ahorros', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PagoMensual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.CharField(max_length=20)),
                ('año', models.IntegerField()),
                ('pagado', models.BooleanField(default=False)),
                ('fecha_pago', models.DateField(blank=True, null=True)),
                ('aplicado_interes', models.BooleanField(default=False)),
                ('ahorro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pagos', to='Ahorros.ahorro')),
            ],
        ),
    ]
