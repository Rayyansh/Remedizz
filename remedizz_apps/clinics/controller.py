from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from remedizz_apps.clinics.models import DigitalClinic
from remedizz_apps.clinics.serializers import DigitalClinicRequestSerializer, DigitalClinicResponseSerializer


class ClinicController:

    @staticmethod
    @api_view(['GET'])
    def get_clinic(request, clinic_id=None):
        if clinic_id:
            clinic = DigitalClinic.get_clinic_by_id(clinic_id)
            if not clinic:
                return Response({'error': 'Clinic not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = DigitalClinicResponseSerializer(clinic)
            return Response(serializer.data)

        clinics = DigitalClinic.get_all_clinics()
        serializer = DigitalClinicResponseSerializer(clinics, many=True)
        return Response(serializer.data)

    @staticmethod
    @api_view(['POST'])
    def create_clinic(request):
        serializer = DigitalClinicRequestSerializer(data=request.data)
        if serializer.is_valid():
            clinic = serializer.save()
            return Response(DigitalClinicResponseSerializer(clinic).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(['PUT'])
    def update_clinic(request, clinic_id):
        clinic = DigitalClinic.get_clinic_by_id(clinic_id)
        if not clinic:
            return Response({'error': 'Clinic not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DigitalClinicRequestSerializer(clinic, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(DigitalClinicResponseSerializer(clinic).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(['DELETE'])
    def delete_clinic(request, clinic_id):
        clinic = DigitalClinic.get_clinic_by_id(clinic_id)
        if not clinic:
            return Response({'error': 'Clinic not found'}, status=status.HTTP_404_NOT_FOUND)

        clinic.delete()
        return Response({'message': 'Clinic deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
