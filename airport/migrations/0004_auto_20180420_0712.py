# Generated by Django 2.0.4 on 2018-04-20 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('airport', '0003_flight_airplane'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='airplane',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airport.Airplane'),
        ),
    ]
