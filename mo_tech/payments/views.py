from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Payment
from .serializers import PaymentSerializer
from .services import PaymentService
from .services import PaymentValidationService


class PaymentViewSet(GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        payment_data = request.data
        validation_service = PaymentValidationService(data=payment_data)
        if not validation_service.is_valid():
            return Response(
                {"error": validation_service.get_errors()},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment_service = PaymentService(data=payment_data)
        try:
            payment = payment_service.create_payment()
            serializer = self.get_serializer(payment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"], url_path="customer/(?P<customer_id>\d+)")
    def list_by_customer(self, request, customer_id=None):
        payments = Payment.objects.filter(customer_id=customer_id)
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
