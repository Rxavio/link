# Generated by Django 3.0.3 on 2020-10-07 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0025_auto_20201007_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='category',
            field=models.CharField(choices=[('YAC', 'AC'), ('NAC', 'NON-AC'), ('DEL', 'DELUXE'), ('KIN', 'KING'), ('QUE', 'QUEEN')], max_length=3, unique=True),
        ),
    ]
