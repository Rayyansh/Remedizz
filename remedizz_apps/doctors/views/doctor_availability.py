from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from remedizz_apps.doctors.models.doctor import Doctor
from remedizz_apps.doctors.models.doctor_availability import DoctorSchedule
from remedizz_apps.doctors.serializers.doctor_availability.request import DoctorScheduleRequestSerializer
from remedizz_apps.doctors.serializers.doctor_availability.response import DoctorScheduleResponseSerializer
from remedizz_apps.user.permissions import IsDoctor
from remedizz_apps.user.authentication import JWTAuthentication
from remedizz_apps.common.common import Common

class DoctorScheduleView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    @Common().exception_handler
    def get(self, request, doctor_id=None, weekday=None):
        """
        Get the doctor's schedule for a specific day or for the whole week.
        """
        # Get doctor_id from JWT if not passed
        if not doctor_id:
            user, token = JWTAuthentication().authenticate(request)
            user_id = user.id
            doctor_id = Doctor.get_doctor_by_id(user_id)
            doctor_id = doctor_id.pk
        
        # Fetch schedule for the specified weekday or all available schedules
        if weekday:
            schedule = DoctorSchedule.get_schedule_by_day(doctor_id, weekday)
            if not schedule:
                return Response({"message": "No schedule found for this day."}, status=status.HTTP_404_NOT_FOUND)
            serializer = DoctorScheduleResponseSerializer(schedule, many=True)
        else:
            schedule = DoctorSchedule.objects.filter(doctor_id=doctor_id)
            if not schedule.exists():
                return Response({"message": "No schedule found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = DoctorScheduleResponseSerializer(schedule, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    @Common().exception_handler
    def post(self, request):
        """
        Create a new schedule for the logged-in doctor.
        """
        user, token = JWTAuthentication().authenticate(request)
        user = user.id
        doctor_id = Doctor.get_doctor_by_id(user)
        doctor_id = doctor_id.pk
        request.data['doctor'] = doctor_id  # Attach the doctor_id to the request data
        
        serializer = DoctorScheduleRequestSerializer(data=request.data)
        if serializer.is_valid():
            schedule = serializer.save()  # Ensure the doctor field is passed here
            return Response(DoctorScheduleResponseSerializer(schedule).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @Common().exception_handler
    def put(self, request, schedule_id):
        """
        Update a specific schedule entry for the logged-in doctor.
        """
        user, token = JWTAuthentication().authenticate(request)
        user = user.id
        doctor_id = Doctor.get_doctor_by_id(user)
        doctor_id = doctor_id.pk
        
        schedule = DoctorSchedule.objects.filter(id=schedule_id, doctor_id=doctor_id).first()
        if not schedule:
            return Response({"message": "Schedule not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DoctorScheduleRequestSerializer(schedule, data=request.data, partial=True)
        if serializer.is_valid():
            updated_schedule = serializer.save()
            return Response(DoctorScheduleResponseSerializer(updated_schedule).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @Common().exception_handler
    def delete(self, request, schedule_id):
        """
        Delete a specific schedule entry for the logged-in doctor.
        """
        user, token = JWTAuthentication().authenticate(request)
        user = user.id
        doctor_id = Doctor.get_doctor_by_id(user)
        doctor_id = doctor_id.pk
        
        schedule = DoctorSchedule.objects.filter(id=schedule_id, doctor_id=doctor_id).first()
        if not schedule:
            return Response({"message": "Schedule not found."}, status=status.HTTP_404_NOT_FOUND)

        schedule.delete()
        return Response({"message": "Schedule deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
