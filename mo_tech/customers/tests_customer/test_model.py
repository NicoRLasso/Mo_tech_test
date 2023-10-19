from django.test import TestCase

from mo_tech.customers.models import Customer


class CustomerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Customer.objects.create(external_id="123", score=10.0)

    def test_external_id_label(self):
        customer = Customer.objects.get(id=1)
        field_label = customer._meta.get_field("external_id").verbose_name
        self.assertEqual(field_label, "external id")

    def test_external_id_max_length(self):
        customer = Customer.objects.get(id=1)
        max_length = customer._meta.get_field("external_id").max_length
        self.assertEqual(max_length, 60)

    def test_score_max_digits_and_decimal_places(self):
        customer = Customer.objects.get(id=1)
        max_digits = customer._meta.get_field("score").max_digits
        decimal_places = customer._meta.get_field("score").decimal_places
        self.assertEqual(max_digits, 12)
        self.assertEqual(decimal_places, 2)

    def test_status_choices(self):
        customer = Customer.objects.get(id=1)
        status_choices = dict(Customer.CustomerStatus.choices)
        self.assertIn(customer.status, status_choices)

    def test_preapproved_at_default_null(self):
        customer = Customer.objects.get(id=1)
        preapproved_at = customer.preapproved_at
        self.assertIsNone(preapproved_at)

    def test_default_status(self):
        customer = Customer.objects.get(id=1)
        self.assertEqual(customer.status, Customer.CustomerStatus.ACTIVE)

    def test_created_at_and_updated_at(self):
        customer = Customer.objects.get(id=1)
        # This ensures the fields are auto-set and are not None.
        self.assertIsNotNone(customer.created_at)
        self.assertIsNotNone(customer.updated_at)
