import json

import requests as req
from drf_spectacular.utils import extend_schema, inline_serializer
from drf_standardized_errors.openapi_serializers import (
    ValidationErrorResponseSerializer,
)
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.response import get_success
from Ecommerce import settings
from payment.serializers import (
    KhaltiPaymentSerializer,
    KhaltiSerializer,
    KhaltiVerifySerializer,
)


# Create your views here.
class Khalti_Data(APIView):
    @extend_schema(
        operation_id="Khalti Api to get payment url",
        description="""
        Creates a product.
        """,
        request=KhaltiPaymentSerializer,
    )
    def post(self, request, *args, **kwargs):
        headers = {
            "Authorization": request.headers.get("Authorization"),
            "Content-Type": "application/json",
        }
        response = req.request(
            "POST", settings.KHALTI_URL, headers=headers, data=json.dumps(request.data)
        )
        return Response(response.json())


class Khalti_Verification(APIView):
    @extend_schema(
        operation_id="Khalti Api to get payment url",
        description="""
        Creates a product.
        """,
        request=KhaltiVerifySerializer,
    )
    def post(self, request, *args, **kwargs):
        headers = {
            "Authorization": request.headers.get("Authorization"),
            "Content-Type": "application/json",
        }
        response = req.request(
            "POST",
            settings.KHALTI_VERIFY_URL,
            headers=headers,
            data=json.dumps(request.data),
        )
        return Response(response.json())


class Khalti_data_save(APIView):
    @extend_schema(
        operation_id="Saves the transaction details in the db",
        description="""
        Creates a product.
        """,
        request=KhaltiSerializer,
        responses={
            status.HTTP_201_CREATED: inline_serializer(
                "success_payment_save_response",
                fields={
                    "code": serializers.IntegerField(default=200),
                    "message": serializers.CharField(
                        default="Transaction data saved successfully"
                    ),
                    "data": serializers.JSONField(default={}),
                    "error": serializers.JSONField(default={}),
                },
            ),
            status.HTTP_400_BAD_REQUEST: ValidationErrorResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = KhaltiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            get_success(200, "Transaction data saved successfully"),
            status=status.HTTP_201_CREATED,
        )
