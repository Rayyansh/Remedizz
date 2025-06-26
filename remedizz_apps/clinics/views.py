from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from remedizz_apps.clinics.models import *
from remedizz_apps.clinics.serializers import *
from remedizz_apps.common.common import Common
from remedizz_apps.user.permissions import IsDigitalClinic
from remedizz_apps.user.authentication import JWTAuthentication

class ClinicView(APIView):
    permission_classes = [IsAuthenticated, IsDigitalClinic]


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


class ClinicMedicalRecordsView(APIView):
    permission_classes = [IsAuthenticated, IsDigitalClinic]

    @Common().exception_handler
    def get(self, request, digital_clinic_id=None):
        digital_clinic_id = DigitalClinic.get_clinic_by_id(digital_clinic_id)
        records = DigitalClinicMedicalRecords.get_medical_records_by_clinic(digital_clinic_id)
        if not records:
            return Response({"error": "Medical record not found"}, status=status.HTTP_404_NOT_FOUND)

        medical_documents = [
            {str(record.id): record.medical_document.url if record.medical_document else None}
            for record in records
        ]

        grouped_data = {
            "digital_clinic_id": digital_clinic_id.digital_clinic_id.id,
            "medical_documents": medical_documents
        }

        serializer = ClinicMedicalRecordGroupedSerializer(grouped_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @Common().exception_handler
    def post(self, request):
        user, _ = JWTAuthentication().authenticate(request)
        clinic = DigitalClinic.get_clinic_by_id(user.id)
        print(clinic.pk)
        data = request.data.copy()
        data['digital_clinic_id'] = clinic.pk

        serializer = ClinicMedicalRecordRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @Common().exception_handler
    def put(self, request):
        serializer = ClinicRecordBulkUpdateRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        clinic_id = serializer.validated_data["digital_clinic_id"]
        updates = serializer.validated_data["updates"]

        clinic = DigitalClinic.get_clinic_by_id(clinic_id)
        if not clinic:
            return Response({"error": "Clinic not found"}, status=status.HTTP_404_NOT_FOUND)

        updated_records = []

        for item in updates:
            record_id = item["record_id"]
            medical_document = item["medical_document"]

            record = DigitalClinicMedicalRecords.objects.filter(id=record_id, digital_clinic_id=clinic).first()
            if not record:
                continue

            record.medical_document = medical_document
            record.save()
            updated_records.append(record)

        response_serializer = ClinicMedicalRecordResponseSerializer(updated_records, many=True)
        return Response(
            {
                "status": True,
                "message": f"{len(updated_records)} record(s) updated successfully",
                "data": response_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


    @Common().exception_handler
    def delete(self, request, clinic_id):
        digital_clinic_id = DigitalClinic.get_clinic_by_id(clinic_id)

        deleted, _ = DigitalClinicMedicalRecords.delete_medical_records(digital_clinic_id)
        if not deleted:
            return Response({"error": "Medical record not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Medical record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ClinicPaymentInfoView(APIView):
    permission_classes = [IsAuthenticated, IsDigitalClinic]

    @Common().exception_handler
    def get(self, request, digital_clinic_id=None):
        digital_clinic_id = DigitalClinic.get_clinic_by_id(digital_clinic_id)
        payment = DigitalClinicPaymentInformation.get_payment_info_by_clinic(digital_clinic_id)
        if not payment:
            return Response({"error": "Payment info not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ClinicPaymentInfoResponseSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @Common().exception_handler
    def post(self, request, digital_clinic_id=None):
        serializer = ClinicPaymentInfoRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(Digital_clinic_name_id=digital_clinic_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @Common().exception_handler
    def put(self, request, digital_clinic_id):
        digital_clinic_id = DigitalClinic.get_clinic_by_id(digital_clinic_id)
        payment = DigitalClinicPaymentInformation.get_payment_info_by_clinic(digital_clinic_id)
        if not payment:
            return Response({"error": "Payment info not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ClinicPaymentInfoRequestSerializer(payment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(ClinicPaymentInfoResponseSerializer(payment).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @Common().exception_handler
    def delete(self, request, digital_clinic_id):
        digital_clinic_id = DigitalClinic.get_clinic_by_id(digital_clinic_id)        
        deleted, _ = DigitalClinicPaymentInformation.delete_payment_info(digital_clinic_id)
        if not deleted:
            return Response({"error": "Payment info not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Payment info deleted successfully"}, status=status.HTTP_204_NO_CONTENT)