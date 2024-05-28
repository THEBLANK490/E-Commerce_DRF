from drf_spectacular.utils import OpenApiParameter, extend_schema, inline_serializer
from drf_standardized_errors.openapi_serializers import (
    ValidationErrorResponseSerializer,
)
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from core.permissions import AllowAny, Is_User, IsAuthenticated
from core.response import get_success
from core.task import send_mail_task
from core.utils import get_or_not_found
from user_authentication.models import UserAccount
from user_authentication.serializers import (
    LoginSerializer,
    LogoutSerializer,
    Password_Changer_Serializer,
    ProfileSerializer,
    RegisterSerializer,
)


# Create your views here.
class Register(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    @extend_schema(
        operation_id="User Registration API",
        description="""
        Creates user with given email.
        """,
        request=RegisterSerializer,
        responses={
            status.HTTP_201_CREATED: inline_serializer(
                "success_registration_response",
                fields={
                    "code": serializers.IntegerField(default=200),
                    "message": serializers.CharField(
                        default="User created successfully"
                    ),
                    "data": serializers.JSONField(default={}),
                    "error": serializers.JSONField(default={}),
                },
            ),
            status.HTTP_400_BAD_REQUEST: ValidationErrorResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            get_success(201, "User created successfully", serializer.data),
            status=status.HTTP_201_CREATED,
        )


class Login(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @extend_schema(
        operation_id="User Login API",
        description="""
        Logins the user
        """,
        request=LoginSerializer,
        responses={
            status.HTTP_201_CREATED: inline_serializer(
                "success_registration_response",
                fields={
                    "code": serializers.IntegerField(default=200),
                    "message": serializers.CharField(
                        default="User logged in successfully"
                    ),
                    "data": serializers.JSONField(default={}),
                    "error": serializers.JSONField(default={}),
                },
            ),
            status.HTTP_400_BAD_REQUEST: ValidationErrorResponseSerializer,
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        res = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": user.id,
        }
        send_mail_task.apply_async(args=(request.data.get("email"),))
        return Response(
            get_success(200, "User logged in  successfully", res),
            status=status.HTTP_200_OK,
        )


class Logout(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    @extend_schema(
        operation_id="User Logout API",
        description="""
        Logouts the user
        """,
        request=LogoutSerializer,
        responses={
            status.HTTP_201_CREATED: inline_serializer(
                "success_registration_response",
                fields={
                    "code": serializers.IntegerField(),
                    "message": serializers.CharField(),
                    "data": serializers.CharField(),
                },
            ),
            status.HTTP_400_BAD_REQUEST: ValidationErrorResponseSerializer,
        },
    )
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Token blacklisted and logout successful."},
            status=status.HTTP_200_OK,
        )


class ViewProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [Is_User, IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return UserAccount.objects.all()

    @extend_schema(
        operation_id="View Profile Api",
        description="""
                To view the user's profile
            """,
        request=ProfileSerializer,
        responses={
            status.HTTP_200_OK: inline_serializer(
                "success_view_profile_response",
                fields={
                    "code": serializers.IntegerField(default=200),
                    "message": serializers.CharField(default="User Data"),
                    "data": serializers.JSONField(default={}),
                    "error": serializers.JSONField(default={}),
                },
            ),
            status.HTTP_400_BAD_REQUEST: ValidationErrorResponseSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        query = get_or_not_found(qs, id=kwargs.get("id"))
        serializer = self.serializer_class(query)
        return Response(
            get_success(200, "User Data", serializer.data), status=status.HTTP_200_OK
        )

    @extend_schema(
        operation_id="View Profile Api",
        description="""
                To view the user's profile
            """,
        request=ProfileSerializer,
        responses={
            status.HTTP_200_OK: inline_serializer(
                "success_view_profile_response",
                fields={
                    "code": serializers.IntegerField(default=200),
                    "message": serializers.CharField(
                        default="User updated successfully"
                    ),
                    "data": serializers.JSONField(default={}),
                    "error": serializers.JSONField(default={}),
                },
            ),
            status.HTTP_400_BAD_REQUEST: ValidationErrorResponseSerializer,
        },
    )
    def patch(self, request, *args, **kwargs):
        qs = self.get_queryset()
        query = get_or_not_found(qs, id=kwargs.get("id"))
        serializer = self.serializer_class(
            instance=query, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            get_success(202, "User updated successfully", serializer.data),
            status=status.HTTP_202_ACCEPTED,
        )


class Password_Changer(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [Is_User, IsAuthenticated]
    serializer_class = Password_Changer_Serializer

    def get_queryset(self) -> UserAccount:
        return UserAccount.objects.all()

    @extend_schema(
        operation_id="Password Changer Api",
        description="""
                To change user's password
            """,
        request=Password_Changer_Serializer,
        responses={
            status.HTTP_200_OK: inline_serializer(
                "success_view_profile_response",
                fields={
                    "code": serializers.IntegerField(default=200),
                    "message": serializers.CharField(
                        default="User password updated successfully"
                    ),
                    "data": serializers.JSONField(default={}),
                    "error": serializers.JSONField(default={}),
                },
            ),
            status.HTTP_400_BAD_REQUEST: ValidationErrorResponseSerializer,
        },
    )
    def patch(self, request, *args, **kwargs):
        qs = self.get_queryset()
        query = get_or_not_found(qs, id=kwargs.get("id"))
        serializer = self.serializer_class(
            instance=query, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            get_success(200, "User password updated successfully", serializer.data),
            status=status.HTTP_200_OK,
        )
