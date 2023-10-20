from django.test import TestCase

from mo_tech.customers.models import Customer
from mo_tech.loans.models import Loan
from mo_tech.payments.models import Payment
from mo_tech.payments.models import PaymentDetail


class PaymentModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            external_id="test_external_id", score=100.0, status=1
        )

    def test_create_payment(self):
        payment = Payment.objects.create(
            external_id="test_external_id",
            total_amount=500,
            customer=self.customer,
            paid_at="2023-11-01T12:30:45Z",
        )

        self.assertEqual(payment.external_id, "test_external_id")
        self.assertEqual(payment.total_amount, 500)
        self.assertEqual(payment.status, Payment.PaymentStatus.COMPLETED)
        self.assertEqual(payment.customer, self.customer)

    def test_payment_status_choices(self):
        payment = Payment.objects.create(
            external_id="test_external_id_2",
            total_amount=500,
            customer=self.customer,
            paid_at="2023-11-01T12:30:45Z",
            status=Payment.PaymentStatus.REJECTED,
        )

        self.assertEqual(payment.status, Payment.PaymentStatus.REJECTED)


class PaymentDetailModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            external_id="test_external_id", score=100.0, status=1
        )
        self.payment = Payment.objects.create(
            external_id="test_external_id_3",
            total_amount=1000,
            customer=self.customer,
            paid_at="2023-11-01T12:30:45Z",
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

    def test_create_payment_detail(self):
        payment_detail = PaymentDetail.objects.create(
            amount=500, loan=self.loan, payment=self.payment
        )

        self.assertEqual(payment_detail.amount, 500)
        self.assertEqual(payment_detail.loan, self.loan)
        self.assertEqual(payment_detail.payment, self.payment)
