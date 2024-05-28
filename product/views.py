from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema, inline_serializer
from drf_standardized_errors.openapi_serializers import (
    ErrorResponse401Serializer,
    ErrorResponse404Serializer,
    ValidationErrorResponseSerializer,
)
from rest_framework import filters, generics, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.permissions import AllowAny, AllowOnlyAuthorized
from core.response import get_success
from core.utils import get_or_not_found
from product.models import Category, Product, Review
from core.pagination import CustomPagination
from product.serializers import CategorySerializer, ProductSerializer, ReviewSerializer


# Create your views here.
class CategoryView(APIView):
    """
    It is a view that is used to perform CRUD in category model.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowOnlyAuthorized]
    serializer_class = CategorySerializer

    def get_queryset(self, id=None):
        """
        Retrieve all categories or a specific category by id.

        Args:
            id (int): The id of the category to retrieve.

        Returns:
            QuerySet: Queryset of Category objects.
        """
        return Category.objects.all()

    @extend_schema(
        operation_id="Category get API",
        description="""
            Displays the category of that particular id.
        """,
        parameters=[
            OpenApiParameter(name="id", required=True),
        ],
        responses={
            status.HTTP_200_OK: inline_serializer(
                "success_category_get_response",
                fields={
                    "code": serializers.IntegerField(default=200),
                    "message": serializers.CharField(
                        default="Successfully fetched category data."
                    ),
                    "data": serializers.JSONField(default={}),
                    "error": serializers.JSONField(default={}),
                },
            ),
            status.HTTP_401_UNAUTHORIZED: ErrorResponse401Serializer,
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve a category.

        Args:
            request: The incoming HTTP request.

        Returns:
            Response: JSON response containing the category data.
        """
        id = request.query_params.get("id")
        qs = self.get_queryset()
        query = get_or_not_found(qs, id=id)
        serializer = self.serializer_class(query)
        return Response(
            get_success(202, "Successfully fetched category data.", serializer.data),
            status=status.HTTP_202_ACCEPTED,
        )

    @extend_schema(
        operation_id="Category-Items post API",
        description="""
        Creates a category.
        """,
        request=CategorySerializer,
        responses={
            status.HTTP_201_CREATED: inline_serializer(
                "success_category_response",
                fields={
                    "code": serializers.IntegerField(default=200),
                    "message": serializers.CharField(default="Category data saved"),
                    "data": serializers.JSONField(default={}),
                    "error": serializers.JSONField(default={}),
                },
            ),
            status.HTTP_400_BAD_REQUEST: ValidationErrorResponseSerializer,
        },
    )
    def post(self, request):
        """
        Handles POST requests to create a category.

        Args:
            request: The incoming HTTP request.

        Returns:
            Response: JSON response containing the saved category data.
        """
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            get_success(201, "Category data saved", serializer.data),
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        operation_id="Category update API",
        description="""
        Allows an user to update the Category.
        """,
        request=CategorySerializer,
        parameters=[
            OpenApiParameter(name="id", required=True),
        ],
        responses={
            status.HTTP_200_OK: inline_serializer(
                "success_update_response",
                fields={
                    "code": serializers.IntegerField(default=200),
                    "message": serializers.CharField(default="Category data updated"),
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
        Handles PATCH requests to update a category.

        Args:
            request: The incoming HTTP request.

        Returns:
            Response: JSON response containing the updated category data.
        """
        id = request.query_params.get("id")
        qs = self.get_queryset()
        instance = get_or_not_found(qs, id=id)
        serializer = self.serializer_class(
            instance=instance, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            get_success(201, "Category data updated", serializer.data),
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        operation_id="Category Delete API",
        description="""
        Allows an user delete the Category.
        """,
        request=CategorySerializer,
        parameters=[
            OpenApiParameter(name="id", required=True),
        ],
        responses={
            status.HTTP_200_OK: inline_serializer(
                "success_delete_response",
                fields={
                    "code": serializers.IntegerField(default=200),
                    "message": serializers.CharField(default="Category data deleted"),
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
        Handles DELETE requests to delete a category.

        Args:
            request: The incoming HTTP request.

        Returns:
            Response: JSON response indicating successful deletion.
        """
        id = request.query_params.get("id")
        qs = self.get_queryset()
        query = get_or_not_found(qs, id=id)
        query.delete()
        return Response(
            get_success(200, "Category data deleted"), status=status.HTTP_200_OK
        )


class Category_all_view(APIView):
    """
    It is a view that is used to get all data from category model.
    """

    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer

    def get_queryset(self) -> Category:
        """
        Retrieve all categories.

        Returns:
            QuerySet: Queryset of all Category objects.
        """
        return Category.objects.all()

    @extend_schema(
        operation_id="Category get all data API",
        description="""
            Displays all the category data.
        """,
        responses={
            status.HTTP_200_OK: inline_serializer(
                "success_category_get_response",
                fields={
                    "code": serializers.IntegerField(default=200),
                    "message": serializers.CharField(
                        default="Successfully fetched category data."
                    ),
                    "data": serializers.JSONField(default={}),
                    "error": serializers.JSONField(default={}),
                },
            ),
            status.HTTP_401_UNAUTHORIZED: ErrorResponse401Serializer,
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve all category data.

        Args:
            request: The incoming HTTP request.

        Returns:
            Response: JSON response containing all category data.
        """
        qs = self.get_queryset()
        serializer = self.serializer_class(qs, many=True)
        return Response(
            get_success(
                202, "Successfully fetched all category data.", serializer.data
            ),
            status=status.HTTP_202_ACCEPTED,
        )


class ProductView(APIView):
    """
    It is a view that is used to perform CRUD in product model.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowOnlyAuthorized]
    serializer_class = ProductSerializer

    def get_queryset(self) -> Product:
        """
        Retrieve all products or a specific product by id.

        Returns:
            QuerySet: Queryset of Product objects.
        """
        return Product.objects.all()

    @extend_schema(
        operation_id="Product get API",
        description="""
            Displays the products of that particular id.
        """,
        parameters=[
            OpenApiParameter(name="id", required=True),
        ],
        responses={
            status.HTTP_200_OK: inline_serializer(
                "success_product_get_response",
                fields={
                    "code": serializers.IntegerField(default=200),
                    "message": serializers.CharField(
                        default="Successfully fetched product data."
                    ),
                    "data": serializers.JSONField(default={}),
                    "error": serializers.JSONField(default={}),
                },
            ),
            status.HTTP_401_UNAUTHORIZED: ErrorResponse401Serializer,
        },
    )
    def get(self, request, id=None):
        """
        Handles GET requests to retrieve a product.

        Args:
            request: The incoming HTTP request.
            id (int): The id of the product to retrieve.

        Returns:
            Response: JSON response containing the product data.
        """
        id = request.query_params.get("id")
        qs = self.get_queryset()
        query = get_or_not_found(qs, id=id)
        serializer = self.serializer_class(query)
        return Response(
            get_success(202, "Successfully fetched category data.", serializer.data),
            status=status.HTTP_202_ACCEPTED,
        )

    @extend_schema(
        operation_id="Product-Items post API",
        description="""
        Creates a product.
        """,
        request=ProductSerializer,
        responses={
            status.HTTP_201_CREATED: inline_serializer(
                "success_category_response",
                fields={
                    "code": serializers.IntegerField(default=200),
                    "message": serializers.CharField(default="Product data saved"),
                    "data": serializers.JSONField(default={}),
                    "error": serializers.JSONField(default={}),
                },
            ),
            status.HTTP_400_BAD_REQUEST: ValidationErrorResponseSerializer,
        },
    )
    def post(self, request):
        """
        Handles POST requests to create a product.

        Args:
            request: The incoming HTTP request.

        Returns:
            Response: JSON response containing the saved product data.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            get_success(201, "Product data saved", serializer.data),
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        operation_id="Product update API",
        description="""
        Allows an user to update the Product.
        """,
        request=ProductSerializer,
        parameters=[
            OpenApiParameter(name="id", required=True),
        ],
        responses={
            status.HTTP_200_OK: inline_serializer(
                "success_update_response",
                fields={
                    "code": serializers.IntegerField(default=200),
                    "message": serializers.CharField(default="Product data updated"),
                    "data": serializers.JSONField(default={}),
                    "error": serializers.JSONField(default={}),
                },
            ),
            status.HTTP_401_UNAUTHORIZED: ErrorResponse401Serializer,
            status.HTTP_404_NOT_FOUND: ErrorResponse404Serializer,
        },
    )
    def patch(self, request, id=None):
        """
        Handles PATCH requests to update a product.

        Args:
            request: The incoming HTTP request.
            id (int): The id of the product to update.

        Returns:
            Response: JSON response containing the updated product data.
        """
        id = request.query_params.get("id")
        qs = self.get_queryset()
        instance = get_or_not_found(qs, id=id)
        serializer = self.serializer_class(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            get_success(201, "Product data updated", serializer.data),
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        operation_id="Product Delete API",
        description="""
        Allows an user delete the Product.
        """,
        request=ProductSerializer,
        parameters=[
            OpenApiParameter(name="id", required=True),
        ],
        responses={
            status.HTTP_200_OK: inline_serializer(
                "success_delete_response",
                fields={
                    "code": serializers.IntegerField(default=200),
                    "message": serializers.CharField(default="Product data deleted"),
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
        Handles DELETE requests to delete a product.

        Args:
            request: The incoming HTTP request.

        Returns:
            Response: JSON response indicating successful deletion.
        """
        id = request.query_params.get("id")
        qs = self.get_queryset()
        query = get_or_not_found(qs, id=id)
        query.delete()
        return Response(
            get_success(200, "Product data deleted"), status=status.HTTP_200_OK
        )


class Product_all_view(APIView):
    """
    It is a view that is used to get all data from product model.
    """

    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self) -> Product:
        """
        Retrieve all products.

        Returns:
            QuerySet: Queryset of all Product objects.
        """
        return Product.objects.all()

    @extend_schema(
        operation_id="Product get all data API",
        description="""
            Displays all the product data.
        """,
        responses={
            status.HTTP_200_OK: inline_serializer(
                "success_product_get_response",
                fields={
                    "code": serializers.IntegerField(default=200),
                    "message": serializers.CharField(
                        default="Successfully fetched product data."
                    ),
                    "data": serializers.JSONField(default={}),
                    "error": serializers.JSONField(default={}),
                },
            ),
            status.HTTP_401_UNAUTHORIZED: ErrorResponse401Serializer,
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve all product data.

        Args:
            request: The incoming HTTP request.

        Returns:
            Response: JSON response containing all product data.
        """
        qs = self.get_queryset()
        serializer = self.serializer_class(qs, many=True)
        return Response(
            get_success(202, "Successfully fetched all product data.", serializer.data),
            status=status.HTTP_202_ACCEPTED,
        )


class ReviewView(APIView):
    """
    It is a view that is used to get and post data for review model.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get(self, request):
        """
        Handles GET requests to retrieve all reviews.

        Args:
            request: The incoming HTTP request.

        Returns:
            Response: JSON response containing all review data.
        """
        reviews = Review.objects.all()
        serializer = self.serializer_class(reviews, many=True)
        return Response(
            get_success(200, "Review Data", serializer.data), status=status.HTTP_200_OK
        )

    def post(self, request):
        """
        Handles POST requests to create a new review.

        Args:
            request: The incoming HTTP request.

        Returns:
            Response: JSON response containing the created review data.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            get_success(201, "Review Posted", serializer.data),
            status=status.HTTP_201_CREATED,
        )


class CategoryFilter(APIView):
    def get(self, request):
        """
        Handles GET requests to filter products by category.

        Args:
            request: The incoming HTTP request.

        Returns:
            Response: JSON response containing filtered product data.
        """
        category = self.request.query_params.get("category")
        if category:
            qs = Product.objects.filter(category__name=category)
        else:
            qs = Product.objects.all()
        serializer = ProductSerializer(qs, many=True)
        return Response(
            get_success(
                200,
                "Product data",
                {"count": len(serializer.data), "data": serializer.data},
            ),
            status=status.HTTP_200_OK,
        )


class ProductFilter(generics.ListAPIView):
    """
    View for filtering products by category and name.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category", "name"]


class ProductSearchView(generics.ListAPIView):
    """
    View for searching products by name.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class ProductListPaginationView(generics.ListAPIView):
    """
    View for paginating product list.
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = CustomPagination

    def get(self, request):
        """
        Handles GET requests to retrieve paginated product list.

        Args:
            request: The incoming HTTP request.

        Returns:
            Response: JSON response containing paginated product data.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
        return Response(data)
