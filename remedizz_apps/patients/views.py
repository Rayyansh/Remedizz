from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from remedizz_apps.patients.models import Patient, ChildPatient, Records
from remedizz_apps.patients.serializers.request.patient_create import PatientRequestSerializer
from remedizz_apps.patients.serializers.request.patient_records_create import PatientRecordRequestSerializer
from remedizz_apps.patients.serializers.response.patient_get_all import PatientResponseSerializer
from remedizz_apps.patients.serializers.request.child_patient_create import ChildPatientRequestSerializer
from remedizz_apps.patients.serializers.response.child_patient_get_all import ChildPatientResponseSerializer
from remedizz_apps.patients.serializers.response.get_patient_records import PatientRecordResponseSerializer
from remedizz_apps.common.common import Common
from remedizz_apps.user.permissions import IsPatient
from remedizz_apps.user.authentication import JWTAuthentication

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

    @Common().exception_handler
    def create_patient_records(self, request):
        user, _ = JWTAuthentication().authenticate(request)
        patient = Patient.get_patient_by_id(user.id)
        request.data['patient'] = patient.pk

        serializer = PatientRecordRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Patient Record created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @Common().exception_handler
    def get_patient_records(self, request):
        user, _ = JWTAuthentication().authenticate(request)
        patient = Patient.get_patient_by_id(user.id)

        records = Records.objects.filter(patient=patient)
        serializer = PatientRecordResponseSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update_patient_records(self, request, record_id):
        user, _ = JWTAuthentication().authenticate(request)
        patient = Patient.get_patient_by_id(user.id)
        if not patient:
            return Response({"error": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)

        record = Records.get_record_by_id_and_patient(record_id, patient)
        if not record:
            return Response({"error": "Record not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PatientRecordRequestSerializer(record, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(PatientRecordResponseSerializer(record).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @Common().exception_handler
    def delete_patient_records(self, request, record_id):
        user, _ = JWTAuthentication().authenticate(request)
        patient = Patient.get_patient_by_id(user.id)
        if not patient:
            return Response({"error": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)

        record = Records.get_record_by_id_and_patient(record_id, patient)
        if not record:
            return Response({"error": "Record not found."}, status=status.HTTP_404_NOT_FOUND)

        record.delete()
        return Response({"message": "Record deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class ChildPatientView(APIView):
    permission_classes = [IsAuthenticated, IsPatient]

    @Common().exception_handler
    def post(self, request):
        parent = request.user.patient_profile
        serializer = ChildPatientRequestSerializer(data=request.data)
        if serializer.is_valid():
            ChildPatient.objects.create(parent=parent, **serializer.validated_data)
            return Response({"message": "Child patient created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @Common().exception_handler
    def get(self, request, member_id=None):
        parent = request.user.patient_profile
        if member_id:
            child = ChildPatient.get_by_id(member_id, parent)
            if not child:
                return Response({"error": "Child patient not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = ChildPatientResponseSerializer(child)
            return Response(serializer.data, status=status.HTTP_200_OK)

        children = ChildPatient.get_all_by_parent(parent)
        serializer = ChildPatientResponseSerializer(children, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @Common().exception_handler
    def put(self, request, member_id):
        parent = request.user.patient_profile
        child = ChildPatient.get_by_id(member_id, parent)
        if not child:
            return Response({"error": "Child patient not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChildPatientRequestSerializer(child, data=request.data, partial=True)
        if serializer.is_valid():
            for attr, value in serializer.validated_data.items():
                setattr(child, attr, value)
            child.save()
            return Response(ChildPatientResponseSerializer(child).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @Common().exception_handler
    def delete(self, request, member_id):
        parent = request.user.patient_profile
        child = ChildPatient.get_by_id(member_id, parent)
        if not child:
            return Response({"error": "Child patient not found."}, status=status.HTTP_404_NOT_FOUND)
        child.delete()
        return Response({"message": "Child patient deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

