from drf_spectacular.utils import extend_schema, inline_serializer
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
    """
    API view for user registration.
    """

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
        """
        Handles POST requests to create a new user.

        Args:
            request: The incoming HTTP request.

        Returns:
            Response: JSON response containing the created user data.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            get_success(201, "User created successfully", serializer.data),
            status=status.HTTP_201_CREATED,
        )


class Login(APIView):
    """
    API view for user login.
    """

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
        """
        Handles POST requests to log in a user.

        Args:
            request: The incoming HTTP request.

        Returns:
            Response: JSON response containing the logged-in user data.
        """
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
    """
    API view for user logout.
    """

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
        """
        Handles POST requests to log out a user.

        Args:
            request: The incoming HTTP request.

        Returns:
            Response: JSON response confirming the logout.
        """
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
    """
    API view for viewing and updating user profile.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [Is_User, IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_queryset(self, request):
        """
        Retrieve all UserAccount.

        Returns:
            QuerySet: Queryset of all UserAccount objects.
        """
        user_email = request.user.email
        return (
            UserAccount.objects.filter(email=user_email).exclude(role="ADMIN").first()
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
                    "message": serializers.CharField(default="User Data"),
                    "data": serializers.JSONField(default={}),
                    "error": serializers.JSONField(default={}),
                },
            ),
            status.HTTP_400_BAD_REQUEST: ValidationErrorResponseSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve user profile.

        Args:
            request: The incoming HTTP request.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: JSON response containing user data.
        """
        qs = self.get_queryset(request=request)
        serializer = self.serializer_class(qs)
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
        """
        Handles PATCH requests to update user profile.

        Args:
            request: The incoming HTTP request.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: JSON response confirming the profile update.
        """
        qs = self.get_queryset(request=request)
        serializer = self.serializer_class(instance=qs, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            get_success(202, "User updated successfully", serializer.data),
            status=status.HTTP_202_ACCEPTED,
        )


class Password_Changer(APIView):
    """
    API view for changing user password.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [Is_User, IsAuthenticated]
    serializer_class = Password_Changer_Serializer

    def get_queryset(self) -> UserAccount:
        """
        Retrieve all UserAccount.

        Returns:
            QuerySet: Queryset of all UserAccount objects.
        """
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
        """
        Handles PATCH requests to change user password.

        Args:
            request: The incoming HTTP request.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: JSON response confirming the password change.
        """
        qs = self.get_queryset()
        query = get_or_not_found(qs, id=request.user.id)
        serializer = self.serializer_class(
            instance=query, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            get_success(200, "User password updated successfully", serializer.data),
            status=status.HTTP_200_OK,
        )
