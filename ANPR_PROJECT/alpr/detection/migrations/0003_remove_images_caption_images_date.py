# Generated by Django 4.2 on 2023-04-18 05:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('detection', '0002_remove_images_image_desc_images_caption'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='images',
            name='caption',
        ),
        migrations.AddField(
            model_name='images',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
