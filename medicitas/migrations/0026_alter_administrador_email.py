# Generated by Django 5.0.6 on 2024-12-26 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicitas', '0025_alter_administrador_email_alter_administrador_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrador',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
