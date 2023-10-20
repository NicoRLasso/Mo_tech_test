from django.test import TestCase
from rest_framework.exceptions import ValidationError

from mo_tech.customers.models import Customer
from mo_tech.customers.serializers import CustomerSerializer


class CustomerSerializerTest(TestCase):
    def setUp(self):
        self.customer_data = {
            "external_id": "12345",
            "score": 9.5,
            "status": Customer.CustomerStatus.ACTIVE,
        }
        self.customer = Customer.objects.create(**self.customer_data)

    def test_serializer_valid_data(self):
        """Test serialization of valid customer data"""
        serializer = CustomerSerializer(instance=self.customer)
        data = serializer.data
        self.assertEqual(data["external_id"], self.customer_data["external_id"])
        self.assertEqual(float(data["score"]), self.customer_data["score"])
        self.assertEqual(data["status"], self.customer_data["status"])

    def test_serializer_read_only_fields(self):
        """Test that read-only fields are not updated by the serializer"""
        serializer = CustomerSerializer(
            instance=self.customer,
            data={
                "id": 99,
                "created_at": "2022-10-19T12:30:45Z",
                "updated_at": "2022-10-19T13:30:45Z",
                "external_id": "98765",
                "score": 8.5,
                "status": Customer.CustomerStatus.INACTIVE,
            },
            partial=True,
        )

        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.customer.refresh_from_db()

        self.assertNotEqual(self.customer.id, 99)
        self.assertNotEqual(str(self.customer.created_at), "2022-10-19T12:30:45Z")
        self.assertNotEqual(str(self.customer.updated_at), "2022-10-19T13:30:45Z")
        self.assertEqual(self.customer.external_id, "98765")
        self.assertEqual(self.customer.score, 8.5)

    def test_serializer_invalid_data(self):
        """Test serialization of invalid data"""
        invalid_data = {
            "external_id": "",
            "score": 15,
            "status": 99,
        }
        serializer = CustomerSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
