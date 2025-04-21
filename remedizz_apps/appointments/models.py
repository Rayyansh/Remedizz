from django.db import models
from remedizz_apps.doctors.models import DoctorSchedule, Doctor
from remedizz_apps.patients.models import Patient

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='bookings')
    schedule = models.ForeignKey(DoctorSchedule, on_delete=models.CASCADE, related_name='bookings',null=True, blank=True)
    symptoms = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} booked {self.doctor} on {self.schedule}"

    @staticmethod
    def get_appointment_by_id(appointment_id):
        return Appointment.objects.select_related("patient__patient_id").filter(id=appointment_id).first()

    
    @staticmethod
    def get_all_appointment():
        return Appointment.objects.all()
    
    @staticmethod
    def update_appointment(appointment_id, **kwargs):
        return Appointment.objects.filter(id=appointment_id).update(**kwargs)
    
    @staticmethod
    def delete_appointment(appointment_id):
        return Appointment.objects.filter(id=appointment_id).delete()


    @staticmethod
    def get_appointment_status(appointment_id):
            return Appointment.objects.select_related("patient", "doctor").filter(id=appointment_id).first()
        # return Booking.objects.filter(id=booking_id).first()



 
