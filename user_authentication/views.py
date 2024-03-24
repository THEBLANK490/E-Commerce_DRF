from user_authentication.models import UserAccount
from rest_framework.views import APIView
from user_authentication.serializers import RegisterSerializer,LoginSerializer,ProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from permission.permissions import Is_User,IsAuthenticated,AllowAny
from user_authentication.response import get_success,get_error

# Create your views here.
class Register(APIView):
    permission_classes = [AllowAny]
    
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(get_success(200,"User created successfully",serializer.data),status=status.HTTP_201_CREATED) 
        return Response(get_error(400,"User registration failed",serializer.errors),status=status.HTTP_400_BAD_REQUEST)

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
            return Response(get_success(200,"User created successfully",res), status=status.HTTP_200_OK) 
        return Response(get_error(400,"User login failed",serializer.errors),status=status.HTTP_400_BAD_REQUEST)
    
class Logout(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(get_success(200,"User logged out successfully"), status=status.HTTP_205_RESET_CONTENT) 
        
        except Exception as e:
            return Response(get_error(400,"User logout failed",{"Invalid token"}),status=status.HTTP_400_BAD_REQUEST)

class ViewProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [Is_User,IsAuthenticated]
    serializer_class = [ProfileSerializer]
    
    def get_queryset(self,id):
        try:
            qs = UserAccount.objects.filter(id = id).exclude(is_staff=True).first()
            return qs
        except UserAccount.DoesNotExist:
            return None
            

    def get(self,request):
        id = request.data.get('id')
        if id is not None:
            qs = self.get_queryset(id)
            serializer = ProfileSerializer(qs)
            return Response(get_success(200,"User Data",serializer.data),status=status.HTTP_200_OK) 
    
    def put(self,request):
        id = request.data.get('id')
        qs = self.get_queryset(id)
        if not qs:
            return Response(get_error(400,"User update failed",{"Invalid id "}),status=status.HTTP_400_BAD_REQUEST)
        serializer = ProfileSerializer(qs,data = request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(get_success(202,"User updated successfully",serializer.data), status=status.HTTP_202_ACCEPTED)    
