import datetime
from django.db import models
from django.db.models import Q
from django.utils import timezone

from remedizz_apps.user.models import User
from remedizz_apps.gender.models import Gender
from remedizz_apps.city.models import City
from remedizz_apps.doctors.models import *
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
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    address = models.TextField(null=True)
    record = models.FileField(upload_to="patients/records/", null=True, blank=True, max_length=30)
    prescription = models.FileField(upload_to="patients/prescriptions/", null=True, blank=True, max_length=30)
    reports = models.FileField(upload_to="patients/reports/", null=True, blank=True, max_length=30)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    patient_profile_picture = models.ImageField(upload_to="patient_profile_pictures/", null=True, blank=True,
                                               max_length=50)

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

class ChildPatient(models.Model):
    parent = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='children')
    name = models.CharField(max_length=30)
    relation = models.CharField(max_length=30, null=True)
    date_of_birth = models.DateField()
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    record = models.FileField(upload_to="patients/child/records/", null=True, blank=True, max_length=30)
    prescription = models.FileField(upload_to="patients/child/prescriptions/", null=True, blank=True, max_length=30)
    reports = models.FileField(upload_to="patients/child/reports/", null=True, blank=True, max_length=30)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'child_patient'

    def __str__(self):
        return f"{self.name} (Child of {self.parent.name})"

    def __str__(self):
        return f"{self.name} (Child of {self.parent.name})"

    @staticmethod
    def get_by_id(child_id, parent):
        return ChildPatient.objects.filter(id=child_id, parent=parent).first()

    @staticmethod
    def get_all_by_parent(parent):
        return ChildPatient.objects.filter(parent=parent)

    @staticmethod
    def update_child(child_id, parent, **kwargs):
        return ChildPatient.objects.filter(id=child_id, parent=parent).update(**kwargs)

    @staticmethod
    def delete_child(child_id, parent):
        return ChildPatient.objects.filter(id=child_id, parent=parent).delete()


# ==========================================================================================================

