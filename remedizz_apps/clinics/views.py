from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from remedizz_apps.clinics.models import *
from remedizz_apps.clinics.serializers import *
from remedizz_apps.common.common import Common
from remedizz_apps.user.permissions import IsDigitalClinic


class ClinicView(APIView):
    permission_classes = [IsAuthenticated, IsDigitalClinic]


    @Common().exception_handler
    def get(self, request, digital_clinic_id=None):
        if digital_clinic_id:
            clinic = DigitalClinic.get_clinic_by_id(digital_clinic_id)
            if not clinic:
                return Response({"error": "Clinic not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = ClinicResponseSerializer(clinic)
            return Response(serializer.data, status=status.HTTP_200_OK)

        clinics = DigitalClinic.objects.all()
        serializer = ClinicResponseSerializer(clinics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @Common().exception_handler
    def put(self, request, digital_clinic_id):
        clinic = DigitalClinic.get_clinic_by_id(digital_clinic_id)
        if not clinic:
            return Response({"error": "Clinic not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClinicRequestSerializer(clinic, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(ClinicResponseSerializer(clinic).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    @Common().exception_handler
    def delete(self, request, digital_clinic_id):
        clinic = DigitalClinic.get_clinic_by_id(digital_clinic_id)
        if not clinic:
            return Response({"error": "Clinic not found"}, status=status.HTTP_404_NOT_FOUND)

        clinic.delete()
        return Response({"message": "Clinic deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

