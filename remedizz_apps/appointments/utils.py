from datetime import datetime, timedelta
from remedizz_apps.appointments.models import Appointment

def generate_available_slots(schedule, appointment_date, booked_slots):
    slots = []
    start_time = datetime.combine(appointment_date, schedule.start_time)
    end_time = datetime.combine(appointment_date, schedule.end_time)

    while start_time + timedelta(minutes=15) <= end_time:
        slot_start = start_time.time()
        if slot_start not in booked_slots:
            slots.append(str(slot_start))
        start_time += timedelta(minutes=15)

    return slots

def get_available_slots(doctor, schedule, appointment_date):
    """
    Get available appointment slots for a doctor on a specific date.
    It excludes booked slots and checks against the doctor's schedule.
    """
    # Get all existing appointments for the doctor, schedule, and appointment_date
    booked_appointments = Appointment.objects.filter(
        doctor=doctor,
        schedule=schedule,
        appointment_date=appointment_date
    )

    # Get all time slots from the doctor's schedule
    available_slots = []
    schedule_start_time = schedule.start_time
    schedule_end_time = schedule.end_time
    slot_duration = schedule.slot_duration  # Assuming the slot duration is provided in minutes

    current_time = schedule_start_time
    while current_time < schedule_end_time:
        # Check if the current slot is already booked
        if not booked_appointments.filter(appointment_time=current_time).exists():
            available_slots.append(current_time)
        current_time += timedelta(minutes=slot_duration)

    return available_slots

def check_slot_availability(doctor, schedule, appointment_date, appointment_time):
    """
    Check if a specific time slot is available for the doctor on the given appointment date.
    """
    # Ensure that the appointment time is within the schedule's available range
    available_slots = get_available_slots(doctor, schedule, appointment_date)
    
    # Check if the requested time slot is available
    if appointment_time not in available_slots:
        return False  # Slot is not available

    return True