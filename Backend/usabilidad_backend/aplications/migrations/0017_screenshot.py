# Generated by Django 3.0.5 on 2024-09-06 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplications', '0016_auto_20240905_2255'),
    ]

    operations = [
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=500)),
                ('image_path', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]