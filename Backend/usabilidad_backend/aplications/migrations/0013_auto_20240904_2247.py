# Generated by Django 3.0.5 on 2024-09-05 03:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aplications', '0012_auto_20240904_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='designtest',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aplications.User'),
        ),
    ]