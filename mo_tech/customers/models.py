from django.db import models


class Customer(models.Model):
    class CustomerStatus(models.IntegerChoices):
        ACTIVE = 1
        INACTIVE = 2

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=60, unique=True)
    status = models.SmallIntegerField(
        choices=CustomerStatus.choices, default=CustomerStatus.ACTIVE
    )
    score = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    preapproved_at = models.DateTimeField(null=True, blank=True)
