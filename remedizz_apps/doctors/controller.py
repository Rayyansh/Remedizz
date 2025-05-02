from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiResponse, OpenApiParameter

from remedizz_apps.doctors.views.doctor_profile import DoctorView, DoctorSearchView, RegistrationCouncilView
from remedizz_apps.doctors.views.doctor_availability import DoctorScheduleView
from remedizz_apps.doctors.serializers.doctor_profile.request import DoctorRequestSerializer, DoctorSearchSerializer, RegistrationCouncilRequestSerializer
from remedizz_apps.doctors.serializers.doctor_profile.response import DoctorResponseSerializer, RegistrationCouncilResponseSerializer
from remedizz_apps.doctors.serializers.doctor_availability.request import DoctorScheduleRequestSerializer
from remedizz_apps.doctors.serializers.doctor_availability.response import DoctorScheduleResponseSerializer

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
    
    # @staticmethod
    # @extend_schema(
    #     description="Get all upcoming appointments for the authenticated doctor.",
    #     responses=SwaggerPage.response(response=BookingResponseSerializer)
    # )
    # @api_view(['GET'])
    # @permission_classes([IsAuthenticated, IsDoctor])
    # def get_upcoming_appointments(request):
    #     return DoctorView().get_upcoming_appointments(request)

    # @staticmethod
    # @extend_schema(
    #     description="Confirm a pending appointment for a doctor.",
    #     responses=SwaggerPage.response(response=BookingResponseSerializer)
    # )
    # @api_view(['PUT'])
    # @permission_classes([IsAuthenticated, IsDoctor])
    # def confirm_appointment(request, appointment_id: int):
    #     return DoctorView().confirm_appointment(request, appointment_id)

    
    @staticmethod
    @extend_schema(
        description="Search doctors by doctor name or specialization.",
        responses=SwaggerPage.response(response=DoctorSearchSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def search_doctors(request: Request) -> Response:
        return DoctorSearchView().search(request)

# ================================== REGISTRACTION COUNCIL ===================================================


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


# ================================== REGISTRACTION COUNCIL ===================================================

class DoctorScheduleController:

    @staticmethod
    @extend_schema(
        description="Retrieve doctor schedules. Filter by weekday if provided.",
        responses=SwaggerPage.response(response=DoctorScheduleResponseSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated, IsDoctor])
    def get_doctor_schedule(request: Request, weekday: int = None) -> Response:
        return DoctorScheduleView().get(request=request, weekday=weekday)
    
    @staticmethod
    @extend_schema(
        description="Create a new doctor schedule.",
        request=DoctorScheduleRequestSerializer,
        responses=SwaggerPage.response(response=DoctorScheduleResponseSerializer)
    )
    @api_view(['POST'])
    @permission_classes([IsAuthenticated, IsDoctor])
    def create_doctor_schedule(request: Request) -> Response:
        return DoctorScheduleView().post(request)

    @staticmethod
    @extend_schema(
        description="Update an existing doctor schedule.",
        request=DoctorScheduleRequestSerializer,
        responses=SwaggerPage.response(response=DoctorScheduleResponseSerializer)
    )
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated, IsDoctor])
    def update_doctor_schedule(request: Request, schedule_id: int) -> Response:
        return DoctorScheduleView().put(request, schedule_id)

    @staticmethod
    @extend_schema(
        description="Delete a doctor schedule.",
        responses=SwaggerPage.response(description="Doctor schedule deleted successfully.")
    )
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated, IsDoctor])
    def delete_doctor_schedule(request: Request, schedule_id: int) -> Response:
        return DoctorScheduleView().delete(request, schedule_id)