# Generated by Django 3.0.5 on 2024-09-04 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplications', '0009_auto_20240903_1436'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='designquestion',
            name='heuristics',
        ),
        migrations.AddField(
            model_name='designquestion',
            name='heuristics',
            field=models.ManyToManyField(blank=True, to='aplications.Heuristic'),
        ),
    ]