from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema

from remedizz_apps.clinics.views import *
from remedizz_apps.clinics.serializers import *
from remedizz_apps.common.swagger import SwaggerPage
from remedizz_apps.user.permissions import IsDigitalClinic


class ClinicController:

    @staticmethod
    @extend_schema(
        description="Retrieve all clinics.",
        responses=SwaggerPage.response(response=ClinicResponseSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsDigitalClinic])
    def get_all_clinics(request: Request) -> Response:
        return ClinicView().get(request)

    @staticmethod
    @extend_schema(
        description="Retrieve a single clinic.",
        responses=SwaggerPage.response(response=ClinicResponseSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsDigitalClinic])
    def get_clinic(request: Request, digital_clinic_id=None) -> Response:
        return ClinicView().get(request, digital_clinic_id=digital_clinic_id)



    @staticmethod
    @extend_schema(
        description="Delete clinic profile.",
        responses=SwaggerPage.response(description="clinic deleted successfully.")
    )
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated, IsDigitalClinic])
    def delete_clinic(request: Request, digital_clinic_id: int) -> Response:
        return ClinicView().delete(request, digital_clinic_id)


    @staticmethod
    @extend_schema(
        description="Update clinic profile",
        request=ClinicRequestSerializer,
        responses=SwaggerPage.response(response=ClinicResponseSerializer)
    )
    @api_view(['PUT']) 
    @permission_classes([IsAuthenticated, IsDigitalClinic])
    def update_clinic(request: Request, digital_clinic_id: int) -> Response:
        return ClinicView().put(request, digital_clinic_id)
    


