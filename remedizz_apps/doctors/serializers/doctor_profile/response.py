from rest_framework import serializers
from remedizz_apps.doctors.models.doctor import Doctor, RegistrationCouncil
from remedizz_apps.doctors.serializers.doctor_profile.request import EducationSerializer, WorkExperienceSerializer

class RegistrationCouncilResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationCouncil
        fields = ['id', 'registration_council_name']
        
class DoctorResponseSerializer(serializers.ModelSerializer):
    education = EducationSerializer(many=True)
    work_experience = WorkExperienceSerializer(many=True)

    specialization = serializers.SlugRelatedField(read_only=True, slug_field='doctor_spcialization_name')
    gender = serializers.SlugRelatedField(read_only=True, slug_field='gender_name')
    city = serializers.SlugRelatedField(read_only=True, slug_field='city_name')
    registration_council = serializers.SlugRelatedField(read_only=True, slug_field='registration_council_name')

    class Meta:
        model = Doctor
        fields = [
            "doctor_id", "name", "specialization", "gender", "city", "doctor_contact_number",
            "doctor_email", "doctor_profile_picture", "education", "work_experience",
            "preferred_language", "terms_and_conditions_accepted",
            "registration_number", "registration_year", "registration_council", 
        ]