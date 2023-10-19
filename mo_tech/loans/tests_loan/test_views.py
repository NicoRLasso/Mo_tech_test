import datetime
import json

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from mo_tech.customers.models import Customer
from mo_tech.loans.models import Loan


class LoanViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Set up a user for authentication
        self.user = User.objects.create_user(username="testuser", password="testpass")
        # Create a customer for testing
        self.customer = Customer.objects.create(
            external_id="customer12345", score=100.0, status=1
        )  # Add any other required fields
        self.client.login(username="testuser", password="testpassword")

        # Set up a test Loan instance linked to the created customer
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
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def test_create_loan(self):
        """Test creating a loan"""
        loan_data = {
            "external_id": "loan12360",
            "amount": 100.50,
            "status": 2,
            "contract_version": "1.0",
            "maximum_payment_date": str(timezone.now() + datetime.timedelta(days=1)),
            "taken_at": str(timezone.now() + datetime.timedelta(days=1)),
            "outstanding": 100.50,
            "customer": self.customer.id,
        }
        data_as_str = json.dumps(loan_data)

        url = reverse(
            "api:loans-list"
        )  # Adjust the name based on your URL configuration
        response = self.client.post(url, data_as_str, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Loan.objects.filter(external_id=loan_data["external_id"]).exists()
        )

    def test_retrieve_loan(self):
        """Test retrieving a loan by its id"""
        url = reverse("api:loans-detail", kwargs={"pk": self.loan.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["external_id"], self.loan.external_id)

    def test_list_loans_by_customer(self):
        """Test the custom list_by_customer endpoint"""
        url = f"/api/loans/list_by_customer/{self.customer.id}/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["external_id"], self.loan.external_id)
