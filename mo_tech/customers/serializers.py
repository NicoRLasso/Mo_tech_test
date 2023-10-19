from rest_framework.serializers import ModelSerializer

from mo_tech.customers.models import Customer


class CustomerSerializer(ModelSerializer):
    """Serializer for the Customer class"""

    class Meta:
        model = Customer
        fields = [
            "id",
            "created_at",
            "updated_at",
            "external_id",
            "status",
            "score",
            "preapproved_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
