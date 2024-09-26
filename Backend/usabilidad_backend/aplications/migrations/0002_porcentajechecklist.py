# Generated by Django 3.0.5 on 2024-06-04 21:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aplications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PorcentajeCheckList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rol', models.CharField(max_length=50)),
                ('suma_si', models.IntegerField(blank=True, null=True)),
                ('suma_no', models.IntegerField(blank=True, null=True)),
                ('porcentaje_si', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('porcentaje_no', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('user_username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplications.User')),
            ],
        ),
    ]