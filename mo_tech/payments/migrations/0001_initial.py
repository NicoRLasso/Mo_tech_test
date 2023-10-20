# Generated by Django 4.2.6 on 2023-10-18 20:31
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("customers", "0001_initial"),
        ("loans", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
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
                    "total_amount",
                    models.DecimalField(decimal_places=10, default=0.0, max_digits=20),
                ),
                (
                    "status",
                    models.SmallIntegerField(
                        choices=[(1, "Completed"), (2, "Rejected")], default=1
                    ),
                ),
                ("paid_at", models.DateTimeField()),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="customers.customer",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PaymentDetail",
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
                (
                    "amount",
                    models.DecimalField(decimal_places=10, default=0.0, max_digits=20),
                ),
                (
                    "loan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="loans.loan"
                    ),
                ),
                (
                    "payment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="payments.payment",
                    ),
                ),
            ],
        ),
    ]
