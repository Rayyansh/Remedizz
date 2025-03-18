from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers
from remedizz_apps.user.models import User

class UserAuthSerializer(serializers.Serializer):

    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('digital_clinic', 'Digital Clinic'),
    )
    username = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    role = serializers.ChoiceField(choices=ROLE_CHOICES)

    def validate(self, data):
        if not all([data.get('username'), data.get('phone_number'), data.get('role')]):
            raise serializers.ValidationError("Username, role, and phone number are required.")
        return data

class OTPVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6, required=True)

    def validate(self, data):
        otp = data.get('otp')
        
        if not otp:
            raise serializers.ValidationError("OTP are required.")
        
        return data

class UserAuthResponseSerializer(serializers.ModelSerializer):
    token = serializers.CharField()

    class Meta:
        model = User
        fields = ('id', 'username', 'phone_number', 'role', 'token')
