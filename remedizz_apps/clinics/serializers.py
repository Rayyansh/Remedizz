from rest_framework import serializers
from remedizz_apps.clinics.models import *
from remedizz_apps.user.models import User


# class DigitalClinicServiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DigitalClinicService
#         fields = ["specialization_offered", "available_service", "operating_hours"]


class ClinicRequestSerializer(serializers.ModelSerializer):
    specialization = serializers.PrimaryKeyRelatedField(
        many=True, queryset=DoctorSpecializations.objects.all(), required=False
    )
    clinic_type = serializers.ListField(child=serializers.CharField(max_length=50), required=False)

    # services = DigitalClinicServiceSerializer(many=True)
    phone_number = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = DigitalClinic
        fields = [
            "clinic_name", "owner_name", "clinic_type", "address", "website_url", "digital_clinic_email",
            "specialization","available_service", "operating_hours", "terms_and_conditions_accepted", "clinic_profile_picture", "owner_name", "phone_number"
        ]

    def update(self, instance, validated_data):
        phone_number = validated_data.pop("phone_number", None)
        specialization_data = validated_data.pop("specialization", None)
        clinic_type_data = validated_data.pop("clinic_type", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if specialization_data is not None:
            instance.specialization.set(specialization_data)

        if clinic_type_data is not None:
            instance.clinic_type = clinic_type_data

        instance.save()

        user = instance.digital_clinic_id
        if phone_number:
            user.phone_number = phone_number
            user.username = phone_number
            user.save()

        return instance


class ClinicResponseSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='digital_clinic_id.phone_number', read_only=True)

    class Meta:
        model = DigitalClinic
        fields = [
            "digital_clinic_id", "owner_name", "phone_number", "clinic_name", "clinic_type", "address", "website_url", "digital_clinic_email",
            "specialization","available_service", "operating_hours", "terms_and_conditions_accepted", "clinic_profile_picture"
        ]


class ClinicMedicalRecordRequestSerializer(serializers.ModelSerializer):
    digital_clinic_id = serializers.PrimaryKeyRelatedField(
        queryset=DigitalClinic.objects.all(), write_only=True
    )

    class Meta:
        model = DigitalClinicMedicalRecords
        fields = [
            "digital_clinic_id",
            "medical_document",
        ]

class ClinicRecordUpdateItemSerializer(serializers.Serializer):
    record_id = serializers.IntegerField()
    medical_document = serializers.CharField()

class ClinicRecordBulkUpdateRequestSerializer(serializers.Serializer):
    digital_clinic_id = serializers.IntegerField()
    updates = ClinicRecordUpdateItemSerializer(many=True)


class ClinicMedicalRecordResponseSerializer(serializers.ModelSerializer):
    digital_clinic_id = serializers.IntegerField(source="digital_clinic_id.digital_clinic_id.id", read_only=True)


    class Meta:
        model = DigitalClinicMedicalRecords
        fields = [
            "digital_clinic_id",
            "medical_document",
        ]

class ClinicMedicalRecordGroupedSerializer(serializers.Serializer):
    digital_clinic_id = serializers.IntegerField()
    medical_documents = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )

class ClinicPaymentInfoRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalClinicPaymentInformation
        fields = [
            "digital_clinic_id",
            "digital_clinic_bank_account_name",
            "digital_clinic_bank_account_number",
            "ifsc_code",
            "uoi_id",
        ]

class ClinicPaymentInfoResponseSerializer(serializers.ModelSerializer):
    digital_clinic_id = serializers.IntegerField(source="digital_clinic_id.digital_clinic_id.id", read_only=True)
    
    class Meta:
        model = DigitalClinicPaymentInformation
        fields = [
            "digital_clinic_id",
            "digital_clinic_bank_account_name",
            "digital_clinic_bank_account_number",
            "ifsc_code",
            "uoi_id",
        ]