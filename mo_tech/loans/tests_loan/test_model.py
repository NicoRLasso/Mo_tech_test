from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from mo_tech.customers.models import Customer
from mo_tech.loans.models import Loan


class LoanModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        customer = Customer.objects.create(
            external_id="test_customer", status=1, score=100.0
        )
        Loan.objects.create(
            external_id="test_loan",
            amount=1000.00,
            maximum_payment_date=timezone.now() + timedelta(days=30),
            taken_at=timezone.now(),
            customer=customer,
            outstanding=1000.00,
        )

    def test_loan_external_id(self):
        loan = Loan.objects.get(external_id="test_loan")
        field_label = loan._meta.get_field("external_id").verbose_name
        self.assertEquals(field_label, "external id")

    def test_loan_amount(self):
        loan = Loan.objects.get(external_id="test_loan")
        field_label = loan._meta.get_field("amount").verbose_name
        self.assertEquals(field_label, "amount")

    def test_loan_status(self):
        loan = Loan.objects.get(external_id="test_loan")
        field_label = loan._meta.get_field("status").verbose_name
        self.assertEquals(field_label, "status")

    def test_loan_contract_version(self):
        loan = Loan.objects.get(external_id="test_loan")
        field_label = loan._meta.get_field("contract_version").verbose_name
        self.assertEquals(field_label, "contract version")

    def test_loan_maximum_payment_date(self):
        loan = Loan.objects.get(external_id="test_loan")
        field_label = loan._meta.get_field("maximum_payment_date").verbose_name
        self.assertEquals(field_label, "maximum payment date")

    def test_loan_taken_at(self):
        loan = Loan.objects.get(external_id="test_loan")
        field_label = loan._meta.get_field("taken_at").verbose_name
        self.assertEquals(field_label, "taken at")

    def test_loan_customer(self):
        loan = Loan.objects.get(external_id="test_loan")
        field_label = loan._meta.get_field("customer").verbose_name
        self.assertEquals(field_label, "customer")

    def test_loan_outstanding(self):
        loan = Loan.objects.get(external_id="test_loan")
        field_label = loan._meta.get_field("outstanding").verbose_name
        self.assertEquals(field_label, "outstanding")
