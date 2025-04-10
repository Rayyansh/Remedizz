from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from remedizz_apps.clinics.models import DigitalClinic
from remedizz_apps.clinics.serializers import (
    DigitalClinicRequestSerializer,
    DigitalClinicResponseSerializer,
    DigitalClinicServiceSerializer
)
from remedizz_apps.common.common import Common
from remedizz_apps.user.permissions import IsDigitalClinic


# class DigitalClinicView(APIView):
#     permission_classes = [IsAuthenticated, IsDigitalClinic]

#     @Common().exception_handler
#     def get(self, request, clinic_id=None):
#         if clinic_id:
#             clinic = DigitalClinic.get_clinic_by_id(clinic_id)
#             if not clinic:
#                 return Response({"error": "Digital clinic not found"}, status=status.HTTP_404_NOT_FOUND)
#             serializer = DigitalClinicResponseSerializer(clinic)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         clinics = DigitalClinic.objects.all()
#         serializer = DigitalClinicResponseSerializer(clinics, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     @Common().exception_handler
#     def post(self, request):
#         serializer = DigitalClinicRequestSerializer(data=request.data)
#         if serializer.is_valid():
#             clinic = serializer.save()
#             return Response(DigitalClinicResponseSerializer(clinic).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @Common().exception_handler
#     def put(self, request, clinic_id):
#         clinic = DigitalClinic.get_clinic_by_id(clinic_id)
#         if not clinic:
#             return Response({"error": "Digital clinic not found"}, status=status.HTTP_404_NOT_FOUND)

#         serializer = DigitalClinicRequestSerializer(clinic, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(DigitalClinicResponseSerializer(clinic).data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @Common().exception_handler
#     def delete(self, request, clinic_id):
#         clinic = DigitalClinic.get_clinic_by_id(clinic_id)
#         if not clinic:
#             return Response({"error": "Digital clinic not found"}, status=status.HTTP_404_NOT_FOUND)

#         clinic.delete()
#         return Response({"message": "Digital clinic deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

#     @Common().exception_handler
#     def get_services(self, request, clinic_id):
#         clinic = DigitalClinic.get_clinic_by_id(clinic_id)
#         if not clinic:
#             return Response({"error": "Clinic not found"}, status=status.HTTP_404_NOT_FOUND)

#         services = clinic.services.all()
#         serializer = DigitalClinicServiceSerializer(services, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     @Common().exception_handler
#     def add_service(self, request, clinic_id):
#         clinic = DigitalClinic.get_clinic_by_id(clinic_id)
#         if not clinic:
#             return Response({"error": "Clinic not found"}, status=status.HTTP_404_NOT_FOUND)

#         serializer = DigitalClinicServiceSerializer(data=request.data)
#         if serializer.is_valid():
#             service = serializer.save()
#             clinic.services.add(service)
#             return Response(DigitalClinicServiceSerializer(service).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 

class DigitalClinicServicesView(APIView):
    permission_classes = [IsAuthenticated, IsDigitalClinic]

    @Common().exception_handler
    def get(self, request, clinic_id):
        clinic = DigitalClinic.get_clinic_by_id(clinic_id)
        if not clinic:
            return Response({"error": "Clinic not found"}, status=status.HTTP_404_NOT_FOUND)

        services = clinic.services.all()
        serializer = DigitalClinicServiceSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddDigitalClinicServiceView(APIView):
    permission_classes = [IsAuthenticated, IsDigitalClinic]

    @Common().exception_handler
    def post(self, request, clinic_id):
        clinic = DigitalClinic.get_clinic_by_id(clinic_id)
        if not clinic:
            return Response({"error": "Clinic not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DigitalClinicServiceSerializer(data=request.data)
        if serializer.is_valid():
            service = serializer.save()
            clinic.services.add(service)
            return Response(DigitalClinicServiceSerializer(service).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
