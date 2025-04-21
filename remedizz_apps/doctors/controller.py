from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema

from remedizz_apps.doctors.views import *
from remedizz_apps.doctors.serializers import *
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
    

# =================================================================================

    
    @staticmethod
    @extend_schema(
        description="Search doctors by doctor name or specialization.",
        responses=SwaggerPage.response(response=DoctorSearchSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def search_doctors(request: Request) -> Response:
        return DoctorSearchView().search(request)

# ======================================================================================


class RegistrationCouncilController:

    @staticmethod
    @extend_schema(
        description="Retrieve all registration council.",
        responses=SwaggerPage.response(response=RegistrationCouncilResponseSerializer)
    )
    @api_view(['GET'])
    def get_all_registration_council(request):
        return RegistrationCouncilView.as_view()(request._request)

    @staticmethod
    @extend_schema(
        description="Retrieve a single registration council.",
        responses=SwaggerPage.response(response=RegistrationCouncilResponseSerializer)
    )
    @api_view(['GET'])
    def get_registration_council_by_id(request, registration_council_id):
        return RegistrationCouncilView.as_view()(request._request, registration_council_id=registration_council_id)
    
    @staticmethod
    @extend_schema(
        description="Create a new registration council.",
        request=RegistrationCouncilRequestSerializer,
        responses=SwaggerPage.response(response=RegistrationCouncilResponseSerializer)
    )
    @api_view(['POST'])
    def create_registration_council(request):
        return RegistrationCouncilView.as_view()(request._request)

    @staticmethod
    @extend_schema(
        description="Update registration council information.",
        request=RegistrationCouncilRequestSerializer,
        responses=SwaggerPage.response(response=RegistrationCouncilResponseSerializer)
    )
    @api_view(['PUT'])
    def update_registration_council(request, registration_council_id):
        return RegistrationCouncilView.as_view()(request._request, registration_council_id=registration_council_id)

    @staticmethod
    @extend_schema(
        description="Delete a registration council.",
        responses=SwaggerPage.response(description="Registration council deleted successfully.")
    )
    @api_view(['DELETE'])
    def delete_registration_council(request, registration_council_id):
        return RegistrationCouncilView.as_view()(request._request, registration_council_id=registration_council_id)


