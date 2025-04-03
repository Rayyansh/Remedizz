from django.db import models
from remedizz_apps.user.models import User


class DigitalClinic(models.Model):
    digital_clinic_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name="clinic_profile")
    name = models.CharField(max_length=30)
    clinic_type = models.CharField(max_length=30)
    address = models.TextField()
    website_url = models.URLField(null=True, blank=True)
    digital_clinic_email = models.EmailField(max_length=20 , null=True, blank=True)

    class Meta:
        db_table = 'digital_clinic'

    def __str__(self):
        return self.digital_clinic_id.username



class DigitalClinicService(models.Model):
    clinic = models.ForeignKey(DigitalClinic, on_delete=models.CASCADE, related_name="services")
    specialization_offered = models.CharField(max_length=20)
    available_service = models.TextField()  # Can store multiple services as a comma-separated list
    operating_hours = models.CharField(max_length=20)  # Example: "9 AM - 6 PM"

    def __str__(self):
        return f"{self.clinic.name} - {self.specialization_offered}"
    


class DigitalClinicMedicalRecords(models.Model):
    digital_clinic_name = models.ForeignKey(DigitalClinic, on_delete=models.CASCADE, related_name="medical_records")
    digital_lab_certificates = models.FileField(upload_to="digital_lab_certificates/", null=True, blank=True)
    digital_clinic_pharmacy_licence = models.FileField(upload_to="digital_clinic_pharmacy_licence/", null=True, blank=True)

    def __str__(self):
        return self.digital_clinic_name.name


class DigitalClinicPaymentInformation(models.Model):
    Digital_clinic_name = models.ForeignKey(DigitalClinic, on_delete=models.CASCADE, related_name="payment_information")
    Digital_clinic_bank_account_number = models.CharField(max_length=20)
    ifsc_code = models.CharField(max_length=10)
    uoi_id = models.CharField(max_length=10) 

    def __str__(self):
        return self.Digital_clinic_name.name   
