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

    # @Common().exception_handler
    # def post(self, request):
    #     try:
    #         doctor = Doctor.objects.filter(doctor_id=request.user).first()
    #         if doctor and doctor.specialization:
    #             return Response({"error": "Doctor profile already exists for this user."}, status=status.HTTP_400_BAD_REQUEST)

    #         serializer = DoctorRequestSerializer(data=request.data, context={'request': request})
    #         if serializer.is_valid():
    #             doctor = serializer.save()
    #             return Response(DoctorResponseSerializer(doctor).data, status=status.HTTP_201_CREATED)
    #         else:
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @Common().exception_handler
    def get(self, request, doctor_id=None):
        if doctor_id:
            doctor = Doctor.get_doctor_by_id(doctor_id)
            if not doctor:
                return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = DoctorResponseSerializer(doctor)
            return Response(serializer.data, status=status.HTTP_200_OK)

        doctors = Doctor.objects.all()
        serializer = DoctorResponseSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # @Common().exception_handler
    # def put(self, request, doctor_id):
    #     doctor = Doctor.get_doctor_by_id(doctor_id)
    #     if not doctor:
    #         return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

    #     serializer = DoctorRequestSerializer(doctor, data=request.data, partial=True, context={'request': request})
    #     if serializer.is_valid():
    #         doctor = serializer.save()
    #         return Response(DoctorResponseSerializer(doctor).data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

