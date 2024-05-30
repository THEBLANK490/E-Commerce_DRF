from drf_spectacular.utils import OpenApiParameter, extend_schema, inline_serializer
from drf_standardized_errors.openapi_serializers import (
    ErrorResponse401Serializer,
    ErrorResponse404Serializer,
    ValidationErrorResponseSerializer,
)
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from cart.models import Cart, CartItems
from cart.serializers import CartItemSerializer, CartSerializer, CheckoutSerializer
from core.response import get_error, get_success
from core.utils import get_or_not_found


# Create your views here.
class CartView(APIView):
    """
    API view for managing user's cart.

    Attributes:
        authentication_classes (list): The authentication classes used for this view.
        permission_classes (list): The permission classes used for this view.
        serializer_class (class): The serializer class used for this view.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self, user):
        """
        Retrieves the cart queryset for the given user.

        Args:
            user: The user for whom to retrieve the cart.

        Returns:
            QuerySet: The cart queryset.
        """
        return Cart.objects.filter(user=user, status=False).first()

    @extend_schema(
        operation_id="Cart get API",
        description="""
            Displays cart of the logged in user.
        """,
        responses={
            status.HTTP_200_OK: inline_serializer(
                "success_cart_get_response",
                fields={
                    "code": serializers.IntegerField(default=200),
                    "message": serializers.CharField(
                        default="Successfully fetched cart."
                    ),
                    "data": serializers.JSONField(default={}),
                    "error": serializers.JSONField(default={}),
                },
            ),
            status.HTTP_401_UNAUTHORIZED: ErrorResponse401Serializer,
        },
    )
    def get(self, request):
        """
        Get method to retrieve user's cart.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object.
        """
        cart = self.get_queryset(user=request.user)
        serializer = CartSerializer(cart)
        return Response(
            get_success(200, "Successfully fetched cart.", serializer.data),
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        operation_id="Cart Create API",
        description="""
        Allows user to construct a cart.
        """,
        request=CartSerializer,
        responses={
            status.HTTP_201_CREATED: inline_serializer(
                "success_cart_create_response",
                fields={
                    "code": serializers.IntegerField(default=200),
                    "message": serializers.CharField(
                        default="Cart created successfully."
                    ),
                    "data": serializers.JSONField(default={}),
                    "error": serializers.JSONField(default={}),
                },
            ),
            status.HTTP_400_BAD_REQUEST: ValidationErrorResponseSerializer,
            status.HTTP_401_UNAUTHORIZED: ErrorResponse401Serializer,
        },
    )
    def post(self, request):
        """
        Post method to create a cart.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object.
        """
        qs = self.get_queryset(user=request.user)
        get_error(qs, "Cart already exists.")
        serializer = self.serializer_class(data={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(
            get_success(200, "Cart created successfully."), status=status.HTTP_200_OK
        )


class CartDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.all()

    @extend_schema(
        operation_id="Cart Delete API",
        description="""
        Allows user to delete a cart.
        """,
        responses={
            status.HTTP_201_CREATED: inline_serializer(
                "success_cart_delete_response",
                fields={
                    "code": serializers.IntegerField(default=200),
                    "message": serializers.CharField(default="Items deleted."),
                    "data": serializers.JSONField(default={}),
                    "error": serializers.JSONField(default={}),
                },
            ),
            status.HTTP_400_BAD_REQUEST: ValidationErrorResponseSerializer,
            status.HTTP_401_UNAUTHORIZED: ErrorResponse401Serializer,
        },
    )
    def delete(self, request, *args, **kwargs):
        """
        Delete method to delete a cart.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object.
        """
        qs = self.get_queryset()
        instance = get_or_not_found(qs, id=self.kwargs.get("id"), user=request.user)
        instance.delete()
        return Response(
            get_success(200, "Items deleted", ""), status=status.HTTP_200_OK
        )


class CartItemView(APIView):
    """
    API view for managing cart items.

    Attributes:
        authentication_classes (list): The authentication classes used for this view.
        permission_classes (list): The permission classes used for this view.
        serializer_class (class): The serializer class used for this view.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    # def get_queryset(self):
    #     """
    #     Retrieves the queryset for cart items.

    #     Returns:
    #         QuerySet: The cart items queryset.
    #     """
    #     return CartItems.objects.all()

    @extend_schema(
        operation_id="Cart get API",
        description="""
            Displays cart-items of the logged in user.
        """,
        responses={
            status.HTTP_200_OK: inline_serializer(
                "success_cart-items_get_response",
                fields={
                    "code": serializers.IntegerField(default=0),
                    "message": serializers.CharField(
                        default="Successfully fetched cart-items of the cart."
                    ),
                    "data": serializers.JSONField(default={}),
                    "error": serializers.JSONField(default={}),
                },
            ),
            status.HTTP_401_UNAUTHORIZED: ErrorResponse401Serializer,
        },
    )
    def get(self, request):
        """
        Get method to retrieve cart items.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object.
        """
        qs = CartItems.objects.filter(user=request.user)
        serializer = self.serializer_class(qs, many=True)
        return Response(
            get_success(200, "Cart data", serializer.data), status=status.HTTP_200_OK
        )

    @extend_schema(
        operation_id="Cart-Items post API",
        description="""
        Creates cart-items for logged in user.
        """,
        request=CartItemSerializer,
        responses={
            status.HTTP_201_CREATED: inline_serializer(
                "success_registration_response",
                fields={
                    "code": serializers.IntegerField(default=200),
                    "message": serializers.CharField(
                        default="Cart item added successfully."
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
        Post method to create a cart item.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object.
        """
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            get_success(200, "Cart item added successfully.", serializer.data),
            status=status.HTTP_200_OK,
        )


class CartItemsUpdateDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def get_queryset(self):
        """
        Retrieves the queryset for cart items.

        Returns:
            QuerySet: The cart items queryset.
        """
        return CartItems.objects.all()

    @extend_schema(
        operation_id="CartItems update API",
        description="""
        Allows an user to update the CartItems.
        """,
        request=CartItemSerializer,
        responses={
            status.HTTP_200_OK: inline_serializer(
                "success_update_response",
                fields={
                    "code": serializers.IntegerField(default=200),
                    "message": serializers.CharField(default="Items updated"),
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
        Patch method to update a cart item.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object.
        """
        qs = self.get_queryset()
        instance = get_or_not_found(qs, id=self.kwargs.get("id"), user=request.user)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            get_success(200, "Items updated", serializer.validated_data),
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        operation_id="CartItems Delete API",
        description="""
        Allows an user delete the CartItems.
        """,
        request=CartItemSerializer,
        responses={
            status.HTTP_200_OK: inline_serializer(
                "success_delete_response",
                fields={
                    "code": serializers.IntegerField(default=200),
                    "message": serializers.CharField(default="Items deleted"),
                    "data": serializers.JSONField(default={}),
                    "error": serializers.JSONField(default={}),
                },
            ),
            status.HTTP_400_BAD_REQUEST: ValidationErrorResponseSerializer,
            status.HTTP_401_UNAUTHORIZED: ErrorResponse401Serializer,
            status.HTTP_404_NOT_FOUND: ErrorResponse404Serializer,
        },
    )
    def delete(self, request, *args, **kwargs):
        """
        Delete method to delete a cart item.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object.
        """
        qs = self.get_queryset()
        instance = get_or_not_found(qs, id=self.kwargs.get("id"), user=request.user)
        instance.delete()
        return Response(
            get_success(200, "Items deleted", ""), status=status.HTTP_200_OK
        )


class Checkout(APIView):
    """
    API view for handling checkout process.

    Attributes:
        authentication_classes (list): The authentication classes used for this view.
        permission_classes (list): The permission classes used for this view.
        serializer_class (class): The serializer class used for this view.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CheckoutSerializer

    @extend_schema(
        operation_id="Cart checkout API",
        description="""
            Displays checkout items of the logged in user.
        """,
        responses={
            status.HTTP_200_OK: inline_serializer(
                "success_checkout-items_get_response",
                fields={
                    "code": serializers.IntegerField(default=0),
                    "message": serializers.CharField(default="Checkout items."),
                    "data": serializers.JSONField(default={}),
                    "error": serializers.JSONField(default={}),
                },
            ),
            status.HTTP_401_UNAUTHORIZED: ErrorResponse401Serializer,
        },
    )
    def get(self, request):
        """
        Get method to retrieve checkout items.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object.
        """
        cart = CartItems.objects.filter(user=request.user)
        serializer = self.serializer_class(cart, many=True)
        return Response(
            get_success(200, "Checkout items", serializer.data),
            status=status.HTTP_200_OK,
        )
