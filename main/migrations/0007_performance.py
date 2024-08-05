# Generated by Django 5.0.7 on 2024-08-04 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0006_rename_header_headerimage"),
    ]

    operations = [
        migrations.CreateModel(
            name="Performance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("year", models.DateField(auto_now=True)),
                ("video_url", models.FileField(upload_to="performance_videos")),
                ("content", models.CharField(max_length=255, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
