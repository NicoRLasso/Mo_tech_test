from django.db.models import Sum
from rest_framework import serializers

from .models import Payment
from .models import PaymentDetail
from .services import PaymentService


class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetail
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    customer_external_id = serializers.CharField(source="customer.external_id")
    payment_date = serializers.DateTimeField(source="paid_at")
    payment_amount = serializers.SerializerMethodField()
    details = PaymentDetailSerializer(source="paymentdetail_set", many=True)

    class Meta:
        model = Payment
        fields = [
            "external_id",
            "customer_external_id",
            "details",
            "payment_date",
            "status",
            "total_amount",
            "payment_amount",
        ]

    def create(self, validated_data):
        payment_service = PaymentService(data=self.initial_data)
        return payment_service.create_payment()

    def get_payment_amount(self, obj) -> float:
        total_amount = PaymentDetail.objects.filter(payment=obj).aggregate(
            sum_amount=Sum("amount")
        )["sum_amount"]
        return total_amount or 0
