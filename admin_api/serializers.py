from rest_framework import serializers
from user_authentication.models import UserAccount,Role,Gender

class AdminAccountRoleSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices = Role.choices)
    class Meta:
        model = UserAccount
        fields = [
            "role"
        ]
    
    def update(self,instance,validated_data):
        instance.role = validated_data.get("role",instance.role)
        instance.save()
        return instance
    
class UserDataSerializer(serializers.Serializer):
    email = serializers.EmailField()
    photo = serializers.ImageField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()
    address = serializers.CharField()
    gender = serializers.ChoiceField(choices=Gender.choices)
    role = serializers.ChoiceField(choices = Role.choices)
    class Meta:
        model = UserAccount
