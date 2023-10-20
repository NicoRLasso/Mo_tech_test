from django.test import TestCase
from rest_framework.exceptions import ValidationError

from mo_tech.customers.models import Customer
from mo_tech.loans.models import Loan
from mo_tech.loans.serializers import LoanSerializer


class LoanSerializerTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            external_id="customer12345", status=1, score=600
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

    def test_serializer_valid_data(self):
        """Test serialization of valid loan data"""
        serializer = LoanSerializer(instance=self.loan)
        data = serializer.data
        self.assertEqual(data["external_id"], self.loan_data["external_id"])
        self.assertEqual(float(data["amount"]), self.loan_data["amount"])
        self.assertEqual(data["status"], self.loan_data["status"])

    def test_serializer_read_only_fields(self):
        """Test that read-only fields are not updated by the serializer"""
        serializer = LoanSerializer(
            instance=self.loan,
            data={
                "id": 99,
                "created_at": "2023-10-19T12:30:45Z",
                "updated_at": "2023-10-19T13:30:45Z",
                "external_id": "loan98765",
                "amount": 150.75,
                "status": Loan.LoanStatus.ACTIVE,
            },
            partial=True,
        )

        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.loan.refresh_from_db()

        self.assertNotEqual(self.loan.id, 99)
        self.assertNotEqual(str(self.loan.created_at), "2023-10-19T12:30:45Z")
        self.assertNotEqual(str(self.loan.updated_at), "2023-10-19T13:30:45Z")
        self.assertEqual(self.loan.external_id, "loan98765")
        self.assertEqual(self.loan.amount, 150.75)

    def test_serializer_invalid_data(self):
        """Test serialization of invalid data"""
        invalid_data = {
            "external_id": "",
            "amount": -100,
            "status": 99,
        }
        serializer = LoanSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
