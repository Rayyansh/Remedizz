from django.db import models
from remedizz_apps.user.models import User


class DigitalClinic(models.Model):
    digital_clinic_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name="clinic_profile")
    name = models.CharField(max_length=255)
    clinic_type = models.CharField(max_length=255)
    address = models.TextField()
    website_url = models.URLField(null=True, blank=True)

    class Meta:
        db_table = 'digital_clinic'

    def __str__(self):
        return self.digital_clinic_id.username



class DigitalClinicService(models.Model):
    clinic = models.ForeignKey(DigitalClinic, on_delete=models.CASCADE, related_name="services")
    specialization_offered = models.CharField(max_length=255)
    available_service = models.TextField()  # Can store multiple services as a comma-separated list
    operating_hours = models.CharField(max_length=255)  # Example: "9 AM - 6 PM"

    def __str__(self):
        return f"{self.clinic.name} - {self.specialization_offered}"
