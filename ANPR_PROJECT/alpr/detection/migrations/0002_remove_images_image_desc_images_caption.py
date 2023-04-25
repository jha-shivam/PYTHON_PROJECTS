# Generated by Django 4.1.7 on 2023-03-21 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("detection", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="images",
            name="image_desc",
        ),
        migrations.AddField(
            model_name="images",
            name="caption",
            field=models.CharField(default="Your caption here", max_length=200),
        ),
    ]