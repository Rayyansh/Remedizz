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
        Get the doctor's schedule for a specific day or the full week.
        """
        if not doctor_id:
            user, _ = JWTAuthentication().authenticate(request)
            doctor_obj = Doctor.get_doctor_by_id(user.id)
            doctor_id = doctor_obj.pk

        filters = {'doctor_id': doctor_id}
        if weekday:
            filters['weekday'] = weekday

        schedules = DoctorSchedule.objects.filter(**filters)

        if not schedules.exists():
            return Response({"message": "No schedule found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DoctorScheduleResponseSerializer(schedules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @Common().exception_handler
    def post(self, request):
        """
        Create a new schedule for the logged-in doctor.
        """
        user, _ = JWTAuthentication().authenticate(request)
        doctor = Doctor.get_doctor_by_id(user.id)
        request.data['doctor'] = doctor.pk

        serializer = DoctorScheduleRequestSerializer(data=request.data)
        if serializer.is_valid():
            schedule = serializer.save()
            response = DoctorScheduleResponseSerializer(schedule).data
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @Common().exception_handler
    def put(self, request, schedule_id):
        """
        Update a specific schedule for the logged-in doctor.
        """
        user, _ = JWTAuthentication().authenticate(request)
        doctor = Doctor.get_doctor_by_id(user.id)

        schedule = DoctorSchedule.objects.filter(id=schedule_id, doctor=doctor).first()
        if not schedule:
            return Response({"message": "Schedule not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DoctorScheduleRequestSerializer(schedule, data=request.data, partial=True)
        if serializer.is_valid():
            updated_schedule = serializer.save()
            response = DoctorScheduleResponseSerializer(updated_schedule).data
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @Common().exception_handler
    def delete(self, request, schedule_id):
        """
        Delete a specific schedule for the logged-in doctor.
        """
        user, _ = JWTAuthentication().authenticate(request)
        doctor = Doctor.get_doctor_by_id(user.id)

        schedule = DoctorSchedule.objects.filter(id=schedule_id, doctor=doctor).first()
        if not schedule:
            return Response({"message": "Schedule not found."}, status=status.HTTP_404_NOT_FOUND)

        schedule.delete()
        return Response({"message": "Schedule deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
