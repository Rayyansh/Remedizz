from rest_framework import serializers
from remedizz_apps.doctors.models.doctor import Education, WorkExperience, Doctor, RegistrationCouncil, DoctorMedicalRecords




class EducationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Education
        fields = ["id", "qualification", "college_name", "college_passing_year"]

class WorkExperienceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = WorkExperience
        fields = ["id", "job_profile", "company_name", "start_date", "end_date"]

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
    education = EducationSerializer(many=True)
    work_experience = WorkExperienceSerializer(many=True)

    class Meta:
        model = Doctor
        fields = [
            # Doctor Profile Fields
            "name", "specialization", "gender", "city", "doctor_contact_number",
            "doctor_email", "doctor_profile_picture", "education", "work_experience",
            "preferred_language", "terms_and_conditions_accepted",
            "registration_number", "registration_year", "registration_council",

            # Clinic Fields
            "clinic_name", "clinic_contact_number", "clinic_number", "clinic_timings", "opd_fees",
            "clinic_city", "clinic_locality", "clinic_street_address", "clinic_address", "clinic_pincode"
        ]

    def create(self, validated_data):
        education_data = validated_data.pop("education", [])
        work_experience_data = validated_data.pop("work_experience", [])

        doctor = Doctor.objects.create(**validated_data)

        for edu in education_data:
            edu_instance = Education.objects.create(**edu)
            doctor.education.add(edu_instance)

        for work in work_experience_data:
            work_instance = WorkExperience.objects.create(**work)
            doctor.work_experience.add(work_instance)

        return doctor

    def update(self, instance, validated_data):
        education_data = validated_data.pop("education", [])
        work_experience_data = validated_data.pop("work_experience", [])

        # === Update Doctor Fields ===
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # === Update Education ===
        existing_edu_ids = [edu.id for edu in instance.education.all()]
        incoming_edu_ids = []

        for edu in education_data:
            edu_id = edu.get("id")
            if edu_id and Education.objects.filter(id=edu_id).exists():
                edu_instance = Education.objects.get(id=edu_id)
                for attr, value in edu.items():
                    setattr(edu_instance, attr, value)
                edu_instance.save()
            else:
                edu_instance = Education.objects.create(**edu)
                instance.education.add(edu_instance)

            incoming_edu_ids.append(edu_instance.id)

        for edu in instance.education.all():
            if edu.id not in incoming_edu_ids:
                instance.education.remove(edu)
                edu.delete()

        # === Update Work Experience ===
        existing_work_ids = [work.id for work in instance.work_experience.all()]
        incoming_work_ids = []

        for work in work_experience_data:
            work_id = work.get("id")
            if work_id and WorkExperience.objects.filter(id=work_id).exists():
                work_instance = WorkExperience.objects.get(id=work_id)
                for attr, value in work.items():
                    setattr(work_instance, attr, value)
                work_instance.save()
            else:
                work_instance = WorkExperience.objects.create(**work)
                instance.work_experience.add(work_instance)

            incoming_work_ids.append(work_instance.id)

        for work in instance.work_experience.all():
            if work.id not in incoming_work_ids:
                instance.work_experience.remove(work)
                work.delete()

        return instance
    


class DoctorRecordRequestSerializer(serializers.ModelSerializer):
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(), write_only=True
    )

    class Meta:
        model = DoctorMedicalRecords
        fields = [
            "doctor_id",
            "medical_document",
        ]

class DoctorRecordUpdateItemSerializer(serializers.Serializer):
    record_id = serializers.IntegerField()
    medical_document = serializers.CharField()

class DoctorRecordBulkUpdateRequestSerializer(serializers.Serializer):
    doctor_id = serializers.IntegerField()
    updates = DoctorRecordUpdateItemSerializer(many=True)