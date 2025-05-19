from django.urls import path
from remedizz_apps.appointments.controller import BookingController

urlpatterns = [
    # Retrieve all bookings for the authenticated user (patient or doctor)
    path('', BookingController.get_all_appointment, name='get_all_appointments'),

    # Retrieve a single booking by ID
    path('<int:appointment_id>/', BookingController.get_appointment, name='get_appointment'),

    # Create a new booking for a patient
    path('create/', BookingController.create_appointment, name='create_appointment'),

    # Get status of a booking by ID (Patient side)
    path('status/<int:appointment_id>/', BookingController.get_appointment_status, name='get_appointment_status'),

    # Fetch available slots for a doctor on a specific day
    path('available-slots/<int:doctor_id>/<str:date>/', BookingController.get_available_slots, name='get_available_slots'),

    path('upcoming_appointments/', BookingController.get_upcoming_appointments, name='upcoming-appointments'),
    path('patient_history/', BookingController.get_patient_history, name='doctor-patient-history'),
    path('patient_history/<int:patient_id>/', BookingController.get_patient_history_detail_for_doctor, name='doctor-patient-history-detail'
),
]