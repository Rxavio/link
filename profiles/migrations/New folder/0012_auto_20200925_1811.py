# Generated by Django 3.0.3 on 2020-09-25 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_auto_20200925_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nationalid',
            field=models.CharField(blank=True, max_length=16),
        ),
        migrations.AlterField(
            model_name='profile',
            name='telephone',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]