from rest_framework import serializers
from user_authentication.models import UserAccount
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from user_authentication.validators import phone_number_validator,password_validator
from user_authentication.models import Gender,Role


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 255,required = True,validators = [UniqueValidator(queryset=UserAccount.objects.all())])
    password = serializers.CharField(max_length = 128,write_only = True,required = True,validators=[password_validator])
    password2 = serializers.CharField(max_length = 128,write_only = True,required = True)
    photo = serializers.FileField(required = False,validators=[phone_number_validator])
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    phone_number = serializers.CharField(max_length=15)
    gender = serializers.ChoiceField(choices=Gender.choices)
    role = serializers.ChoiceField(choices=Role.choices)

    def validate(self, data):        
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password":"Password Fields don't match"})
        return data
    
    def create(self,validated_data):
        user = UserAccount.objects.create(email=validated_data['email'],first_name = validated_data['first_name'],last_name = validated_data['last_name'],phone_number=validated_data['phone_number'],gender = validated_data['gender'],role=validated_data['role'])
        
        if user.role =='ADMIN':
            user.is_staff = True
            user.is_superuser = True

        if user.role =='STAFF':
            user.is_staff = True
            
        user.set_password(validated_data['password'])
        if 'photo' in validated_data:
            user.photo=validated_data['photo']
        user.save()
        return validated_data 
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 255,required = True)
    password = serializers.CharField(max_length = 128,write_only = True,required = True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")
        return data

class ProfileSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length =255)
    photo = serializers.FileField(required = False)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    
    def update(self,instance,validated_data):
        instance.email = validated_data.get('email',instance.email)
        instance.first_name = validated_data.get("first_name",instance.first_name)
        instance.last_name = validated_data.get("last_name",instance.last_name)
        instance.save()
        return instance
