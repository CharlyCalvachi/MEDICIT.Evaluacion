# Generated by Django 5.0.6 on 2024-07-05 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicitas', '0006_medico_foto_perfil_medico_sexo_paciente_foto_perfil_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medico',
            old_name='especialidades',
            new_name='especialidad',
        ),
        migrations.RemoveField(
            model_name='citamedica',
            name='especialidad',
        ),
        migrations.AddField(
            model_name='citamedica',
            name='especialidad',
            field=models.ManyToManyField(to='medicitas.especialidad'),
        ),
    ]
