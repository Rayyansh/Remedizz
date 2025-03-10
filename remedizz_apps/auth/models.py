from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


class AppTemplate(models.Model):
    pass

    class Meta:
        db_table = 'app_template'

    def create(self) -> int:
        pass

    @staticmethod
    def get() -> list:
        pass

    @staticmethod
    def remove() -> None:
        pass

    @staticmethod
    def update() -> None:
        pass


# ====================================================================================================

class User(AbstractUser):
    USER_ROLE_CHOICES = [
        ('Patient', 'Patient'),
        ('Doctor', 'Doctor'),
        ('Digital Clinic', 'Digital Clinic'),
    ]
    user_role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES)
    contact_number = models.CharField(max_length=15, unique=True)
    profile_picture = models.ImageField(upload_to='profiles_pictures/', blank=True, null=True)

    def __str__(self):
        return self.username


# ==================================================================================================
class PatientProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=200)

    patient_date_of_birth = models.DateField()
    patient_address = models.TextField()

    def __str__(self):
        return self.patient_name


# =================================================================================================

# master table for doctor profile
class RegistrationCouncil(models.Model):
    registration_council_name = models.CharField(max_length=255)

    def __str__(self):
        return self.registration_council_name


class Languages(models.Model):
    language_name = models.CharField(max_length=150)

    def __str__(self):
        return self.language_name


class DoctorInformation(models.Model):
    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'digital_clinic'})
    doctor_name = models.CharField(max_length=200)
    doctor_email = models.EmailField(unique=True)
    doctor_gender = models.CharField(max_length=20, choices=GENDER)
    doctor_city = models.CharField(max_length=255)
    terms_and_conditions = models.BooleanField(default=False, help_text='I agree terms and conditions!')

    def __str__(self):
        return f'Doctor information of {self.doctor_name}'


class DoctorEducationInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor_name = models.ForeignKey(DoctorInformation, on_delete=models.CASCADE)
    doctor_qualification = models.CharField(max_length=200)
    doctor_college_name = models.TextField()
    doctor_college_passing_year = models.DateField()
    doctor_speciality = models.CharField(max_length=255)

    def __str__(self):
        return f'Education information of {self.doctor_name}'


class DoctorClinicInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    doctor_name = models.ForeignKey(DoctorInformation, on_delete=models.CASCADE)
    clinic_name = models.CharField(max_length=255)

    clinic_contact_number = models.CharField(max_length=15)
    clinic_alternate_number = models.CharField(max_length=15)

    clinic_time = models.CharField(max_length=15)
    opd_fees = models.DecimalField(max_digits=8, decimal_places=2)

    clinic_city = models.CharField(max_length=200)
    clinic_locality = models.CharField(max_length=200)
    clinic_street_address = models.TextField()
    clinic_address = models.TextField()

    clinic_pincode = models.CharField(max_length=6)

    def __str__(self):
        return f'Clinic information of {self.doctor_name}'


class DoctorRegistrationInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor_name = models.ForeignKey(DoctorInformation, on_delete=models.CASCADE)
    doctor_registration_number = models.CharField(max_length=200)
    doctor_registration_council = models.ForeignKey(RegistrationCouncil, on_delete=models.CASCADE)
    doctor_registration_year = models.DateField()

    def __str__(self):
        return f'Registration information for {self.doctor_name}'


class DoctorClinicProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor_name = models.ForeignKey(DoctorInformation, on_delete=models.CASCADE)
    doctor_preferred_language = models.ForeignKey(Languages, on_delete=models.CASCADE)
    choose_appointment_date = models.DateField()
    video_call_afternoon_slot = models.TimeField()
    video_evening_slot = models.TimeField()
    audio_call_afternoon_slot = models.TimeField()
    audio_call_evening_slot = models.TimeField()
    chat_afternoon_slot = models.TimeField()
    chat_evening_slot = models.TimeField()

    def __str__(self):
        return f'Clinic profile for {self.doctor_name}'


# =========================================================================================================

# master tables for digital clinic profile

class DigitalClinicType(models.Model):
    digital_clinic_type = models.CharField(max_length=200)

    def __str__(self):
        return self.digital_clinic_type


class DigitalClinicSpecialisation(models.Model):
    specialisation_name = models.CharField(max_length=200)

    def __str__(self):
        return self.specialisation_name


class DigitalClinicAvailableService(models.Model):
    available_services = models.CharField(max_length=200)

    def __str__(self):
        return self.available_services


class DigitalClinicOperationHours(models.Model):
    operation_hours = models.CharField(max_length=200)

    def __str__(self):
        return self.operation_hours


class DigitalClinicProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    digital_clinic_name = models.CharField(max_length=200)
    digital_clinic_type = models.ForeignKey(DigitalClinicType, on_delete=models.CASCADE)
    digital_clinic_address = models.TextField()
    digital_clinic_contact_number = models.CharField(max_length=15)
    digital_clinic_website_url = models.CharField(max_length=255)
    digital_clinic_email = models.EmailField(unique=True)

    def __str__(self):
        return self.digital_clinic_name


class DigitalClinicSpecialisationAndServices(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    digital_clinic_name = models.CharField(max_length=200)
    specialization_offered = models.ForeignKey(DigitalClinicSpecialisation, on_delete=models.CASCADE)
    available_service = models.ForeignKey(DigitalClinicAvailableService, on_delete=models.CASCADE)
    operating_hours = models.ForeignKey(DigitalClinicOperationHours, on_delete=models.CASCADE)

    def __str__(self):
        return f'Specialisation offered details for {self.digital_clinic_name}'


class DigitalClinicMedicalRecords(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    digital_clinic_name = models.CharField(max_length=200)
    digital_clinic_lab_certificates = models.FileField(upload_to='digital_clinic_lab_certificates/')
    digital_clinic_pharmacy_licence = models.FileField(upload_to='digital_clinic_pharmacy_licence/')

    def __str__(self):
        return f'Medical records details for {self.digital_clinic_name}'


class DigitalClinicPaymentInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    digital_clinic_name = models.CharField(max_length=200)
    digital_clinic_bank_account_number = models.CharField(max_length=200)
    ifsc_code = models.CharField(max_length=200)
    upi_id = models.CharField(max_length=200)

    def __str__(self):
        return f'Bank details of {self.digital_clinic_bank_account_number}'

# ================================================================================================================
