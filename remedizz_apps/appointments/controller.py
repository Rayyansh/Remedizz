from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from remedizz_apps.appointments.views import *
from remedizz_apps.appointments.serializers import *
from remedizz_apps.common.swagger import SwaggerPage
from remedizz_apps.user.permissions import IsPatient, IsDoctor


class BookingController:

    @staticmethod
    @extend_schema(
        description="Retrieve all bookings for the authenticated user (patient or doctor).",
        responses=SwaggerPage.response(response=BookingListSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get_all_appointment(request):
        return BookingView().get(request)

    @staticmethod
    @extend_schema(
        description="Retrieve a single booking by ID.",
        responses=SwaggerPage.response(response=BookingResponseSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get_appointment(request, appointment_id: int):
        return BookingView().get(request, appointment_id)

    @staticmethod
    @extend_schema(
        description="Create a new booking for a patient.",
        request=BookingRequestSerializer,
        responses=SwaggerPage.response(response=BookingResponseSerializer)
    )
    @api_view(['POST'])
    @permission_classes([IsAuthenticated, IsPatient])
    def create_appointment(request):
        return BookingView().post(request)

    @staticmethod
    @extend_schema(
        description="Get status of a booking by ID (Patient side).",
        responses=SwaggerPage.response(response=BookingResponseSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated , IsPatient])  # No IsPatient check since you're using booking_id directly
    def get_appointment_status(request, appointment_id: int):
        # Assuming get method in BookingView handles status as well
        return BookingView().get_status(request, appointment_id)


    # @staticmethod
    # @extend_schema(
    #     description="Search for bookings by doctor, patient, or status.",
    #     responses=SwaggerPage.response(response=BookingListSerializer)
    # )
    # @api_view(['GET'])
    # @permission_classes([IsAuthenticated])
    # def search_bookings(request):
    #     return BookingSearchView().get(request)







