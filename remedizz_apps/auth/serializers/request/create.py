# from rest_framework import serializers
#
# from biller_apps.app_template.dataclasses.request.create import AppTemplateRequest
#
#
# class AppTemplateRequestSerializer(serializers.Serializer):
#
#     def create(self, validated_data) -> AppTemplateRequest:
#         return AppTemplateRequest(**validated_data)

from rest_framework import serializers
from remedizz_apps.auth.models import User, OTP
from remedizz_apps.auth.dataclasses.request.create import UserCreateData


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data) -> UserCreateData:
        user = User.objects.create(**validated_data)
        return UserCreateData(id=user.id, username=user.username, user_role=user.user_role, contact_number=user.contact_number)


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = '__all__'

    def create(self, validated_data) -> OTP:
        return OTP.objects.create(**validated_data)


