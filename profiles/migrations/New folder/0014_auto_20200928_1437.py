# Generated by Django 3.0.3 on 2020-09-28 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0013_auto_20200925_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]
