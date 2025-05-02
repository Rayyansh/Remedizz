from django.db import models
from django.db import models, IntegrityError

class Appointment(models.Model):
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)  # Use string reference
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE, related_name='bookings')  # Use string reference
    schedule = models.ForeignKey('doctors.DoctorSchedule', on_delete=models.CASCADE, related_name='bookings')  # Use string reference
    appointment_date = models.DateField()  # ➕ This tracks the actual day (e.g., "2025-04-25")
    appointment_time = models.TimeField(null=True)
    symptoms = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('doctor', 'schedule', 'appointment_date', 'appointment_time')  # Add appointment_time

    def __str__(self):
        return f"{self.patient} booked {self.doctor} on {self.appointment_date} ({self.schedule})"

    @staticmethod
    def create_appointment(patient, doctor, schedule, appointment_date, appointment_time, symptoms=None):
        # Check for slot conflict
        if Appointment.objects.filter(
            doctor=doctor,
            schedule=schedule,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        ).exists():
            raise IntegrityError("This time slot is already booked for the selected doctor.")

        return Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            schedule=schedule,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            symptoms=symptoms
        )
    
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
    
    @staticmethod
    def get_booked_slots(doctor_id, schedule_id, appointment_date):
        return Appointment.objects.filter(
            doctor_id=doctor_id,
            schedule_id=schedule_id,
            appointment_date=appointment_date
        ).values_list('appointment_time', flat=True)
    


 
