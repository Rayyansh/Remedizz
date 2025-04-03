from rest_framework import serializers
from remedizz_apps.patients.models import Patient
from remedizz_apps.user.models import User


class PatientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["date_of_birth", "address", "record", "prescription", "reports"]


class PatientResponseSerializer(serializers.ModelSerializer):
    patient_id = serializers.CharField(source="patient_id.username")

    class Meta:
        model = Patient
        fields = ["patient_id", "date_of_birth", "address", "record", "prescription", "reports", "created_at", "updated_at"]


class PatientListSerializer(serializers.ModelSerializer):
    patient_id = serializers.CharField(source="patient_id.username")

    class Meta:
        model = Patient
        fields = ["patient_id", "date_of_birth", "address"]



class PatientRequestSerializer(serializers.Serializer):
    patient_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='patient'))
    date_of_birth = serializers.DateField()
    address = serializers.CharField()
    record = serializers.FileField(required=False, allow_null=True)
    prescription = serializers.FileField(required=False, allow_null=True)
    reports = serializers.FileField(required=False, allow_null=True)

    def validate(self, data):
        # Additional custom validation if needed
        return data


class PatientResponseSerializer(serializers.ModelSerializer):
    patient_id = serializers.CharField(source='patient_id.username')

    class Meta:
        model = Patient
        fields = ['patient_id', 'date_of_birth', 'address', 'record', 'prescription', 'reports', 'created_at', 'updated_at']
