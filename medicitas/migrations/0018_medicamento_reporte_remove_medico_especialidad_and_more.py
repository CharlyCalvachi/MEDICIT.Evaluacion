# Generated by Django 5.0.6 on 2024-12-17 04:22

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicitas', '0017_alter_historialmedico_citas'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, unique=True)),
                ('descripcion', models.TextField()),
                ('dosis_recomendada', models.CharField(max_length=100)),
                ('efectos_secundarios', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('estadistico', 'Estadístico'), ('enfermedades', 'Enfermedades Comunes'), ('desempeño_medico', 'Desempeño Médico')], max_length=30)),
                ('fecha_generacion', models.DateTimeField(auto_now_add=True)),
                ('datos', models.JSONField()),
                ('archivo', models.FileField(blank=True, null=True, upload_to='reportes/')),
            ],
        ),
        migrations.RemoveField(
            model_name='medico',
            name='especialidad',
        ),
        migrations.AddField(
            model_name='citamedica',
            name='estado',
            field=models.CharField(choices=[('programada', 'Programada'), ('confirmada', 'Confirmada'), ('realizada', 'Realizada'), ('cancelada', 'Cancelada')], default='programada', max_length=20),
        ),
        migrations.AddField(
            model_name='historialmedico',
            name='fecha_diagnostico',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='medico',
            name='especialidades',
            field=models.ManyToManyField(related_name='medicos', to='medicitas.especialidad'),
        ),
        migrations.AddField(
            model_name='medico',
            name='horario_atencion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medico',
            name='usuario',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paciente',
            name='usuario',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='personal',
            name='usuario',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='citamedica',
            name='medico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='citas', to='medicitas.medico'),
        ),
        migrations.AlterField(
            model_name='citamedica',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='citas', to='medicitas.paciente'),
        ),
        migrations.AlterField(
            model_name='especialidad',
            name='nombre',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='historialmedico',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historiales', to='medicitas.paciente'),
        ),
        migrations.AlterField(
            model_name='historialmedico',
            name='unidad_estatura',
            field=models.CharField(choices=[('metros', 'Metros'), ('pulgadas', 'Pulgadas')], default='metros', max_length=10),
        ),
        migrations.AlterField(
            model_name='historialmedico',
            name='unidad_peso',
            field=models.CharField(choices=[('libras', 'Libras'), ('kilos', 'Kilos')], default='libras', max_length=10),
        ),
        migrations.AlterField(
            model_name='medico',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='medico',
            name='num_documento',
            field=models.CharField(max_length=20, unique=True, validators=[django.core.validators.RegexValidator(message='Solo se permiten números en el número de documento', regex='^\\d+$')]),
        ),
        migrations.AlterField(
            model_name='medico',
            name='telefono',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Número de teléfono inválido', regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='num_documento',
            field=models.CharField(max_length=20, unique=True, validators=[django.core.validators.RegexValidator(message='Solo se permiten números en el número de documento', regex='^\\d+$')]),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='telefono',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Número de teléfono inválido', regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AlterField(
            model_name='personal',
            name='email',
            field=models.EmailField(default='', max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='personal',
            name='num_documento',
            field=models.CharField(max_length=20, unique=True, validators=[django.core.validators.RegexValidator(message='Solo se permiten números en el número de documento', regex='^\\d+$')]),
        ),
        migrations.AlterField(
            model_name='personal',
            name='telefono',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Número de teléfono inválido', regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.CreateModel(
            name='FormularioSatisfaccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calificacion_general', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comentarios', models.TextField(blank=True, null=True)),
                ('fecha_completado', models.DateTimeField(auto_now_add=True)),
                ('cita', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='medicitas.citamedica')),
            ],
        ),
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('cita', 'Cita'), ('examen', 'Examen'), ('recordatorio', 'Recordatorio'), ('otro', 'Otro')], max_length=20)),
                ('mensaje', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('leida', models.BooleanField(default=False)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificaciones', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Receta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dosis', models.CharField(max_length=100)),
                ('frecuencia', models.CharField(max_length=100)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('estado', models.CharField(choices=[('activa', 'Activa'), ('completada', 'Completada'), ('cancelada', 'Cancelada')], default='activa', max_length=20)),
                ('historial_medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recetas', to='medicitas.historialmedico')),
                ('medicamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicitas.medicamento')),
            ],
        ),
    ]
