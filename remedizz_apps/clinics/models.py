from django.db import models
from remedizz_apps.user.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from remedizz_apps.doctors.models.doctor import NameWithSpaceValidator
from remedizz_apps.specialization.models import DoctorSpecializations
from django.contrib.postgres.fields import ArrayField

class DigitalClinic(models.Model):
    digital_clinic_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name="clinic_profile")
    specialization = models.ManyToManyField("specialization.DoctorSpecializations", blank=True)
    available_service = models.CharField(max_length=20, null=True)
    operating_hours = models.CharField(max_length=20, null=True)
    username_validator = UnicodeUsernameValidator()
    owner_name = models.CharField(("username"),
        max_length=50,
        unique=True,
        help_text=(
            "Required. 20 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[NameWithSpaceValidator],
        error_messages={
            "unique": ("A user with that username already exists."),
        },
        null=True
    )
    clinic_name = models.CharField(("username"),
        max_length=50,
        unique=True,
        help_text=(
            "Required. 20 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[NameWithSpaceValidator],
        error_messages={
            "unique": ("A user with that username already exists."),
        },
        null=True
    )

    clinic_type = ArrayField(
        models.CharField(max_length=50),
        blank=True,
        null=True
    )
    address = models.TextField()
    website_url = models.CharField(null=True, blank=True)
    digital_clinic_email = models.EmailField(max_length=50, null=True, blank=True)

    terms_and_conditions_accepted = models.BooleanField(default=False) 
    clinic_profile_picture = models.ImageField(upload_to="clinic_profile_picture/", null=True, blank=True,
                                               max_length=50) 

    class Meta:
        db_table = 'digital_clinic'

    def __str__(self):
        return self.name


    @staticmethod
    def get_clinic_by_id(clinic_id):
        return DigitalClinic.objects.filter(digital_clinic_id=clinic_id).first()
    
    @staticmethod
    def get_all_clinics():
        return DigitalClinic.objects.all()
    
    @staticmethod
    def update_clinic(clinic_id, **kwargs):
        return DigitalClinic.objects.filter(digital_clinic_id=clinic_id).update(**kwargs)
    

    @staticmethod
    def create_clinic(clinic_id, **kwargs):
        clinic = DigitalClinic.objects.create(digital_clinic_id=clinic_id, **kwargs)
        return clinic
    
    @staticmethod
    def delete_clinic(clinic_id):
        return DigitalClinic.objects.filter(digital_clinic_id=clinic_id).delete()
    
# class DigitalClinicService(models.Model):
   
#     specialization_offered = models.CharField(max_length=20)
#     available_service = models.TextField()  # Can store multiple services as a comma-separated list
#     operating_hours = models.CharField(max_length=20)  # Example: "9 AM - 6 PM"

#     def __str__(self):
#         return f"{self.clinic.name} - {self.specialization_offered}"
    
#     @staticmethod
#     def get_services_by_clinic(clinic_id):
#         return DigitalClinicService.objects.filter(clinic_id=clinic_id)
    
#     @staticmethod
#     def get_service_by_id(service_id):
#         return DigitalClinicService.objects.filter(id=service_id).first()
    
#     @staticmethod
#     def update_service(service_id, **kwargs):
#         return DigitalClinicService.objects.filter(id=service_id).update(**kwargs)
    
#     @staticmethod
#     def create_service(clinic_id, **kwargs):
#         service = DigitalClinicService.objects.create(clinic_id=clinic_id, **kwargs)
#         return service
    
#     @staticmethod
#     def delete_service(service_id):
#         return DigitalClinicService.objects.filter(id=service_id).delete()


class DigitalClinicMedicalRecords(models.Model):
    digital_clinic_id = models.ForeignKey(DigitalClinic, on_delete=models.CASCADE, related_name="medical_records")
    medical_document = models.FileField(upload_to="medical_document/", null=True, blank=True)


    def __str__(self):
        return self.medical_document.name
    

    @staticmethod
    def get_medical_records_by_clinic(clinic_id):
        return DigitalClinicMedicalRecords.objects.filter(digital_clinic_id=clinic_id)
    
    @staticmethod
    def update_medical_records(clinic_id, **kwargs):
        return DigitalClinicMedicalRecords.objects.filter(digital_clinic_id=clinic_id).update(**kwargs)
    
    @staticmethod
    def create_medical_records(clinic_id, **kwargs):
        records = DigitalClinicMedicalRecords.objects.create(digital_clinic_id=clinic_id, **kwargs)
        return records
    
    @staticmethod
    def delete_medical_records(clinic_id):
        return DigitalClinicMedicalRecords.objects.filter(digital_clinic_id=clinic_id).delete()
    
    


class DigitalClinicPaymentInformation(models.Model):
    digital_clinic_id = models.ForeignKey(DigitalClinic, on_delete=models.CASCADE, related_name="payment_information")
    digital_clinic_bank_account_number = models.CharField(max_length=20)
    digital_clinic_bank_account_name = models.CharField(max_length=20, null=True)
    ifsc_code = models.CharField(max_length=11)
    uoi_id = models.CharField(max_length=50)

    def __str__(self):
        return self.digital_clinic_id.name
    
    @staticmethod
    def get_payment_info_by_clinic(clinic_id):
        return DigitalClinicPaymentInformation.objects.filter(digital_clinic_id=clinic_id).first()
    
    @staticmethod
    def update_payment_info(clinic_id, **kwargs):
        return DigitalClinicPaymentInformation.objects.filter(digital_clinic_id=clinic_id).update(**kwargs)
    
    @staticmethod
    def create_payment_info_by_id(payment_id, **kwargs):
      return DigitalClinicPaymentInformation.objects.create(id=payment_id, **kwargs)

   

    @staticmethod
    def delete_payment_info(clinic_id):
        return DigitalClinicPaymentInformation.objects.filter(digital_clinic_id=clinic_id).delete()

    @staticmethod
    def get_payment_info_by_id(payment_id):
        return DigitalClinicPaymentInformation.objects.filter(id=payment_id).first()
    
    @staticmethod
    def update_payment_info_by_id(payment_id, **kwargs):
        return DigitalClinicPaymentInformation.objects.filter(id=payment_id).update(**kwargs)
    
    @staticmethod
    def create_payment_info_by_id(payment_id, **kwargs):
        payment_info = DigitalClinicPaymentInformation.objects.create(id=payment_id, **kwargs)
        return payment_info
    
    @staticmethod
    def delete_payment_info_by_id(payment_id):
        return DigitalClinicPaymentInformation.objects.filter(id=payment_id).delete()
    
    
    