# Generated by Django 4.2.3 on 2024-04-10 03:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ack_mail",
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
                ("reference_number", models.CharField(max_length=255)),
                ("sales_mail", models.CharField(max_length=255)),
                ("sales_email_time", models.CharField(max_length=255)),
                ("client_email", models.CharField(max_length=255)),
                ("client_email_time", models.CharField(max_length=255)),
                ("client_cc", models.TextField()),
                ("client_subject", models.CharField(max_length=255)),
                ("email_body", models.BinaryField()),
                ("attachment", models.BinaryField()),
                ("plain_text", models.TextField()),
                ("sales_person_name", models.TextField()),
                ("client_person_name", models.TextField()),
                ("quotation_time", models.TextField()),
                ("quotation_to", models.TextField()),
                ("quotation_from", models.TextField()),
                ("quotation_subject", models.TextField()),
                ("quotation_plain_body", models.TextField()),
                ("quotation_html_body", models.BinaryField()),
                ("quotation_attachment", models.BinaryField()),
                ("total_order_value", models.CharField(max_length=255)),
                ("currency", models.CharField(max_length=255)),
                ("currency_value", models.CharField(max_length=255)),
                ("reminder_status", models.CharField(max_length=255)),
                ("ack_time", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "ack_mail",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="User_record",
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
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("user", models.CharField(max_length=100, unique=True)),
                ("password", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("role_name", models.CharField(max_length=50)),
                (
                    "created_date",
                    models.DateTimeField(
                        blank=True,
                        default=django.utils.timezone.now,
                        editable=False,
                        null=True,
                    ),
                ),
                ("reporting_to", models.CharField(max_length=50)),
                ("sales_tracker", models.BooleanField(default=False)),
                ("user_management", models.BooleanField(default=False)),
                ("quality", models.BooleanField(default=False)),
                ("procurement", models.BooleanField(default=False)),
                ("quote_generator", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
