# Generated by Django 4.2.6 on 2023-10-18 20:31
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("customers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Loan",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("external_id", models.CharField(max_length=60, unique=True)),
                (
                    "amount",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
                ),
                (
                    "status",
                    models.SmallIntegerField(
                        choices=[
                            (1, "Pending"),
                            (2, "Active"),
                            (3, "Rejected"),
                            (4, "Paid"),
                        ],
                        default=1,
                    ),
                ),
                ("contract_version", models.CharField(default="1.0", max_length=60)),
                ("maximum_payment_date", models.DateTimeField()),
                ("taken_at", models.DateTimeField()),
                (
                    "outstanding",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="customers.customer",
                    ),
                ),
            ],
        ),
    ]
