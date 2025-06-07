from rest_framework import serializers
from remedizz_apps.doctors.models.doctor import Doctor, RegistrationCouncil, DoctorMedicalRecords
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
    doctor_contact_number = serializers.SerializerMethodField()

    def get_doctor_contact_number(self, obj):
        return obj.doctor_id.phone_number if obj.doctor_id else None
    
    class Meta:
        model = Doctor
        fields = [
            # Doctor Profile
            "doctor_id", "name", "specialization", "gender", "city", "doctor_contact_number",
            "doctor_email", "doctor_profile_picture", "education", "work_experience",
            "preferred_language", "terms_and_conditions_accepted",
            "registration_number", "registration_year", "registration_council",

            # Clinic Info
            "clinic_name", "clinic_contact_number", "clinic_number", "clinic_timings", "opd_fees",
            "clinic_city", "clinic_locality", "clinic_street_address", "clinic_address", "clinic_pincode"
        ]

class DoctorRecordResponseSerializer(serializers.ModelSerializer):
    doctor_id = serializers.IntegerField(source="doctor_id.doctor_id.id", read_only=True)

    class Meta:
        model = DoctorMedicalRecords
        fields = [
            "doctor_id",
            "medical_document",
        ]

class DoctorMedicalRecordGroupedSerializer(serializers.Serializer):
    doctor_id = serializers.IntegerField()
    medical_documents = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )