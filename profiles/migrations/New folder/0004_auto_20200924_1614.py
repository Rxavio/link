# Generated by Django 3.0.3 on 2020-09-24 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20200924_1528'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='avatar',
            new_name='image',
        ),
    ]