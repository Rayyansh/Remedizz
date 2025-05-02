from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from remedizz_apps.doctors.models.doctor import Doctor, RegistrationCouncil
from remedizz_apps.doctors.serializers.doctor_profile.request import DoctorRequestSerializer, RegistrationCouncilRequestSerializer
from remedizz_apps.doctors.serializers.doctor_profile.response import DoctorResponseSerializer, RegistrationCouncilResponseSerializer
from remedizz_apps.appointments.serializers import BookingResponseSerializer
from remedizz_apps.common.common import Common
from remedizz_apps.user.permissions import IsDoctor
from remedizz_apps.user.authentication import JWTAuthentication

class DoctorView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    @Common().exception_handler
    def get(self, request, doctor_id=None):
        if doctor_id:
            doctor = Doctor.get_doctor_by_id(doctor_id)
            if not doctor:
                return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = DoctorResponseSerializer(doctor)
            return Response(serializer.data, status=status.HTTP_200_OK)

        doctors = Doctor.get_all_doctors()
        serializer = DoctorResponseSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @Common().exception_handler
    def put(self, request, doctor_id):
        doctor = Doctor.get_doctor_by_id(doctor_id)
        if not doctor:
            return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DoctorRequestSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(DoctorResponseSerializer(doctor).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @Common().exception_handler
    def delete(self, request, doctor_id):
        doctor = Doctor.get_doctor_by_id(doctor_id)
        if not doctor:
            return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

        doctor.delete()
        return Response({"message": "Doctor deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    @Common().exception_handler
    def get_upcoming_appointments(self, request):
        doctor_id = JWTAuthentication.authenticate(request) 
        doctor_id = doctor_id.get("id")
        upcoming_appointments = Doctor.get_upcoming_appointments(doctor_id)

        if not upcoming_appointments:
            return Response({"message": "No upcoming appointments."}, status=status.HTTP_200_OK)

        serializer = BookingResponseSerializer(upcoming_appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @Common().exception_handler
    def confirm_appointment(self, request, appointment_id: int):
        doctor_id = JWTAuthentication.authenticate(request) 
        doctor_id = doctor_id.get("id")
        success = Doctor.confirm_appointment(doctor_id, appointment_id)

        if success:
            return Response({"message": "Appointment confirmed successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Appointment not found or already confirmed."}, status=status.HTTP_404_NOT_FOUND)

# ================================== SEARCH CLASS ============================================================

class DoctorSearchView:
    permission_classes = [IsAuthenticated]

    @Common().exception_handler
    def search(self, request):
        doctor_name = request.query_params.get("doctor_name")
        specialization = request.query_params.get("specialization")

        doctors = Doctor.objects.select_related("doctor_id", "specialization")

        if doctor_name:
            doctors = doctors.filter(doctor_id__username__icontains=doctor_name)

        if specialization:
            doctors = doctors.filter(specialization__doctor_spcialization_name__icontains=specialization)

        if not doctors.exists():
            return Response({'message': 'No doctor found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DoctorResponseSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ================================== SEARCH CLASS ============================================================


# ================================== REGISTRAION COUNCIL CLASS ============================================================
class RegistrationCouncilView(APIView):

    @Common().exception_handler
    def post(self, request):
        serializer = RegistrationCouncilRequestSerializer(data=request.data)
        if serializer.is_valid():
            registration_council = serializer.save()
            return Response(RegistrationCouncilResponseSerializer(registration_council).data, status=status.HTTP_201_CREATED)

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    @Common().exception_handler
    def get(self, request, registration_council_id=None):
        if registration_council_id:
            registration_council = RegistrationCouncil.get_registration_council_by_id(registration_council_id)
            if registration_council:
                serializer = RegistrationCouncilResponseSerializer(registration_council)
                return Response(serializer.data)
            return Response({"detail": "Registration council not found."}, status=status.HTTP_404_NOT_FOUND)
        registration_council = RegistrationCouncil.get_all_registration_council()
        serializer = RegistrationCouncilResponseSerializer(registration_council, many=True)
        return Response(serializer.data)

    @Common().exception_handler
    def put(self, request, registration_council_id):
        registration_council = RegistrationCouncil.get_registration_council_by_id(registration_council_id)
        if not registration_council:
            return Response({"detail": "Registration council not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = RegistrationCouncilRequestSerializer(registration_council, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @Common().exception_handler
    def delete(self, request, registration_council_id):
        registration_council = RegistrationCouncil.get_registration_council_by_id(registration_council_id)
        if not registration_council:
            return Response({"detail": "Registration council not found."}, status=status.HTTP_404_NOT_FOUND)

        registration_council.delete()
        return Response({"detail": "Registration council deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    @Common().exception_handler
    def get(self, request, doctor_id):

        # Get upcoming appointments for this doctor
        upcoming_appointments = Doctor.get_upcoming_appointments(doctor_id)

        if not upcoming_appointments:
            return Response({"message": "No upcoming appointments."}, status=status.HTTP_200_OK)

        # Serialize the upcoming appointments
        serializer = BookingResponseSerializer(upcoming_appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @Common().exception_handler
    def put(self, request, appointment_id, doctor_id):

        # Call the model function to confirm the appointment
        success = Doctor.confirm_appointment(doctor_id, appointment_id)

        if success:
            return Response({"message": "Appointment confirmed successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Appointment not found or already confirmed."}, status=status.HTTP_404_NOT_FOUND)
        
# ================================== REGISTRAION COUNCIL CLASS ============================================================