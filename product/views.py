from rest_framework.views import APIView
from product.models import Category,Product,Review
from user_authentication.views import CustomResponse
from rest_framework.response import Response
from rest_framework import status 
from product.serializers import CategorySerializer,ProductSerializer,ReviewSerializer
from product.permissions import AllowOnlyAuthorized
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
class CategoryView(APIView):
    '''
    It is a view that is used to perform CRUD in category model.
    '''
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowOnlyAuthorized]
    
    def get(self,request,id=None):
        if id is not None:
            qs = Category.objects.filter(id = id).first()
            if not qs:
                return Response(CustomResponse().get_error(400,"data fetch failed",{"Invalid id"}),status=status.HTTP_400_BAD_REQUEST)
            serializer = CategorySerializer(qs)
            return Response(CustomResponse().get_success(202,"Category data",serializer.data), status=status.HTTP_202_ACCEPTED) 
        qs=Category.objects.all()
        serializer = CategorySerializer(qs,many=True)
        return Response(CustomResponse().get_success(202,"Category data",serializer.data), status=status.HTTP_202_ACCEPTED) 

    def post(self,request):
        serializer = CategorySerializer(data =request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(CustomResponse().get_success(201,"Category data saved",serializer.data), status=status.HTTP_201_CREATED) 
        return Response(CustomResponse().get_error(400,"Category data not saved",serializer.errors),status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,id):
        qs = Category.objects.filter(id = id).first()
        if not qs:
            return Response(CustomResponse().get_error(400,"Category data not saved","Invalid id"),status=status.HTTP_400_BAD_REQUEST)
        serializer = CategorySerializer(qs,data = request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(CustomResponse().get_success(201,"Category data saved",serializer.data), status=status.HTTP_201_CREATED) 
        return Response(CustomResponse().get_error(400,"Category data not saved",serializer.errors),status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id=None):
        qs = Category.objects.filter(id = id).first()
        if not qs:
            return Response(CustomResponse().get_error(400,"Category data not deleted","Invalid id"),status=status.HTTP_400_BAD_REQUEST)
        qs.delete()
        return Response(CustomResponse().get_success(200,"Category data deleted"), status=status.HTTP_200_OK) 

class ProductView(APIView):
    '''
    It is a view that is  use to perform CRUD in product model.
    '''
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowOnlyAuthorized]
    
    def get(self,request,id=None):
        if id is not None:
            qs = Product.objects.filter(id=id).first()
            if not qs:
                return Response(CustomResponse().get_error(400,"Product data doesn't exist","Invalid id"),status=status.HTTP_400_BAD_REQUEST)
            serializer = ProductSerializer(qs)
            return Response(CustomResponse().get_success(202,"Product data",serializer.data), status=status.HTTP_202_ACCEPTED) 
        qs = Product.objects.all()
        serializer = ProductSerializer(qs,many=True)
        return Response(CustomResponse().get_success(202,"Product data",serializer.data), status=status.HTTP_202_ACCEPTED) 
    
    def post(self,request):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(CustomResponse().get_success(201,"Product data saved",serializer.data), status=status.HTTP_201_CREATED) 
        return Response(CustomResponse().get_error(400,"Product data not saved",serializer.errors),status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,id=None):
        qs = Product.objects.filter(id=id).first()
        if not qs:
            return Response(CustomResponse().get_error(400,"Product data not saved","Invalid id"),status=status.HTTP_400_BAD_REQUEST)
        serializer = ProductSerializer(qs,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(CustomResponse().get_success(201,"Product data saved",serializer.data), status=status.HTTP_201_CREATED) 
        return Response(CustomResponse().get_error(400,"Product data not saved",serializer.errors),status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id=None):
        qs = Product.objects.filter(id=id).first()
        if not qs:
            return Response(CustomResponse().get_error(400,"Product data not deleted","Invalid id"),status=status.HTTP_400_BAD_REQUEST)
        qs.delete()
        return Response(CustomResponse().get_success(200,"Product data deleted"), status=status.HTTP_200_OK) 
    
class ReviewView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductFilter(APIView):
    def get(self,request):
        category = self.request.query_params.get('category') 
        if category:
            qs = Product.objects.filter(category__name = category)
        else:
            qs = Product.objects.all()
        serializer = ProductSerializer(qs,many =True)
        return Response(CustomResponse().get_success(200,"Product data",{'count':len(serializer.data),'data':serializer.data}), status=status.HTTP_200_OK) 
