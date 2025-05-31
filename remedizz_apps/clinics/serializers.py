from rest_framework import serializers
from remedizz_apps.clinics.models import *
from remedizz_apps.user.models import User


class DigitalClinicServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalClinicService
        fields = ["specialization_offered", "available_service", "operating_hours"]


class ClinicRequestSerializer(serializers.ModelSerializer):
    services = DigitalClinicServiceSerializer(many=True)
    owner_name = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = DigitalClinic
        fields = [
            "clinic_name", "clinic_type", "address", "website_url", "digital_clinic_email",
            "services", "terms_and_conditions_accepted", "clinic_profile_picture", "owner_name"
        ]

    def update(self, instance, validated_data):
        services_data = validated_data.pop("services", [])
        owner_name = validated_data.pop("owner_name", None)


        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update username of related User
        if owner_name:
            user = instance.digital_clinic_id
            user.owner_name = owner_name
            user.save()

        if services_data:
            instance.services.clear()
            for service in services_data:
                service_instance, _ = DigitalClinicService.objects.get_or_create(**service)
                instance.services.add(service_instance)

        return instance

    
class ClinicResponseSerializer(serializers.ModelSerializer):
    digital_clinic_username = serializers.CharField(source='digital_clinic_id.username', read_only=True)
    services = DigitalClinicServiceSerializer(many=True, read_only=True)

    class Meta:
        model = DigitalClinic
        fields = [
            "digital_clinic_username", "clinic_name", "clinic_type", "address", "website_url", "digital_clinic_email",
            "services", "terms_and_conditions_accepted", "clinic_profile_picture"
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