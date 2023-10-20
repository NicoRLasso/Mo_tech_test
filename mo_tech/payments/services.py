from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from .models import Payment
from .models import PaymentDetail
from mo_tech.customers.models import Customer
from mo_tech.loans.models import Loan


class PaymentValidationService:
    def __init__(self, data):
        self.data = data
        self.errors = []

    def is_valid(self):
        customer_external_id = self.data.get("customer_external_id")
        customer = Customer.objects.filter(external_id=customer_external_id).first()
        if not customer:
            self.errors.append("Customer not found")
            return False
        total_amount = self.data.get("total_amount", 0.0)
        loan_details = self.data.get("details", [])
        loan_ids = [loan_detail["loan"] for loan_detail in loan_details]
        actual_loans = Loan.objects.filter(id__in=loan_ids)
        loan_lookup = {loan.id: loan for loan in actual_loans}
        total_due = sum(
            [
                loan_lookup.get(loan_detail["loan"], Loan(outstanding=0)).outstanding
                for loan_detail in loan_details
            ]
        )
        if float(total_amount) > float(total_due):
            self.errors.append("Payment amount exceeds total due.")
        loans_amount = sum(
            [float(loan_detail["amount"]) for loan_detail in loan_details]
        )
        if loans_amount != float(total_amount):
            self.errors.append(
                "The total_amount does not match the sum of loan amounts"
            )
        for loan_data in loan_details:
            loan = loan_lookup.get(loan_data["loan"])
            if not loan:
                self.errors.append(f"Loan with ID {loan_data['loan']} doesn't exist")
            elif loan.outstanding < float(loan_data["amount"]):
                self.errors.append(
                    f"Payment for loan {loan_data['loan']} is greater than the outstanding amount"
                )
        return not bool(self.errors)

    def get_errors(self):
        return self.errors


class PaymentService:
    def __init__(self, data):
        self.data = data

    def create_payment(self):
        customer_external_id = self.data.get("customer_external_id")
        external_id = self.data.get("external_id")
        total_amount = self.data.get("total_amount", 0)
        loans = self.data.get("details", [])
        customer = Customer.objects.filter(external_id=customer_external_id).first()
        if not customer:
            raise ValueError("Customer not found")
        with transaction.atomic():
            payment = self._create_payment_entry(customer, total_amount, external_id)
            self._create_payment_detail_entries(payment, loans)
            self._update_loan_outstanding(loans)

        return payment

    def _create_payment_entry(self, customer, total_amount, external_id):
        payment = Payment(
            external_id=external_id,
            total_amount=total_amount,
            customer=customer,
            paid_at=timezone.now(),
        )
        payment.save()
        return payment

    def _create_payment_detail_entries(self, payment, loans):
        loan_ids = [loan_data["loan"] for loan_data in loans]
        actual_loans = Loan.objects.filter(id__in=loan_ids)
        loan_lookup = {loan.id: loan for loan in actual_loans}
        payment_details = []
        for loan_data in loans:
            loan = loan_lookup.get(loan_data["loan"])
            if not loan:
                continue
            payment_detail = PaymentDetail(
                amount=loan_data["amount"], loan=loan, payment=payment
            )
            payment_details.append(payment_detail)
        PaymentDetail.objects.bulk_create(payment_details)

    def _update_loan_outstanding(self, loans):
        loan_ids = [loan_data["loan"] for loan_data in loans]
        actual_loans = Loan.objects.filter(id__in=loan_ids)
        loan_lookup = {loan.id: loan for loan in actual_loans}
        updated_loans = []
        for loan_data in loans:
            loan = loan_lookup.get(loan_data["loan"])
            if not loan:
                continue
            loan.outstanding -= Decimal(loan_data["amount"])
            if loan.outstanding < 0:
                loan.outstanding = 0
            updated_loans.append(loan)

        Loan.objects.bulk_update(updated_loans, ["outstanding"])
