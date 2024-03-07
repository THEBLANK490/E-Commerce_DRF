from django.shortcuts import render
from user_authentication.models import UserAccount
from rest_framework.views import APIView
from user_authentication.serializers import RegisterSerializer,LoginSerializer,ProfileSerializer
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
class CustomResponse():
    @classmethod
    def get_success(self,code,message,data=None):
        context = {
        "code":code,
        "message":message,
        "data": data,
        "error":{}
        }
        return context
    
    @classmethod
    def get_error(self,code,message,error):
        context = {
        "code":code,
        "message":message,
        "data": {},
        "error":error,
        }
        return context


class Register(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(CustomResponse().get_success(200,"User created successfully",serializer.data),status=status.HTTP_201_CREATED) 
        return Response(CustomResponse().get_error(400,"User registration failed",serializer.errors),status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            res={
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id
            }
            return Response(CustomResponse().get_success(200,"User created successfully",res), status=status.HTTP_200_OK) 
        return Response(CustomResponse().get_error(400,"User login failed",serializer.errors),status=status.HTTP_400_BAD_REQUEST)
    
class Logout(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(CustomResponse().get_success(200,"User logged out successfully"), status=status.HTTP_205_RESET_CONTENT) 
        
        except Exception as e:
            return Response(CustomResponse().get_error(400,"User logout failed",{"Invalid token"}),status=status.HTTP_400_BAD_REQUEST)

        
from user_authentication.permissions import Is_User
class ViewProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [Is_User,IsAuthenticated]
    
    def get(self,request,id=None):
        if id is not None:
            qs = UserAccount.objects.filter(id = id).exclude(is_staff=True).first()
            self.check_object_permissions(request,qs)
            if not qs:
                return Response(CustomResponse().get_error(400,"data fetch failed",{"Invalid id"}),status=status.HTTP_400_BAD_REQUEST)
            serializer = ProfileSerializer(qs)
            return Response(CustomResponse().get_success(202,"User data",serializer.data), status=status.HTTP_202_ACCEPTED) 
    
        qs = UserAccount.objects.exclude(is_staff=True)   
        serializer = ProfileSerializer(qs,many=True)
        return Response(CustomResponse().get_success(202,"User data",serializer.data), status=status.HTTP_202_ACCEPTED) 
    
    def put(self,request, id):
        qs = UserAccount.objects.filter(id=id).exclude(is_staff=True).first()
        if not qs:
            return Response(CustomResponse().get_error(400,"User update failed",{"Invalid id "}),status=status.HTTP_400_BAD_REQUEST)
        serializer = ProfileSerializer(qs,data = request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(CustomResponse().get_success(202,"User updated successfully",serializer.data), status=status.HTTP_202_ACCEPTED)
        return Response(CustomResponse().get_error(400,"Not valid",serializer.errors), status=status.HTTP_400_BAD_REQUEST) 
    
