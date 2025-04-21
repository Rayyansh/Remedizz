from rest_framework import serializers
from remedizz_apps.specialization.models import DoctorSpecializations



class SpecializationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSpecializations
        fields = ['doctor_spcialization_name']

class SpecializationResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSpecializations
        fields = ['id', 'doctor_spcialization_name']
