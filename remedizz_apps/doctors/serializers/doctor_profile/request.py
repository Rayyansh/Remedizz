from rest_framework import serializers
from remedizz_apps.doctors.models.doctor import Education, WorkExperience, Doctor, RegistrationCouncil



class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ["qualification", "college_name", "college_passing_year"]


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = ["job_profile", "company_name", "start_date", "end_date"]

class DoctorSearchSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor_id.username', read_only=True)

    class Meta:
        model = Doctor
        fields = ['doctor_name', 'specialization']

class RegistrationCouncilRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationCouncil
        fields = ['registration_council_name']


class DoctorRequestSerializer(serializers.ModelSerializer):
    education = EducationSerializer()
    work_experience = WorkExperienceSerializer()

    class Meta:
        model = Doctor
        fields = [ 
            "name","specialization", "gender", "city", "doctor_contact_number",
            "doctor_email", "doctor_profile_picture", "education", "work_experience",
            "preferred_language", "terms_and_conditions_accepted",
            "registration_number", "registration_year", "registration_council"
        ]

    def update(self, instance, validated_data):
        education_data = validated_data.pop("education", None)
        work_experience_data = validated_data.pop("work_experience", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Education
        if education_data:
            if instance.education:
                for attr, value in education_data.items():
                    setattr(instance.education, attr, value)
                instance.education.save()
            else:
                education = Education.objects.create(**education_data)
                instance.education = education
                instance.save()

        # Work Experience
        if work_experience_data:
            if instance.work_experience:
                for attr, value in work_experience_data.items():
                    setattr(instance.work_experience, attr, value)
                instance.work_experience.save()
            else:
                work_experience = WorkExperience.objects.create(**work_experience_data)
                instance.work_experience = work_experience
                instance.save()

        return instance
    
