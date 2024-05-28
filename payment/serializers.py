from rest_framework import serializers

from core.validators import email_is_user_instance_validator, phone_number_validator
from payment.models import KhaltiInfo


class KhaltiSerializer(serializers.Serializer):
    """
    Serializer for saving data in db.

    Attributes:
        user (CharField): The email of the user.
        pixd (CharField): The PIXD information.
        transaction_id (CharField): The transaction ID.
        total_amount (IntegerField): The total amount.
        mobile (CharField): The mobile number.
        status (CharField): The status.
        user_email (CharField): The email of the user.
        purchase_order_id (CharField): The purchase order ID.
        purchase_order_name (CharField): The purchase order name.

    Methods:
        create: Creates a new KhaltiInfo instance with the validated data.
    """

    user = serializers.CharField(source="user.email")
    pixd = serializers.CharField(max_length=250)
    transaction_id = serializers.CharField(max_length=250)
    total_amount = serializers.IntegerField()
    mobile = serializers.CharField(max_length=50, validators=[phone_number_validator])
    status = serializers.CharField(max_length=250)
    user_email = serializers.CharField(validators=[email_is_user_instance_validator])
    purchase_order_id = serializers.CharField(max_length=250)
    purchase_order_name = serializers.CharField(max_length=250)

    def create(self, validated_data: dict) -> KhaltiInfo:
        """
        Creates a new KhaltiInfo instance with the validated data.

        Args:
            validated_data (dict): The validated data for KhaltiInfo creation.

        Returns:
            KhaltiInfo: The newly created KhaltiInfo instance.
        """
        data = {
            "user": validated_data["user"],
            "pixd": validated_data["pixd"],
            "transaction_id": validated_data["transaction_id"],
            "total_amount": validated_data["total_amount"],
            "mobile": validated_data["mobile"],
            "status": validated_data["status"],
            "user_email": validated_data["user_email"],
            "purchase_order_id": validated_data["purchase_order_id"],
            "purchase_order_name": validated_data["purchase_order_name"],
        }

        data = KhaltiInfo.objects.create(**data)
        data.save()
        return data


class KhaltiUserSerializer:
    """Serializer to show the fields in swagger"""

    name = serializers.CharField()
    email = serializers.CharField()
    phone = serializers.CharField()


class KhaltiPaymentSerializer(serializers.Serializer):
    """Serializer to show the fields in swagger"""

    return_url = serializers.CharField()
    website_url = serializers.CharField()
    amount = serializers.IntegerField()
    purchase_order_id = serializers.CharField()
    customer_info = KhaltiUserSerializer()


class KhaltiVerifySerializer(serializers.Serializer):
    """Serializer to show the fields in swagger"""

    pidx = serializers.CharField()
