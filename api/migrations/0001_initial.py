# Generated by Django 4.2.3 on 2024-02-20 07:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
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
        migrations.CreateModel(
            name="AckMail",
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
                ("email_body", models.FileField(upload_to="file")),
                ("attachment", models.FileField(upload_to="file")),
                ("plain_text", models.TextField()),
                ("sales_person_name", models.TextField()),
                ("client_person_name", models.TextField()),
                ("quotation_time", models.TextField()),
                ("quotation_to", models.TextField()),
                ("quotation_from", models.TextField()),
                ("quotation_subject", models.TextField()),
                ("quotation_plain_body", models.TextField()),
                ("quotation_html_body", models.FileField(upload_to="file")),
                ("quotation_attachment", models.FileField(upload_to="file")),
                ("total_order_value", models.CharField(max_length=255)),
                ("currency", models.CharField(max_length=255)),
                ("currency_value", models.CharField(max_length=255)),
                ("reminder_status", models.CharField(max_length=255)),
                ("ack_time", models.CharField(max_length=255)),
                ("order_ageing", models.DateField(blank=True)),
                ("order_date_time", models.DateTimeField(blank=True)),
                ("order_closure_days", models.DateTimeField(blank=True)),
                ("order_value", models.DateTimeField(blank=True)),
                ("order_email_attachment", models.DateTimeField(blank=True)),
            ],
        ),
    ]
