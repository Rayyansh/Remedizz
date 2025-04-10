from rest_framework import serializers
from remedizz_apps.clinics.models import (
    DigitalClinic,
    DigitalClinicsService,
    # DigitalClinicMedicalRecords,
    # DigitalClinicPaymentInformation
)
from remedizz_apps.user.models import User


# ----------- SERVICE SERIALIZER -----------
class DigitalClinicServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalClinicsService
        fields = ['id', 'specialization_offered', 'available_service', 'operating_hours']


# ----------- REQUEST SERIALIZER -----------
class DigitalClinicRequestSerializer(serializers.ModelSerializer):
    digital_clinic_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role__iexact='digital_clinic')
    )
    services = DigitalClinicServiceSerializer(many=True)

    class Meta:
        model = DigitalClinic
        fields = [
            "digital_clinic_id",
            "name",
            "clinic_type",
            "address",
            "website_url",
            "digital_clinic_email",
            "services",
        ]

    def create(self, validated_data):
        services_data = validated_data.pop("services", [])
        clinic = DigitalClinic.objects.create(**validated_data)

        for service_data in services_data:
            service = DigitalClinicsService.objects.create(**service_data)
            clinic.services.add(service)

        return clinic

    def update(self, instance, validated_data):
        services_data = validated_data.pop("services", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if services_data is not None:
            instance.services.clear()
            for service_data in services_data:
                service = DigitalClinicsService.objects.create(**service_data)
                instance.services.add(service)

        return instance


# ----------- RESPONSE SERIALIZER -----------
class DigitalClinicResponseSerializer(serializers.ModelSerializer):
    digital_clinic_id = serializers.CharField(source="digital_clinic_id.username", read_only=True)
    services = DigitalClinicServiceSerializer(many=True)

    class Meta:
        model = DigitalClinic
        fields = [
            "id",
            "digital_clinic_id",
            "name",
            "clinic_type",
            "address",
            "website_url",
            "digital_clinic_email",
            "services"
        ]


# ----------- LIST SERIALIZER -----------
class DigitalClinicListSerializer(serializers.ModelSerializer):
    digital_clinic_id = serializers.CharField(source="digital_clinic_id.username", read_only=True)
    services = DigitalClinicServiceSerializer(many=True, read_only=True)

    class Meta:
        model = DigitalClinic
        fields = ["id", "digital_clinic_id", "name", "clinic_type", "services"]


# ----------- UPDATE SERIALIZER -----------
class DigitalClinicUpdateSerializer(serializers.ModelSerializer):
    services = DigitalClinicServiceSerializer(many=True, required=False)

    class Meta:
        model = DigitalClinic
        fields = ["name", "clinic_type", "address", "website_url", "digital_clinic_email", "services"]


# ----------- USER NESTED SERIALIZER -----------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'email', 'role']


# ----------- NESTED CLINIC SERIALIZER -----------
class DigitalClinicSerializer(serializers.ModelSerializer):
    digital_clinic_id = UserSerializer(read_only=True)
    services = DigitalClinicServiceSerializer(many=True, read_only=True)

    class Meta:
        model = DigitalClinic
        fields = ["digital_clinic_id", "services", "name", "clinic_type"]
