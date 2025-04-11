from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema

from remedizz_apps.doctors.views import DoctorView
from remedizz_apps.doctors.serializers import DoctorRequestSerializer, DoctorResponseSerializer
from remedizz_apps.common.swagger import SwaggerPage
from remedizz_apps.user.permissions import IsDoctor


class DoctorController:

    @staticmethod
    @extend_schema(
        description="Retrieve all doctors.",
        responses=SwaggerPage.response(response=DoctorResponseSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsDoctor])
    def get_all_doctors(request: Request) -> Response:
        return DoctorView().get(request)

    @staticmethod
    @extend_schema(
        description="Retrieve a single doctor.",
        responses=SwaggerPage.response(response=DoctorResponseSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsDoctor])
    def get_doctor(request: Request, doctor_id=None) -> Response:
        return DoctorView().get(request, doctor_id=doctor_id)



    @staticmethod
    @extend_schema(
        description="Delete doctor profile.",
        responses=SwaggerPage.response(description="Doctor deleted successfully.")
    )
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated, IsDoctor])
    def delete_doctor(request: Request, doctor_id: int) -> Response:
        return DoctorView().delete(request, doctor_id)


    @staticmethod
    @extend_schema(
        description="Update doctor profile",
        request=DoctorRequestSerializer,
        responses=SwaggerPage.response(response=DoctorResponseSerializer)
    )
    @api_view(['PUT']) 
    @permission_classes([IsAuthenticated, IsDoctor])
    def update_doctor(request: Request, doctor_id: int) -> Response:
        return DoctorView().put(request, doctor_id)
