# from drf_spectacular.utils import extend_schema
# from rest_framework.decorators import api_view
# from rest_framework.request import Request
# from rest_framework.response import Response
#
# from biller_apps.app_template.serializers.request.create import AppTemplateRequestSerializer
# from biller_apps.app_template.serializers.request.delete import AppTemplateDeleteRequestSerializer
# from biller_apps.app_template.serializers.request.delete_many import AppTemplateDeleteManySerializer
# from biller_apps.app_template.serializers.request.update import AppTemplateUpdateRequestSerializer
# from biller_apps.app_template.serializers.response.get_all import AppTemplateGetAllSerializer
# from biller_apps.app_template.views import AppTemplateView
# from biller_apps.common.serializer_validations import SerializerValidations
# from biller_apps.common.serializers.request.get_all import GetAllSerializer
# from biller_apps.common.serializers.request.search import SearchSerializer
# from biller_apps.common.swagger import SwaggerPage
#
#
# class AppTemplateViewController:
#
#     @extend_schema(
#         description="Add an AppTemplate",
#         request=AppTemplateRequestSerializer,
#         responses=SwaggerPage.response(description=AppTemplateView().data_created)
#     )
#     @api_view(['POST'])
#     @SerializerValidations(serializer=AppTemplateRequestSerializer,
#                            exec_func='AppTemplateView().create_extract(request)').validate
#     def create(request: Request) -> Response:
#         return AppTemplateView().create_extract(params=request.params, token_payload=request.payload)



from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from remedizz_apps.auth.serializers.request.create import UserSerializer, OTPSerializer
from remedizz_apps.auth.views import UserView, OTPView
from remedizz_apps.common.serializer_validations import SerializerValidations
from remedizz_apps.common.swagger import SwaggerPage


class UserViewController:

    @extend_schema(
        description="Create a new user",
        request=UserSerializer,
        responses=SwaggerPage.response(description=UserView().data_created)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=UserSerializer,
                           exec_func='UserView().create_user(request)').validate
    def create(request: Request) -> Response:
        """Handles user registration"""
        return UserView().create_user(params=request.data, token_payload=request.auth)


class OTPViewController:

    @extend_schema(
        description="Generate OTP for authentication",
        request=OTPSerializer,
        responses=SwaggerPage.response(description=OTPView().otp_generated)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=OTPSerializer,
                           exec_func='OTPView().generate_otp(request)').validate
    def generate(request: Request) -> Response:
        """Handles OTP generation"""
        return OTPView().generate_otp(params=request.data, token_payload=request.auth)

    @extend_schema(
        description="Verify the OTP",
        request=OTPSerializer,
        responses=SwaggerPage.response(description=OTPView().otp_verified)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=OTPSerializer,
                           exec_func='OTPView().verify_otp(request)').validate
    def verify(request: Request) -> Response:
        """Handles OTP verification"""
        return OTPView().verify_otp(params=request.data, token_payload=request.auth)


