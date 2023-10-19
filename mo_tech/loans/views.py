from django.utils import timezone
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Loan
from .serializers import LoanSerializer


class LoanViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        loan = serializer.save()
        if loan.status == Loan.LoanStatus.ACTIVE:
            loan.taken_at = timezone.now()
            loan.save()

    @action(
        detail=False,
        methods=["get"],
        url_path="list_by_customer/(?P<customer_id>[^/.]+)",
    )
    def list_by_customer(self, request, customer_id=None):
        if customer_id:
            loans = Loan.objects.filter(customer_id=customer_id)
            serializer = LoanSerializer(loans, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "customer_id is required"}, status=400)
