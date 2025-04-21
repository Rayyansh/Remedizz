from rest_framework import serializers
from remedizz_apps.patients.models import Patient
from remedizz_apps.gender.models import Gender
from remedizz_apps.city.models import City


class PatientRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    date_of_birth = serializers.DateField()
    address = serializers.CharField()
    gender = serializers.PrimaryKeyRelatedField(queryset=Gender.objects.all())
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    record = serializers.FileField(required=False, allow_null=True)
    prescription = serializers.FileField(required=False, allow_null=True)
    reports = serializers.FileField(required=False, allow_null=True)

    def create(self, validated_data):
        return Patient.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def validate(self, data):
        # Additional custom validation if needed
        return data
