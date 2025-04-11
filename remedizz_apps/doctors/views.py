from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from remedizz_apps.doctors.models import *
from remedizz_apps.doctors.serializers import *
from remedizz_apps.common.common import Common
from remedizz_apps.user.permissions import IsDoctor


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

