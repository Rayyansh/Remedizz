from rest_framework import serializers
from remedizz_apps.patients.models import Patient, Records


class PatientRecordResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Records
        fields = '__all__'

class PatientResponseSerializer(serializers.ModelSerializer):
    gender = serializers.SlugRelatedField(read_only=True, slug_field='gender_name')
    city = serializers.SlugRelatedField(read_only=True, slug_field='city_name')
    records = PatientRecordResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = ["patient_id", "gender", "city", "name", "date_of_birth", "address", "created_at",
                  "updated_at", "records"]