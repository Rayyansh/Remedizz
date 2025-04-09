from django.db import models
from remedizz_apps.user.models import User


class Doctor(models.Model):
    doctor_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    specialization = models.CharField(max_length=20, choices=[
        ("Cardiologist", "Cardiologist"),
        ("Dermatologist", "Dermatologist"),
        ("Neurologist", "Neurologist"),
    ])
    gender = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")])
    city = models.CharField(max_length=20)
    doctor_contact_number = models.CharField(max_length=15, null=True, blank=True)
    doctor_email = models.EmailField(max_length=30, null=True, blank=True)
    doctor_profile_picture = models.ImageField(upload_to="doctor_profile_pictures/", null=True, blank=True,
                                               max_length=30)
    education = models.ForeignKey('Education', on_delete=models.CASCADE, related_name="doctor_education", null=True)
    work_experience = models.ForeignKey('WorkExperience', on_delete=models.CASCADE, related_name="doctor_experience",
                                        null=True)

    # Preferences
    preferred_language = models.CharField(max_length=15)
    terms_and_conditions_accepted = models.BooleanField(default=False)

    # registration information
    registration_number = models.CharField(max_length=50, null=True, blank=True)
    registration_year = models.DateField(null=True)
    registration_council = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'doctor'

    def __str__(self):
        return self.doctor_id.username
    


    @staticmethod
    def get_doctor_by_id(doctor_id):
        return Doctor.objects.filter(doctor_id=doctor_id).first()
    
    
    @staticmethod
    def get_all_doctors():
        return Doctor.objects.all()
    
    @staticmethod
    def update_doctor(doctor_id, **kwargs):
        return Doctor.objects.filter(id=doctor_id).update(**kwargs)
    
    @staticmethod
    def delete_doctor(doctor_id):
        return Doctor.objects.filter(id=doctor_id).first()


class Education(models.Model):
    qualification = models.CharField(max_length=50)
    college_name = models.CharField(max_length=50)
    college_passing_year = models.DateField()


class WorkExperience(models.Model):
    job_profile = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()


class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="schedules")
    appointment_type = models.CharField(max_length=20, choices=[
        ("Video Call", "Video Call"),
        ("Audio Call", "Audio Call"),
        ("Chat", "Chat"),
    ], null=True)

    appointment_date = models.DateField(null=True)
    slot = models.TimeField(null=True)

    def __str__(self):
        return f"{self.doctor.doctor_id} - {self.appointment_date} - {self.slot}"
