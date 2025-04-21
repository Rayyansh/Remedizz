from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from remedizz_apps.specialization.models import DoctorSpecializations
from remedizz_apps.common.common import Common
from remedizz_apps.specialization.serializers import *

class SpecializationView(APIView):

    @Common().exception_handler
    def post(self, request):
        serializer = SpecializationRequestSerializer(data=request.data)
        if serializer.is_valid():
            specialization = serializer.save()
            return Response(SpecializationResponseSerializer(specialization).data, status=status.HTTP_201_CREATED)

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    @Common().exception_handler
    def get(self, request, specialization_id=None):
        if specialization_id:
            specialization = DoctorSpecializations.get_specialization_by_id(specialization_id)
            if specialization:
                serializer = SpecializationResponseSerializer(specialization)
                return Response(serializer.data)
            return Response({"detail": "Specialization not found."}, status=status.HTTP_404_NOT_FOUND)
        specialization = DoctorSpecializations.get_all_specialization()
        serializer = SpecializationResponseSerializer(specialization, many=True)
        return Response(serializer.data)

    @Common().exception_handler
    def put(self, request, specialization_id):
        specialization = DoctorSpecializations.get_specialization_by_id(specialization_id)
        if not specialization:
            return Response({"detail": "Specialization not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SpecializationRequestSerializer(specialization, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @Common().exception_handler
    def delete(self, request, specialization_id):
        specialization = DoctorSpecializations.get_specialization_by_id(specialization_id)
        if not specialization:
            return Response({"detail": "Specialization not found."}, status=status.HTTP_404_NOT_FOUND)

        specialization.delete()
        return Response({"detail": "Specialization deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
