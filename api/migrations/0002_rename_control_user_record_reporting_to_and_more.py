# Generated by Django 4.2.3 on 2024-01-25 06:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user_record",
            old_name="control",
            new_name="reporting_to",
        ),
        migrations.AddField(
            model_name="user_record",
            name="procurement",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user_record",
            name="quality",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user_record",
            name="sales_tracker",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user_record",
            name="user_management",
            field=models.BooleanField(default=False),
        ),
    ]
