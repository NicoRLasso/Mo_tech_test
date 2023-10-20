from django.test import TestCase

from mo_tech.customers.models import Customer
from mo_tech.loans.models import Loan
from mo_tech.payments.models import Payment
from mo_tech.payments.models import PaymentDetail
from mo_tech.payments.serializers import PaymentDetailSerializer
from mo_tech.payments.serializers import PaymentSerializer


class PaymentSerializerTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            external_id="test_external_id", score=100.0, status=1
        )
        self.payment = Payment.objects.create(
            external_id="test_external_id",
            total_amount=1000,
            customer=self.customer,
            paid_at="2023-10-20T12:30:45Z",
        )
        self.loan_data = {
            "external_id": "loan12345",
            "amount": 100.50,
            "status": Loan.LoanStatus.PENDING,
            "contract_version": "1.0",
            "maximum_payment_date": "2023-11-01T12:30:45Z",
            "taken_at": "2023-10-20T12:30:45Z",
            "outstanding": 100.50,
            "customer": self.customer,
        }
        self.loan = Loan.objects.create(**self.loan_data)
        self.payment_detail = PaymentDetail.objects.create(
            amount=500,
            loan=self.loan,
            payment=self.payment,
            created_at="2023-10-20T12:30:45Z",
            updated_at="2023-10-20T12:30:45Z",
        )

    def test_payment_detail_serializer(self):
        serializer = PaymentDetailSerializer(self.payment_detail)
        expected_data = {
            "id": self.payment_detail.id,
            "created_at": self.payment_detail.created_at.strftime(
                "%Y-%m-%dT%H:%M:%S.%fZ"
            ),
            "updated_at": self.payment_detail.updated_at.strftime(
                "%Y-%m-%dT%H:%M:%S.%fZ"
            ),
            "amount": "{:.10f}".format(500),
            "loan": self.loan.id,
            "payment": self.payment.id,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_payment_serializer(self):
        serializer = PaymentSerializer(self.payment)

        expected_data = {
            "external_id": self.payment.external_id,
            "customer_external_id": self.customer.external_id,
            "payment_date": self.payment.paid_at,
            "status": self.payment.status,
            "total_amount": "{:.10f}".format(self.payment.total_amount),
            "payment_amount": serializer.get_payment_amount(self.payment),
            "details": [PaymentDetailSerializer(self.payment_detail).data],
        }

        self.assertEqual(serializer.data, expected_data)
