from django.db import models
from remedizz_apps.doctors.models.doctor import Doctor

class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='weekly_availability')
    
    appointment_type = models.CharField(max_length=20, choices=[
        ("Video Call", "Video Call"),
        ("Audio Call", "Audio Call"),
        ("Chat", "Chat"),
    ], null=True, blank=True)

    weekday = models.IntegerField(choices=[
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ])

    start_time = models.TimeField()
    end_time = models.TimeField()

    slot_duration = models.PositiveIntegerField(default=15, help_text="Duration of each slot in minutes")
    buffer_time = models.PositiveIntegerField(default=0, help_text="Gap after each slot in minutes")

    class Meta:
        unique_together = ('doctor', 'weekday', 'start_time', 'end_time')
        ordering = ['doctor', 'weekday', 'start_time']

    def get_weekday_display(self):
        weekday_mapping = {
            0: 'Monday',
            1: 'Tuesday',
            2: 'Wednesday',
            3: 'Thursday',
            4: 'Friday',
            5: 'Saturday',
            6: 'Sunday',
        }
        return weekday_mapping.get(self.weekday, 'Invalid Weekday')
    
    def __str__(self):
        return f"{self.doctor.name} - {self.get_weekday_display()} {self.start_time}-{self.end_time}"

    # Get schedule by doctor and weekday
    @staticmethod
    def get_schedule_by_day(doctor_id, weekday):
        return DoctorSchedule.objects.filter(doctor_id=doctor_id, weekday=weekday)

    # Get available slots for a specific day and appointment type
    @staticmethod
    def get_available_slots(doctor_id, date, appointment_type=None):
        # First filter by doctor and date
        weekday = date.weekday()  # Get the weekday (0-6, Monday to Sunday)
        
        # Query doctor schedule for that weekday
        schedule = DoctorSchedule.objects.filter(doctor_id=doctor_id, weekday=weekday)
        
        # Further filter by appointment type, if provided
        if appointment_type:
            schedule = schedule.filter(appointment_type=appointment_type)
        
        # Here, we will exclude the booked slots logic when the appointment module is ready
        return schedule

    # Get all available slots for a given date
    @staticmethod
    def get_slots_for_date(doctor_id, date, appointment_type=None):
        weekday = date.weekday()  # Get the weekday (0-6, Monday to Sunday)
        available_slots = DoctorSchedule.get_available_slots(doctor_id, date, appointment_type)
        
        # Here we could add additional logic to filter out already booked slots based on appointments
        return available_slots

class DoctorAvailabilityException(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="availability_exceptions")
    date = models.DateField()

    # Block full day or specify a blocked/opened time
    is_available = models.BooleanField(default=False)

    # Optional time range — if blank, applies to full day
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = ('doctor', 'date', 'start_time', 'end_time')
        ordering = ['doctor', 'date', 'start_time']

    def __str__(self):
        status = "Available" if self.is_available else "Unavailable"
        if self.start_time and self.end_time:
            return f"{self.doctor.name} - {self.date} ({status} from {self.start_time} to {self.end_time})"
        return f"{self.doctor.name} - {self.date} ({status} full day)"