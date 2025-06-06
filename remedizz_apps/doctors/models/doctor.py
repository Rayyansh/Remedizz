from django.db import models
from remedizz_apps.user.models import User
from remedizz_apps.gender.models import Gender
from remedizz_apps.city.models import City
from remedizz_apps.appointments.models import Appointment
from remedizz_apps.specialization.models import DoctorSpecializations
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone

# ======================================== REGISTRATION COUNCIL TABLE ================================================

class RegistrationCouncil(models.Model):
    registration_council_name = models.CharField(max_length=255)

    def __str__(self):
        return self.registration_council_name
      
    @staticmethod
    def get_registration_council_by_id(registration_council_id):
        return RegistrationCouncil.objects.filter(id=registration_council_id).first()

    @staticmethod
    def get_all_registration_council():
        return RegistrationCouncil.objects.all()

    @staticmethod
    def update_registration_council(registration_council_id, **kwargs):
        return RegistrationCouncil.objects.filter(id=registration_council_id).update(**kwargs)

    @staticmethod
    def delete_registration_council(registration_council_id):
        return RegistrationCouncil.objects.filter(id=registration_council_id).delete()

# ======================================== REGISTRATION COUNCIL TABLE ================================================

class Doctor(models.Model):
    doctor_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
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
    
    specialization = models.ForeignKey(DoctorSpecializations, on_delete=models.CASCADE, blank=True, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    doctor_contact_number = models.CharField(max_length=15, null=True, blank=True)
    doctor_email = models.EmailField(max_length=30, null=True, blank=True)
    doctor_profile_picture = models.ImageField(upload_to="doctor_profile_pictures/", null=True, blank=True,
                                               max_length=50)
    education = models.ManyToManyField('Education', related_name="doctors", blank=True)
    work_experience = models.ManyToManyField('WorkExperience', related_name="doctors", blank=True)


    # Preferences
    preferred_language = models.CharField(max_length=15)
    terms_and_conditions_accepted = models.BooleanField(default=False)

    # registration information
    registration_number = models.CharField(max_length=50, null=True, blank=True)
    registration_year = models.DateField(null=True) 
    registration_council = models.ForeignKey(RegistrationCouncil, on_delete=models.CASCADE, null=True)

    # Clinic Fields
    clinic_name = models.CharField(max_length=100, null=True, blank=True)
    clinic_contact_number = models.CharField(max_length=15, null=True, blank=True)
    clinic_number = models.CharField(max_length=20, null=True, blank=True)
    clinic_timings = models.CharField(max_length=100, null=True, blank=True)
    opd_fees = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    clinic_city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name="clinic_city")
    clinic_locality = models.CharField(max_length=100, null=True, blank=True)
    clinic_street_address = models.CharField(max_length=255, null=True, blank=True)
    clinic_address = models.CharField(max_length=255, null=True, blank=True)
    clinic_pincode = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = 'doctor'

    def __str__(self):
        return self.name

    


    @staticmethod
    def get_doctor_by_id(doctor_id):
        return Doctor.objects.filter(doctor_id=doctor_id).first()
    
    
    @staticmethod
    def get_all_doctors():
        return Doctor.objects.all()
    
    @staticmethod
    def update_doctor(doctor_id, **kwargs):
        return Doctor.objects.filter(doctor_id=doctor_id).update(**kwargs)
    
    @staticmethod
    def delete_doctor(doctor_id):
        return Doctor.objects.filter(doctor_id=doctor_id).first()
    
    @staticmethod
    def get_upcoming_appointments(doctor_id):
        doctor = Doctor.objects.filter(doctor_id=doctor_id).first()
        if doctor:
            return Appointment.objects.filter(
                doctor=doctor,
                status="Pending",
                scheduled_at__gte=timezone.now()  # Assuming there is a field for the scheduled date/time
            )
        return None

    @staticmethod
    def confirm_appointment(doctor_id, appointment_id):
        doctor = Doctor.objects.filter(doctor_id=doctor_id).first()
        if doctor:
            appointment = Appointment.objects.filter(id=appointment_id, doctor=doctor, status="Pending").first()
            if appointment:
                appointment.status = 'Confirmed'
                appointment.save()
                return True
        return False


class Education(models.Model):
    qualification = models.CharField(max_length=50)
    college_name = models.CharField(max_length=50)
    college_passing_year = models.DateField()


class WorkExperience(models.Model):
    job_profile = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()

class DoctorMedicalRecords(models.Model):
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="medical_records")
    medical_document = models.FileField(upload_to="medical_document/", null=True, blank=True)


    def __str__(self):
        return self.medical_document.name
    

    @staticmethod
    def get_medical_records_by_doctor(doctor_id):
        return DoctorMedicalRecords.objects.filter(doctor_id=doctor_id)
    
    @staticmethod
    def update_medical_records(doctor_id, **kwargs):
        return DoctorMedicalRecords.objects.filter(doctor_id=doctor_id).update(**kwargs)
    
    @staticmethod
    def create_medical_records(doctor_id, **kwargs):
        records = DoctorMedicalRecords.objects.create(doctor_id=doctor_id, **kwargs)
        return records
    
    @staticmethod
    def delete_medical_records(doctor_id):
        return DoctorMedicalRecords.objects.filter(doctor_id=doctor_id).delete()
    