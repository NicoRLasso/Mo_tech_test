from django.db import models


class Payment(models.Model):
    class PaymentStatus(models.IntegerChoices):
        COMPLETED = 1
        REJECTED = 2

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=60, unique=True)
    total_amount = models.DecimalField(max_digits=20, decimal_places=10, default=0.0)
    status = models.SmallIntegerField(
        choices=PaymentStatus.choices, default=PaymentStatus.COMPLETED
    )
    paid_at = models.DateTimeField()
    customer = models.ForeignKey("customers.Customer", on_delete=models.CASCADE)


class PaymentDetail(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=20, decimal_places=10, default=0.0)
    loan = models.ForeignKey("loans.Loan", on_delete=models.CASCADE)
    payment = models.ForeignKey("payments.Payment", on_delete=models.CASCADE)
