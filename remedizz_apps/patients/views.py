from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from remedizz_apps.patients.models import Patient
from remedizz_apps.patients.serializers import PatientRequestSerializer, PatientResponseSerializer
from remedizz_apps.common.common import Common
from remedizz_apps.user.permissions import IsPatient


class PatientView(APIView):
    permission_classes = [IsAuthenticated, IsPatient]

    @Common().exception_handler
    def get(self, request, patient_id=None):
        """
        Retrieve a single patient if patient_id is provided, else retrieve all patients.
        """
        if patient_id:
            patient = Patient.get_patient_by_id(patient_id)
            if not patient:
                return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = PatientResponseSerializer(patient)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Get all patients
        patients = Patient.get_all_patients()
        serializer = PatientResponseSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @Common().exception_handler
    def put(self, request, patient_id):
        """Update patient profile"""
        patient = Patient.get_patient_by_id(patient_id)
        if not patient:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PatientRequestSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(PatientResponseSerializer(patient).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @Common().exception_handler
    def delete(self, request, patient_id):
        """Delete patient profile"""
        patient = Patient.get_patient_by_id(patient_id)
        if not patient:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        patient.delete()
        return Response({"message": "Patient deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
