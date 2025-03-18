from django.db import models
from remedizz_apps.user.models import User


class Doctor(models.Model):
    doctor_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    specialization = models.CharField(max_length=100, choices=[
        ("Cardiologist", "Cardiologist"),
        ("Dermatologist", "Dermatologist"),
        ("Neurologist", "Neurologist"),
    ])
    gender = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")])
    city = models.CharField(max_length=100)

    # Education
    qualification = models.CharField(max_length=255)
    college_name = models.CharField(max_length=255)
    college_passing_year = models.PositiveIntegerField()

    # Preferences
    preferred_language = models.CharField(max_length=100)
    terms_and_conditions_accepted = models.BooleanField(default=False)

    class Meta:
        db_table = 'doctor'

    def __str__(self):
        return self.doctor_id.username

class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="schedules")
    
    appointment_date = models.DateField()
    video_call_afternoon_slot = models.TimeField(null=True, blank=True)
    video_call_evening_slot = models.TimeField(null=True, blank=True)
    audio_call_afternoon_slot = models.TimeField(null=True, blank=True)
    audio_call_evening_slot = models.TimeField(null=True, blank=True)
    chat_afternoon_slot = models.TimeField(null=True, blank=True)
    chat_evening_slot = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.doctor.doctor_id} - {self.appointment_date}"



