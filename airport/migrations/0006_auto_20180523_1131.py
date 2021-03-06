# Generated by Django 2.1a1 on 2018-05-23 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('airport', '0005_auto_20180420_1106'),
    ]

    operations = [
        migrations.CreateModel(
            name='AirplaneCrew',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('captainsName', models.CharField(max_length=255)),
                ('captainsSurname', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='airplanecrew',
            unique_together={('captainsName', 'captainsSurname')},
        ),
        migrations.AddField(
            model_name='flight',
            name='crew',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='airport.AirplaneCrew'),
        ),
    ]
