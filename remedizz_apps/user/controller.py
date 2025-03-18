from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from remedizz_apps.user.serializers import UserAuthSerializer, OTPVerifySerializer
from remedizz_apps.user.views import UserAuthView, DoctorOnlyView, PatientOnlyView, DigitalClinicOnlyView
from remedizz_apps.user.permissions import IsDoctor, IsPatient, IsDigitalClinic
from remedizz_apps.common.swagger import SwaggerPage

class AuthController:
    
    @extend_schema(
        description="Authenticate or register a user and send OTP",
        request=UserAuthSerializer,
        responses=SwaggerPage.response(description="OTP sent successfully.")
    )
    @api_view(['POST'])
    def auth_process(request: Request) -> Response:
        return UserAuthView().auth_process(params=request.data)
    
    @extend_schema(
        description="Verify OTP and log in the user",
        request=OTPVerifySerializer,
        responses=SwaggerPage.response(description="User logged in successfully.")
    )
    @api_view(['POST'])
    def verify_otp(request: Request) -> Response:
        return UserAuthView().verify_otp(params=request.data)
    
    @extend_schema(
        description="Doctor-only endpoint",
        responses=SwaggerPage.response(description="Welcome, Doctor!")
    )
    @api_view(['GET'])
    @permission_classes([IsDoctor])
    def doctor_view(request: Request) -> Response:
        return DoctorOnlyView().get(request)
    
    @extend_schema(
        description="Patient-only endpoint",
        responses=SwaggerPage.response(description="Welcome, Patient!")
    )
    @api_view(['GET'])
    @permission_classes([IsPatient])
    def patient_view(request: Request) -> Response:
        return PatientOnlyView().get(request)
    
    @extend_schema(
        description="Digital Clinic-only endpoint",
        responses=SwaggerPage.response(description="Welcome, Digital Clinic!")
    )
    @api_view(['GET'])
    @permission_classes([IsDigitalClinic])
    def digital_clinic_view(request: Request) -> Response:
        return DigitalClinicOnlyView().get(request)
