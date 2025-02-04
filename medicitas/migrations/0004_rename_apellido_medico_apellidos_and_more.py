# Generated by Django 5.0.6 on 2024-07-04 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicitas', '0003_remove_medico_especialidad_medico_especialidades'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medico',
            old_name='apellido',
            new_name='apellidos',
        ),
        migrations.RenameField(
            model_name='medico',
            old_name='nombre',
            new_name='nombres',
        ),
        migrations.RenameField(
            model_name='paciente',
            old_name='apellido',
            new_name='apellidos',
        ),
        migrations.RenameField(
            model_name='paciente',
            old_name='nombre',
            new_name='nombres',
        ),
        migrations.RenameField(
            model_name='personal',
            old_name='apellido',
            new_name='apellidos',
        ),
        migrations.RenameField(
            model_name='personal',
            old_name='nombre',
            new_name='nombres',
        ),
        migrations.AddField(
            model_name='medico',
            name='num_documento',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='medico',
            name='tipo_documento',
            field=models.CharField(choices=[('cedula', 'Cédula'), ('pasaporte', 'Pasaporte')], default='cedula', max_length=10),
        ),
        migrations.AddField(
            model_name='personal',
            name='num_documento',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='personal',
            name='tipo_documento',
            field=models.CharField(choices=[('cedula', 'Cédula'), ('pasaporte', 'Pasaporte')], default='cedula', max_length=10),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='num_documento',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='tipo_documento',
            field=models.CharField(choices=[('cedula', 'Cédula'), ('pasaporte', 'Pasaporte')], default='cedula', max_length=10),
        ),
    ]
