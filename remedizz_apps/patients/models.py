import datetime
from django.db import models
from django.db.models import Q
from django.utils import timezone

from remedizz_apps.user.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator

class Patient(models.Model):
    patient_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_profile")
    username_validator = UnicodeUsernameValidator()
    name = models.CharField(("username"),
        max_length=20,
        unique=True,
        help_text=(
            "Required. 20 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": ("A user with that username already exists."),
        },
        null=True
    )
    date_of_birth = models.DateField(null=True)
    address = models.TextField(null=True)
    record = models.FileField(upload_to="patients/records/", null=True, blank=True, max_length=30)
    prescription = models.FileField(upload_to="patients/prescriptions/", null=True, blank=True, max_length=30)
    reports = models.FileField(upload_to="patients/reports/", null=True, blank=True, max_length=30)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'patient'

    def __str__(self):
        return self.name

    @staticmethod
    def get_patient_by_id(patient_id):
        return Patient.objects.filter(patient_id=patient_id).first()
    
    @staticmethod
    def get_all_patients():
        return Patient.objects.all()
    
    @staticmethod
    def update_patient(patient_id, **kwargs):
        return Patient.objects.filter(patient_id=patient_id).update(**kwargs)
    
    @staticmethod
    def delete_patient(patient_id):
        return Patient.objects.filter(patient_id=patient_id).delete()

