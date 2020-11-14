# Generated by Django 3.0.3 on 2020-10-28 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0033_auto_20201027_0533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='upload_images/profile1.PNG', upload_to='upload_images'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image2',
            field=models.ImageField(default='upload_images/profile2.PNG', upload_to='upload_images'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image3',
            field=models.ImageField(default='upload_images/profile3.PNG', upload_to='upload_images'),
        ),
    ]
