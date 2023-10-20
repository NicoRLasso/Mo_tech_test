from django.db.models import Q
from django.db.models import Sum
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Customer
from .serializers import CustomerSerializer
from mo_tech.loans.models import Loan


class CustomerViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
    mixins.ListModelMixin,
):
    """ViewSet for the Customer class"""

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(status=Customer.CustomerStatus.ACTIVE)

    @action(detail=True, methods=["GET"], url_path="retrieve_balance")
    def retrieve_balance(self, request, pk=None):
        """Retrieve the balance for a specific customer."""
        customer = self.get_object()
        total_debt = (
            Loan.objects.filter(
                Q(status=Loan.LoanStatus.PENDING) | Q(status=Loan.LoanStatus.ACTIVE),
                customer=customer,
            ).aggregate(total_outstanding=Sum("outstanding"))["total_outstanding"]
            or 0.0
        )
        available_amount = customer.score - total_debt
        return Response(
            {
                "external_id": customer.external_id,
                "score": customer.score,
                "available_amount": available_amount,
                "total_debt": total_debt,
            }
        )
