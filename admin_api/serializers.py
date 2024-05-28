from rest_framework import serializers

from user_authentication.models import Gender, Role, UserAccount


class AdminAccountRoleSerializer(serializers.Serializer):
    """
    Serializer for admin account role.

    Attributes:
        id (IntegerField): The ID of the user account.
        role (ChoiceField): The role of the user account.

    Methods:
        update: Updates the role of the user account.
    """

    id = serializers.IntegerField()
    role = serializers.ChoiceField(choices=Role.choices)

    class Meta:
        model = UserAccount
        fields = ["id" "role"]

    def update(self, instance: object, validated_data: dict) -> UserAccount:
        """
        Updates the role of the user account.

        Args:
            instance (object): The user account instance to be updated.
            validated_data (dict): The validated data for role update.

        Returns:
            UserAccount: The updated user account instance.
        """
        instance.role = validated_data.get("role", instance.role)
        instance.save()
        return instance


class UserDataSerializer(serializers.Serializer):
    """
    Serializer for user data.

    Attributes:
        email (EmailField): The email of the user.
        photo (ImageField): The photo of the user.
        first_name (CharField): The first name of the user.
        last_name (CharField): The last name of the user.
        phone_number (CharField): The phone number of the user.
        address (CharField): The address of the user.
        gender (ChoiceField): The gender of the user.
        role (ChoiceField): The role of the user.
    """

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
        fields = [
            "email",
            "photo",
            "first_name",
            "last_name",
            "phone_number",
            "address",
            "gender",
            "role",
        ]
