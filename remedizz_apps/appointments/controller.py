from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from remedizz_apps.appointments.views import *
from remedizz_apps.appointments.serializers import *
from remedizz_apps.common.swagger import SwaggerPage
from remedizz_apps.user.permissions import IsPatient, IsDoctor
from remedizz_apps.doctors.models.doctor import Doctor


class BookingController:

    @staticmethod
    @extend_schema(
        description="Retrieve all bookings for the authenticated user (patient or doctor).",
        responses=SwaggerPage.response(response=BookingResponseSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get_all_appointment(request):
        # Adjusting to return bookings based on the user type (patient or doctor)
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
    @permission_classes([IsAuthenticated, IsPatient])
    def get_appointment_status(request, appointment_id: int):
        return BookingView().get_status(request, appointment_id)    
    
    @staticmethod
    @extend_schema(
        description="Fetch available slots (15-minute intervals) for a doctor on a specific day.",
        responses=SwaggerPage.response(response=dict)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated, IsPatient])
    def get_available_slots(request, doctor_id: int, date: datetime):
        return AvailableSlotsView().get(request, doctor_id, date)
    
    @staticmethod
    @extend_schema(
        description="Get upcoming appointments for the authenticated patient or doctor.",
        responses=SwaggerPage.response(response=BookingResponseSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get_upcoming_appointments(request):
        return BookingView().get_upcoming(request)
    
    @staticmethod
    @extend_schema(
        description="Get past appointments for a patient (visible to the doctor).",
        responses=SwaggerPage.response(response=BookingResponseSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get_patient_history(request):
        return BookingView().get_patient_history(request)
    

    @staticmethod
    @extend_schema(
        description="Get appointment history with a specific patient (Doctor side).",
        responses=SwaggerPage.response(response=BookingResponseSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated, IsDoctor])
    def get_patient_history_detail_for_doctor(request, patient_id: int):
        return BookingView().get_patient_history_detail(request, patient_id)
