# Generated by Django 3.0.5 on 2024-09-15 21:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aplications', '0017_screenshot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='designtest',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplications.User'),
        ),
    ]
