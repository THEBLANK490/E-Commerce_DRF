import re
from rest_framework import serializers

def phone_number_validator(phone):
    pattern = r"^9[0-9]{9}$"
    match = re.match(pattern,phone)
    if match is None:
        raise serializers.ValidationError({"phone":"Enter a valid phone number"})
    
def password_validator(data):
    if len(data) < 5:
        raise serializers.ValidationError({'password':'Password length less than 5'})
