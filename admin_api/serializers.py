from rest_framework import serializers

from user_authentication.models import Gender, Role, UserAccount


class AdminAccountRoleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    role = serializers.ChoiceField(choices=Role.choices)

    class Meta:
        model = UserAccount
        fields = ["id" "role"]

    def update(self, instance: object, validated_data: dict) -> UserAccount:
        instance.role = validated_data.get("role", instance.role)
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
    role = serializers.ChoiceField(choices=Role.choices)

    class Meta:
        model = UserAccount
