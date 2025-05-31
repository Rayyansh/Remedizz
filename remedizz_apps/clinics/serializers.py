from rest_framework import serializers
from remedizz_apps.clinics.models import *
from remedizz_apps.user.models import User


class DigitalClinicServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalClinicService
        fields = ["specialization_offered", "available_service", "operating_hours"]


class ClinicRequestSerializer(serializers.ModelSerializer):
    services = DigitalClinicServiceSerializer(many=True)
    
    class Meta:
        model = DigitalClinic
        fields = [
            "name", "clinic_type", "address", "website_url", "digital_clinic_email",
            "services", "terms_and_conditions_accepted"
        ]

    def update(self, instance, validated_data):
        services_data = validated_data.pop("services", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if services_data:
            instance.services.clear()
            for service in services_data:
                service_instance, _ = DigitalClinicService.objects.get_or_create(**service)
                instance.services.add(service_instance)

        return instance

    
class ClinicResponseSerializer(serializers.ModelSerializer):
    # digital_clinic_id = serializers.IntegerField(source='id', read_only=True)
    services = DigitalClinicServiceSerializer(many=True, read_only=True)

    class Meta:
        model = DigitalClinic
        fields = [
            "digital_clinic_id", "name", "clinic_type", "address", "website_url", "digital_clinic_email",
            "services", "terms_and_conditions_accepted"
        ]


class ClinicMedicalRecordRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalClinicMedicalRecords
        fields = [
            "digital_clinic_name",
            "medical_document",
        ]



class ClinicMedicalRecordResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalClinicMedicalRecords
        fields = [
            "digital_clinic_name",
            "medical_document",
        ]


class ClinicPaymentInfoRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalClinicPaymentInformation
        fields = [
            "digital_clinic_name",
            "digital_clinic_bank_account_number",
            "ifsc_code",
            "uoi_id",
        ]

class ClinicPaymentInfoResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalClinicPaymentInformation
        fields = [
            "digital_clinic_name",
            "digital_clinic_bank_account_number",
            "ifsc_code",
            "uoi_id",
        ]