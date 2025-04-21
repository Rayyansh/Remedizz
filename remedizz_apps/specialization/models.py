from django.db import models

# Create your models here.
 

class DoctorSpecializations(models.Model):
    doctor_spcialization_name = models.CharField(max_length=150)

    def __str__(self):
        return self.doctor_spcialization_name

    @staticmethod
    def get_specialization_by_id(specialization_id):
        return DoctorSpecializations.objects.filter(id=specialization_id).first()

    @staticmethod
    def get_all_specialization():
        return DoctorSpecializations.objects.all()

    @staticmethod
    def update_specialization(specialization_id, **kwargs):
        return DoctorSpecializations.objects.filter(id=specialization_id).update(**kwargs)

    @staticmethod
    def delete_specialization(specialization_id):
        return DoctorSpecializations.objects.filter(id=specialization_id).delete()
