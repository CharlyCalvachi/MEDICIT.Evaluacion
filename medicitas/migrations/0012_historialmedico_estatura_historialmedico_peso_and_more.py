# Generated by Django 5.0.6 on 2024-07-05 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicitas', '0011_alter_historialmedico_num_identificacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='historialmedico',
            name='estatura',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historialmedico',
            name='peso',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historialmedico',
            name='num_identificacion',
            field=models.CharField(max_length=20),
        ),
    ]
