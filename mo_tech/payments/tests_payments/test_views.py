from decimal import Decimal

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from mo_tech.customers.models import Customer
from mo_tech.loans.models import Loan
from mo_tech.payments.models import Payment
from mo_tech.payments.serializers import PaymentSerializer


class PaymentViewSetTestCase(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            external_id="test_external_id", score=100.0, status=1
        )
        self.payment = Payment.objects.create(
            customer=self.customer,
            total_amount=1000,
            paid_at="2023-10-20T12:30:45Z",
            external_id="test_external_id",
        )
        self.loan_data = {
            "amount": 1000.50,
            "status": Loan.LoanStatus.PENDING,
            "contract_version": "1.0",
            "maximum_payment_date": "2023-11-01T12:30:45Z",
            "taken_at": "2023-10-20T12:30:45Z",
            "outstanding": 1000.50,
            "customer": self.customer,
        }
        self.loan_1 = Loan.objects.create(**self.loan_data, external_id="loan12346")
        self.loan_2 = Loan.objects.create(**self.loan_data, external_id="loan12347")
        self.loan_3 = Loan.objects.create(**self.loan_data, external_id="loan12348")

        self.user = User.objects.create_user(username="testuser", password="password")
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def test_retrieve_existing_payment(self):
        """Ensure we can retrieve an existing payment."""
        url = reverse("api:payments-detail", args=[self.payment.id])
        response = self.client.get(url)
        serializer = PaymentSerializer(self.payment)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_non_existing_payment(self):
        """Ensure retrieving a non-existing payment returns a 404."""
        url = reverse("api:payments-detail", args=[99999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_payments_for_non_existing_customer(self):
        """Ensure an empty list is returned for a non-existing customer."""
        url = f"/api/payments/customer/99999/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_list_by_customer(self):
        """Ensure we can list payments for a specific customer."""
        url = f"/api/payments/customer/{self.customer.id}/"
        response = self.client.get(url)
        payments = Payment.objects.filter(customer_id=self.customer.id)
        serializer = PaymentSerializer(payments, many=True)
        serialized_data = serializer.data
        response_data = response.data
        self.assertEqual(
            len(serialized_data),
            len(response_data),
            "Length mismatch between serialized and response data",
        )
        for serialized_item, response_item in zip(serialized_data, response_data):
            for key in serialized_item:
                self.assertIn(
                    key, response_item, f"Key {key} not found in response item"
                )
                self.assertEqual(
                    serialized_item[key],
                    response_item[key],
                    f"Discrepancy in {key}: Serialized: {serialized_item[key]} vs Response: {response_item[key]}",
                )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_payment(self):
        """Ensure we can create a new payment."""
        url = reverse("api:payments-list")
        data = {
            "external_id": "test_external_id_2",
            "customer_external_id": self.customer.external_id,
            "details": [
                {
                    "amount": "500.50",
                    "loan": self.loan_1.id,
                }
            ],
            "payment_date": "2023-11-01T12:30:45Z",
            "status": 1,
            "total_amount": "500.50",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Payment.objects.filter(external_id="test_external_id_2").exists()
        )
        payment = Payment.objects.get(external_id="test_external_id_2")
        self.assertEqual(payment.customer.external_id, data["customer_external_id"])
        self.assertEqual(payment.total_amount, Decimal(data["total_amount"]))
        payment_detail = payment.paymentdetail_set.first()
        self.assertIsNotNone(payment_detail)
        self.assertEqual(payment_detail.amount, Decimal(data["details"][0]["amount"]))
