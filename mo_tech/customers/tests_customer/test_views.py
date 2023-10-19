import datetime
import json
import uuid

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from mo_tech.customers.models import Customer
from mo_tech.loans.models import Loan


class CustomerViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Assuming you have a User model for authentication
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

        self.customer_data = {
            "external_id": str(uuid.uuid4()),
            "score": 100.0,
            "status": 1,
        }
        self.customer = Customer.objects.create(**self.customer_data)

        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def test_create_customer(self):
        url = reverse("api:customers-list")
        customer_data = {
            "external_id": str(uuid.uuid4()),
            "score": 100.0,
            "status": 1,
        }
        data_as_str = json.dumps(customer_data)
        response = self.client.post(url, data_as_str, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)
        self.assertEqual(response.data["status"], Customer.CustomerStatus.ACTIVE)

    def test_retrieve_customer(self):
        url = reverse("api:customers-detail", args=[self.customer.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["external_id"], self.customer_data["external_id"]
        )

    def test_retrieve_balance(self):
        max_payment_date = timezone.now() + datetime.timedelta(days=5)
        taken_at = timezone.now() + datetime.timedelta(days=1)
        Loan.objects.create(
            external_id=str(uuid.uuid4()),
            customer=self.customer,
            outstanding=30.0,
            status=Loan.LoanStatus.ACTIVE,
            maximum_payment_date=max_payment_date,
            taken_at=taken_at,
        )
        Loan.objects.create(
            external_id=str(uuid.uuid4()),
            customer=self.customer,
            outstanding=20.0,
            status=Loan.LoanStatus.PENDING,
            maximum_payment_date=max_payment_date,
            taken_at=taken_at,
        )
        Loan.objects.create(
            external_id=str(uuid.uuid4()),
            customer=self.customer,
            outstanding=10.0,
            status=Loan.LoanStatus.PAID,
            maximum_payment_date=max_payment_date,
            taken_at=taken_at,
        )

        url = f"/api/customers/{self.customer.id}/retrieve_balance/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_debt"], 50.0)
        self.assertEqual(
            response.data["available_amount"], 50.0
        )  # 100 (score) - 50 (debt)
