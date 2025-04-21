

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from remedizz_apps.appointments.models import Appointment
from remedizz_apps.appointments.serializers import BookingRequestSerializer, BookingResponseSerializer 
from remedizz_apps.common.common import Common
from remedizz_apps.patients.models import Patient


class BookingView(APIView):
    permission_classes = [IsAuthenticated]

    @Common().exception_handler
    def post(self, request):
        try:
            # get patient instance linked to logged-in user
            patient = Patient.objects.get(patient_id=request.user)

            serializer = BookingRequestSerializer(data=request.data)
            if serializer.is_valid():
                # manually set patient
                appointment = serializer.save(patient=patient)
                return Response(BookingResponseSerializer(appointment).data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Patient.DoesNotExist:
            return Response({"error": "Authenticated user is not a patient"}, status=status.HTTP_400_BAD_REQUEST)


    @Common().exception_handler
    def get(self, request, appointment_id=None):
     
        if appointment_id:
          
            appointment = Appointment.get_appointment_by_id(appointment_id)
            if not appointment:
                return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)



            return Response(BookingResponseSerializer(appointment).data, status=status.HTTP_200_OK)

     
        appointment =Appointment.get_all_appointment()
        serializer = BookingResponseSerializer(appointment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @Common().exception_handler
    def delete(self, request, appointment_id):
  
        # Retrieve booking by ID
        appointment = Appointment.get_appointment_by_id(appointment_id)
        if not appointment:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the patient is accessing their own booking
        if request.user != appointment.patient.patient_id:
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
