from rest_framework import serializers
from remedizz_apps.doctors.models import *
from remedizz_apps.user.models import User


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ["qualification", "college_name", "college_passing_year"]


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = ["job_profile", "company_name", "start_date", "end_date"]


class DoctorScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSchedule
        fields = ["appointment_type", "appointment_date", "slot"]

# =========================================================================================================

class DoctorResponseSerializer(serializers.ModelSerializer):
    doctor_id = serializers.IntegerField(source='id', read_only=True)
    education = EducationSerializer()
    work_experience = WorkExperienceSerializer()
    schedules = DoctorScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = Doctor
        fields = [
            "doctor_id", "name", "specialization", "gender", "city", "doctor_contact_number",
            "doctor_email", "doctor_profile_picture", "education", "work_experience",
            "preferred_language", "terms_and_conditions_accepted", "registration_number",
            "registration_year", "registration_council", "schedules"
        ]


class DoctorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "specialization", "gender", "city", "doctor_contact_number",
            "doctor_email", "doctor_profile_picture", "education",
            "work_experience", "preferred_language",
            "terms_and_conditions_accepted", "registration_number",
            "registration_year", "registration_council"
        ]


class DoctorListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = ["specialization", "city"]


class DoctorRequestSerializer(serializers.ModelSerializer):
    education = EducationSerializer()
    work_experience = WorkExperienceSerializer()
    schedules = DoctorScheduleSerializer(many=True)

    class Meta:
        model = Doctor
        fields = [
            "specialization", "gender", "city", "doctor_contact_number",
            "doctor_email", "doctor_profile_picture", "education", "work_experience",
            "schedules", "preferred_language", "terms_and_conditions_accepted",
            "registration_number", "registration_year", "registration_council"
        ]
    
    def update(self, instance, validated_data):
        education_data = validated_data.pop("education", None)
        work_experience_data = validated_data.pop("work_experience", None)
        schedules_data = validated_data.pop("schedules", None)

        # Update simple Doctor fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle education
        if education_data:
            if instance.education:
                for attr, value in education_data.items():
                    setattr(instance.education, attr, value)
                instance.education.save()
            else:
                education = Education.objects.create(**education_data)
                instance.education = education
                instance.save()

        # Handle work experience
        if work_experience_data:
            if instance.work_experience:
                for attr, value in work_experience_data.items():
                    setattr(instance.work_experience, attr, value)
                instance.work_experience.save()
            else:
                work_experience = WorkExperience.objects.create(**work_experience_data)
                instance.work_experience = work_experience
                instance.save()

        # Handle schedules
        if schedules_data is not None:
            instance.schedules.all().delete()
            for schedule in schedules_data:
                DoctorSchedule.objects.create(doctor=instance, **schedule)

        return instance




