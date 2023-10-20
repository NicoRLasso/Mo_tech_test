from django.db import models


class Loan(models.Model):
    class LoanStatus(models.IntegerChoices):
        PENDING = 1
        ACTIVE = 2
        REJECTED = 3
        PAID = 4

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=60, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    status = models.SmallIntegerField(
        choices=LoanStatus.choices, default=LoanStatus.PENDING
    )
    contract_version = models.CharField(max_length=60, default="1.0")
    maximum_payment_date = models.DateTimeField()
    taken_at = models.DateTimeField()
    customer = models.ForeignKey("customers.Customer", on_delete=models.CASCADE)
    outstanding = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
