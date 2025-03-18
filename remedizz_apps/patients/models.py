from django.db import models
from remedizz_apps.user.models import User


class Patient(models.Model):
    patient_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_profile")
    date_of_birth = models.DateField()
    address = models.TextField()
    record = models.FileField(upload_to="patients/records/", null=True, blank=True)
    prescription = models.FileField(upload_to="patients/prescriptions/", null=True, blank=True)
    reports = models.FileField(upload_to="patients/reports/", null=True, blank=True)

    class Meta:
        db_table = 'patient'

    def __str__(self):
        return self.patient_id.username


