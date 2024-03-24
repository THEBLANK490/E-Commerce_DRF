from rest_framework.views import APIView
from permission.permissions import IsAdmin
from user_authentication.models import UserAccount
from product.models import Product,Category
from rest_framework.response import Response
from user_authentication.response import get_success,get_error
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication 
from admin_api.serializers import AdminAccountRoleSerializer,UserDataSerializer

# Create your views here.

class AccountRole(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    
    def get_queryset(self,id):
        qs = UserAccount.objects.filter(id = id ).exclude(is_staff=True).first()
        return qs 
    
    def patch(self,request,*args,**kwargs):
        id =request.data.get("id")
        qs = self.get_queryset(id)
        if not qs:
            return Response(get_error(400,"User update failed",{"Invalid id "}),status=status.HTTP_400_BAD_REQUEST)
        serializer = AdminAccountRoleSerializer(qs,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(get_success(202,"User role updated successfully",serializer.data), status=status.HTTP_202_ACCEPTED)  

class GetStatistics(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    def get(self,request,*args,**kwargs):
        total_customers = UserAccount.objects.filter(role = "CUSTOMER").count()
        total_staffs = UserAccount.objects.filter(role = "STAFF").count()
        total_products = Product.objects.all().count()
        total_category = Category.objects.all().count()
        data={
            "total_customers" : total_customers,
            "total_staffs" :total_staffs,
            "total_products":total_products,
            "total_category":total_category
            }
        return Response(get_success(200,"Statistics data",data),status=status.HTTP_200_OK)

class UserListAdmin(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    def get(self,request):
        qs = UserAccount.objects.all().exclude(role = "ADMIN")
        serializer = UserDataSerializer(qs, many=True)
        return Response(get_success(200,"User data",serializer.data),status=status.HTTP_200_OK)
    


