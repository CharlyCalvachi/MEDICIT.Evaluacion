# Generated by Django 5.0.6 on 2024-07-04 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicitas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
    ]
