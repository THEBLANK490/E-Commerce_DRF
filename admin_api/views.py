from drf_spectacular.utils import extend_schema, inline_serializer
from drf_standardized_errors.openapi_serializers import (
    ErrorResponse401Serializer,
    ErrorResponse404Serializer,
)
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from admin_api.serializers import AdminAccountRoleSerializer, UserDataSerializer
from core.permissions import IsAdmin
from core.response import get_success
from core.utils import get_or_not_found
from product.models import Category, Product
from user_authentication.models import UserAccount


# Create your views here.
class AccountRole(APIView):
    """
    API view for managing user roles by admin.

    Attributes:
        authentication_classes (list): The authentication classes used for this view.
        permission_classes (list): The permission classes used for this view.
        serializer_class (class): The serializer class used for this view.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    serializer_class = AdminAccountRoleSerializer

    def get_queryset(self):
        """
        Returns the queryset of user accounts.

        Returns:
            QuerySet: The queryset of user accounts.
        """
        return UserAccount.objects.all().exclude(is_staff=True)

    @extend_schema(
        operation_id="Account Role update API",
        description="""
        Allows admin to update Role.
        """,
        request=AdminAccountRoleSerializer,
        responses={
            status.HTTP_200_OK: inline_serializer(
                "success_update_response",
                fields={
                    "code": serializers.IntegerField(default=200),
                    "message": serializers.CharField(
                        default="User role updated successfully"
                    ),
                    "data": serializers.JSONField(default={}),
                    "error": serializers.JSONField(default={}),
                },
            ),
            status.HTTP_401_UNAUTHORIZED: ErrorResponse401Serializer,
            status.HTTP_404_NOT_FOUND: ErrorResponse404Serializer,
        },
    )
    def patch(self, request, *args, **kwargs):
        """
        Patch method to update user role.

        Args:
            request (Request): The request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The response object.
        """
        id = request.data.get("id")
        qs = self.get_queryset()
        query = get_or_not_found(qs, id=id)
        serializer = self.serializer_class(query, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            get_success(202, "User role updated successfully", serializer.data),
            status=status.HTTP_202_ACCEPTED,
        )


class GetStatistics(APIView):
    """
    API view for getting statistics.

    Attributes:
        authentication_classes (list): The authentication classes used for this view.
        permission_classes (list): The permission classes used for this view.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    @extend_schema(
        operation_id="Get Statistics API",
        description="""
            Displays stats.
        """,
        responses={
            status.HTTP_200_OK: inline_serializer(
                "success_stats_get_response",
                fields={
                    "code": serializers.IntegerField(default=200),
                    "message": serializers.CharField(default="Statistics data."),
                    "data": serializers.JSONField(default={}),
                    "error": serializers.JSONField(default={}),
                },
            ),
            status.HTTP_401_UNAUTHORIZED: ErrorResponse401Serializer,
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Get method to retrieve statistics data.

        Args:
            request (Request): The request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The response object.
        """
        total_customers = UserAccount.objects.filter(role="CUSTOMER").count()
        total_staffs = UserAccount.objects.filter(role="STAFF").count()
        total_products = Product.objects.all().count()
        total_category = Category.objects.all().count()
        data = {
            "total_customers": total_customers,
            "total_staffs": total_staffs,
            "total_products": total_products,
            "total_category": total_category,
        }
        return Response(
            get_success(200, "Statistics data", data), status=status.HTTP_200_OK
        )


class UserListAdmin(APIView):
    """
    API view for getting user list by admin.

    Attributes:
        authentication_classes (list): The authentication classes used for this view.
        permission_classes (list): The permission classes used for this view.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    @extend_schema(
        operation_id="Get User's List API",
        description="""
            Displays user's list.
        """,
        responses={
            status.HTTP_200_OK: inline_serializer(
                "success_user's_list_get_response",
                fields={
                    "code": serializers.IntegerField(default=200),
                    "message": serializers.CharField(default="User data."),
                    "data": serializers.JSONField(default={}),
                    "error": serializers.JSONField(default={}),
                },
            ),
            status.HTTP_401_UNAUTHORIZED: ErrorResponse401Serializer,
        },
    )
    def get(self, request):
        """
        Get method to retrieve user list.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object.
        """
        qs = UserAccount.objects.all().exclude(role="ADMIN")
        serializer = UserDataSerializer(qs, many=True)
        return Response(
            get_success(200, "User data", serializer.data), status=status.HTTP_200_OK
        )
