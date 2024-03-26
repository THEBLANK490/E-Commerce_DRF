from rest_framework.views import APIView
from Ecommerce import settings
from product.models import Category,Product,Review
from user_authentication.response import get_error,get_success
from rest_framework.response import Response
from rest_framework import status 
from product.serializers import CategorySerializer,ProductSerializer,ReviewSerializer,KhaltiSerializer
from permission.permissions import AllowOnlyAuthorized
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import filters
from product.pagination import CustomPagination
import requests as req
# from django.conf import settings

# Create your views here.
class CategoryView(APIView):
    '''
    It is a view that is used to perform CRUD in category model.
    '''
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowOnlyAuthorized]
    
    def get_queryset(self, id):
        try:
            category = Category.objects.filter(id = id).first()
            return category
        except Category.DoesNotExist:
            return None
        
    def get(self,request,id=None):
        if id is not None:
            qs = self.get_queryset(id)
            if not qs:
                return Response(get_error(400,"data fetch failed",{"Invalid id"}),status=status.HTTP_400_BAD_REQUEST)
            serializer = CategorySerializer(qs)
            return Response(get_success(202,"Category data",serializer.data), status=status.HTTP_202_ACCEPTED) 
        qs=Category.objects.all()
        serializer = CategorySerializer(qs,many=True)
        return Response(get_success(202,"Category data",serializer.data), status=status.HTTP_202_ACCEPTED) 

    def post(self,request):
        serializer = CategorySerializer(data =request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(get_success(201,"Category data saved",serializer.data), status=status.HTTP_201_CREATED) 
        return Response(get_error(400,"Category data not saved",serializer.errors),status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,id):
        qs = self.get_queryset(id)
        if not qs:
            return Response(get_error(400,"Category data not saved","Invalid id"),status=status.HTTP_400_BAD_REQUEST)
        serializer = CategorySerializer(qs,data = request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(get_success(201,"Category data saved",serializer.data), status=status.HTTP_201_CREATED) 
        return Response(get_error(400,"Category data not saved",serializer.errors),status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id=None):
        qs = self.get_queryset(id)
        if not qs:
            return Response(get_error(400,"Category data not deleted","Invalid id"),status=status.HTTP_400_BAD_REQUEST)
        qs.delete()
        return Response(get_success(200,"Category data deleted"), status=status.HTTP_200_OK) 

class ProductView(APIView):
    '''
    It is a view that is used to perform CRUD in product model.
    '''
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowOnlyAuthorized]
    
    def get_queryset(self, id=None):
        try:
            if id:
                product = Product.objects.filter(id=id).first()
            else:
                product = Product.objects.all()
            return product
            
        except Product.DoesNotExist:
            return None
    
    def get(self,request,id=None):
        if id is not None:
            qs=self.get_queryset(id)
            if not qs:
                return Response(get_error(400,"Product data doesn't exist","Invalid id"),status=status.HTTP_400_BAD_REQUEST)
            serializer = ProductSerializer(qs)
            return Response(get_success(202,"Product data",serializer.data), status=status.HTTP_202_ACCEPTED) 

        qs = self.get_queryset()
        serializer = ProductSerializer(qs,many=True)
        return Response(get_success(202,"Product data",serializer.data), status=status.HTTP_202_ACCEPTED) 
        
    
    def post(self,request):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(get_success(201,"Product data saved",serializer.data), status=status.HTTP_201_CREATED) 
        return Response(get_error(400,"Product data not saved",serializer.errors),status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,id=None):
        qs = self.get_queryset(id)
        if not qs:
            return Response(get_error(400,"Product data not saved","Invalid id"),status=status.HTTP_400_BAD_REQUEST)
        serializer = ProductSerializer(qs,data=request.data,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(get_success(201,"Product data saved",serializer.data), status=status.HTTP_201_CREATED) 
    
    def delete(self,request,id=None):
        qs = self.get_queryset(id)
        if not qs:
            return Response(get_error(400,"Product data not deleted","Invalid id"),status=status.HTTP_400_BAD_REQUEST)
        qs.delete()
        return Response(get_success(200,"Product data deleted"), status=status.HTTP_200_OK) 
    
class ReviewView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(get_success(200,"Review Data",serializer.data), status=status.HTTP_200_OK) 


    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(get_success(201,"Review Posted",serializer.data), status=status.HTTP_201_CREATED) 
        return Response(get_error(400,"Review not Posted",serializer.errors),status=status.HTTP_400_BAD_REQUEST)

class CategoryFilter(APIView):
    def get(self,request):
        category = self.request.query_params.get('category') 
        if category:
            qs = Product.objects.filter(category__name = category)
        else:
            qs = Product.objects.all()
        serializer = ProductSerializer(qs,many =True)
        return Response(get_success(200,"Product data",{'count':len(serializer.data),'data':serializer.data}), status=status.HTTP_200_OK) 

class ProductFilter(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'name']
    
class ProductSearchView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
class ProductListPaginationView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = CustomPagination
    
    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data # pagination data
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
        return Response(data)
    
# class VerifyEsewa(APIView):
#     def get(self,request):
#         url ="https://uat.esewa.com.np/epay/main"
#         d = {'amt': request.data.amt,
#             'pdc': request.data.pdc,
#             'psc': request.data.psc,
#             'txAmt': request,
#             'tAmt': 100,
#             'pid':'ee2c3ca1-696b-4cc5-a6be-2c40d929d453',
#             'scd':'EPAYTEST',
#             'su':'http://merchant.com.np/page/esewa_payment_success?q=su',
#             'fu':'http://merchant.com.np/page/esewa_payment_failed?q=fu'}
#         resp = req.post(url, d) 
#         return Response(resp)
    
import json
class Khalti_Data(APIView):
    def post(self,request,*args,**kwargs):
        # serializer = KhaltiSerializer(data=request.data)
        headers = {
                    'Authorization': 'key live_secret_key_68791341fdd94846a146f0457ff7b455',
                    'Content-Type': 'application/json',
                }
        response = req.request("POST", settings.KHALTI_VERIFY_URL, headers=headers, data=json.dumps(request.data))        
        return Response(json.loads(response.text))
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(get_success(201,"Payment details saved",response), status=status.HTTP_201_CREATED) 
        # return Response(get_error(402,"Invalid Payment details",serializer.errors), status=status.HTTP_402_PAYMENT_REQUIRED) 
    
class Khalti_data_save(APIView):
    def post(self,request,*args,**kwargs):
        serializer = KhaltiSerializer(data = request.data)
        