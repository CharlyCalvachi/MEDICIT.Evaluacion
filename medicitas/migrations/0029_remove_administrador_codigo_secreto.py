# Generated by Django 5.0.6 on 2024-12-26 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medicitas', '0028_administrador_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='administrador',
            name='codigo_secreto',
        ),
    ]
