# Generated by Django 3.0.5 on 2024-09-04 04:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aplications', '0010_auto_20240903_2245'),
    ]

    operations = [
        migrations.RenameField(
            model_name='designquestion',
            old_name='test',
            new_name='test_id',
        ),
    ]
