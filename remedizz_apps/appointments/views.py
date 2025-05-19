
from datetime import datetime
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from remedizz_apps.user.permissions import IsPatient
from rest_framework.exceptions import PermissionDenied

from remedizz_apps.appointments.models import Appointment
from remedizz_apps.appointments.serializers import BookingRequestSerializer, BookingResponseSerializer 
from remedizz_apps.common.common import Common
from remedizz_apps.doctors.models.doctor import Doctor
from remedizz_apps.doctors.models.doctor_availability import DoctorSchedule
from remedizz_apps.patients.models import Patient
from remedizz_apps.appointments.utils import generate_available_slots
from remedizz_apps.appointments.booking_service import BookingService
from remedizz_apps.user.authentication import JWTAuthentication

class BookingView(APIView):
    permission_classes = [IsAuthenticated]

    @Common().exception_handler
    def post(self, request):
        user, token = JWTAuthentication().authenticate(request)
        user = user.id
        patient_id = Patient.get_patient_by_id(user)
        patient_id = patient_id.pk

        patient = Patient.objects.get(id=patient_id)

        serializer = BookingRequestSerializer(data=request.data, context={'patient': patient})

        serializer.is_valid(raise_exception=True)

        appointment = BookingService.create_appointment(patient, serializer.validated_data)
        return Response(BookingResponseSerializer(appointment).data, status=status.HTTP_201_CREATED)

    @Common().exception_handler
    def put(self, request, appointment_id):
        # Retrieve the appointment to be updated
        appointment = Appointment.get_appointment_by_id(appointment_id)
        if not appointment:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        user, token = JWTAuthentication().authenticate(request)
        user = user.id
        patient_id = Patient.get_patient_by_id(user)
        patient_id = patient_id.pk
        # Get patient instance linked to logged-in user
        patient = Patient.objects.get(patient=patient_id)

        # Validate incoming data with serializer
        serializer = BookingRequestSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            # Use the serializer's update method to handle the update logic
            updated_appointment = serializer.update(appointment, serializer.validated_data)

            # Return the updated appointment details in response
            return Response(BookingResponseSerializer(updated_appointment).data, status=status.HTTP_200_OK)

        # If serializer is invalid, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @Common().exception_handler
    def get(self, request, appointment_id=None):
        if appointment_id:
            appointment = Appointment.get_appointment_by_id(appointment_id)
            if not appointment:
                return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

            return Response(BookingResponseSerializer(appointment).data, status=status.HTTP_200_OK)

        appointment = Appointment.get_all_appointment()
        serializer = BookingResponseSerializer(appointment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @Common().exception_handler
    def delete(self, request, appointment_id):
        # Retrieve booking by ID
        patient_id = JWTAuthentication.authenticate(request) 
        patient_id = patient_id.get("id")
        appointment = Appointment.get_appointment_by_id(appointment_id)
        if not appointment:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the patient is accessing their own booking
        if patient_id != appointment.patient.patient_id:
            raise PermissionDenied("You are not authorized to delete this booking.")

        # Delete the booking
        appointment.delete()
        return Response({"message": "Booking deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    @Common().exception_handler
    def get_status(self, request, appointment_id: int):
        # Retrieve booking by ID
        appointment = Appointment.get_appointment_by_id(appointment_id)
        if not appointment:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the patient is accessing their own booking
        return Response({"booking_id": appointment.id, "status": appointment.status}, status=status.HTTP_200_OK)

    @Common().exception_handler
    def get_upcoming(self, request):
        user, token = JWTAuthentication().authenticate(request)
        user_id = user.id

        # Check if user is a patient
        patient_obj = Patient.get_patient_by_id(user_id)
        if patient_obj:
            appointments = Appointment.objects.filter(
                patient=patient_obj,
                appointment_date__gte=timezone.now().date()
            ).order_by('appointment_date', 'appointment_time')

            serializer = BookingResponseSerializer(appointments, many=True)
            return Response({"upcoming_appointments": serializer.data}, status=200)

        # Check if user is a doctor
        doctor_obj = Doctor.get_doctor_by_id(user_id)
        if doctor_obj:
            appointments = Appointment.objects.filter(
                doctor=doctor_obj,
                appointment_date__gte=timezone.now().date()
            ).order_by('appointment_date', 'appointment_time')

            serializer = BookingResponseSerializer(appointments, many=True)
            return Response({"upcoming_appointments": serializer.data}, status=200)

        return Response({"error": "Unauthorized role"}, status=403)
    
    @Common().exception_handler
    def get_patient_history(self, request, patient_id: int):
        user, token = JWTAuthentication().authenticate(request)
        user = user.id
        doctor = Doctor.get_doctor_by_id(user)

        if not doctor:
            return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get past appointments for this doctor
        history = Appointment.objects.filter(
            doctor=doctor,
            appointment_date__lt=timezone.now().date()
        ).order_by('-appointment_date', '-appointment_time')

        serializer = BookingResponseSerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_patient_history_detail(self, request, patient_id: int):
        user, _ = JWTAuthentication().authenticate(request)
        doctor = Doctor.get_doctor_by_id(user.id)

        if not doctor:
            raise PermissionDenied("Only doctors can access patient history.")

        # Get all appointments for this doctor and the specified patient in the past
        history = Appointment.objects.filter(
            doctor=doctor,
            patient__id=patient_id,
            appointment_date__lt=timezone.now().date()
        ).order_by('-appointment_date')

        serializer = BookingResponseSerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AvailableSlotsView(APIView):
    permission_classes = [IsAuthenticated, IsPatient]

    @Common().exception_handler
    def get(self, request, doctor_id, date):
        appointment_date = datetime.strptime(date, "%Y-%m-%d").date()
        schedules = DoctorSchedule.get_schedule_by_day(doctor_id, appointment_date.weekday())

        if not schedules:
            return Response({"error": "No schedule found for this doctor on the selected day"}, status=404)

        all_available_slots = []

        for schedule in schedules:
            booked_slots = Appointment.get_booked_slots(doctor_id, schedule.pk, appointment_date)
            available_slots = generate_available_slots(schedule, appointment_date, booked_slots)
            all_available_slots.extend(available_slots)

        return Response({"slots": all_available_slots})