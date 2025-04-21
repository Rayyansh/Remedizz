from rest_framework import serializers
from remedizz_apps.patients.models import Patient


class PatientResponseSerializer(serializers.ModelSerializer):
    gender = serializers.SlugRelatedField(read_only=True, slug_field='gender_name')
    city = serializers.SlugRelatedField(read_only=True, slug_field='city_name')

    class Meta:
        model = Patient
        fields = ["patient_id", "gender", "city", "name", "date_of_birth", "address", "record", "prescription", "reports", "created_at",
                  "updated_at"]