from django.urls import path
from remedizz_apps.doctors.controller import DoctorController, RegistrationCouncilController, DoctorScheduleController

urlpatterns = [

    # Doctor profile crud

    # path('create/', DoctorController.create_doctor, name='create_doctor'),
    path('', DoctorController.get_doctor, name='get_all_doctors'),
    path('<int:doctor_id>/', DoctorController.get_doctor, name='get_doctor'),
    path('update/<int:doctor_id>/', DoctorController.update_doctor, name='update_doctor'),
    path('delete/<int:doctor_id>/', DoctorController.delete_doctor, name='delete_doctor'),

    # Doctor search with doctor name or with speciality

    path('search/', DoctorController.search_doctors, name='search_doctors'), 

    # Doctor-specific appointment actions
    # path('appointments/upcoming/', DoctorController.get_upcoming_appointments, name='doctor-upcoming-appointments'),
    # path('appointments/confirm/<int:appointment_id>/', DoctorController.confirm_appointment, name='doctor-confirm-appointment'),

    # Doctor Schedule URLS
    path('schedule/', DoctorScheduleController.get_doctor_schedule, name='get_doctor_schedule'),
    path('schedule/<int:weekday>/', DoctorScheduleController.get_doctor_schedule, name='get_doctor_schedule_by_weekday'),
    path('schedule/create/', DoctorScheduleController.create_doctor_schedule, name='create_doctor_schedule'),
    path('schedule/update/<int:schedule_id>/', DoctorScheduleController.update_doctor_schedule, name='update_doctor_schedule'),
    path('schedule/delete/<int:schedule_id>/', DoctorScheduleController.delete_doctor_schedule, name='delete_doctor_schedule'),
    
    # Registration Council urls

    path('registration/council/create/', RegistrationCouncilController.create_registration_council, name='create_registration_council'),  # create
    path('registration/council/', RegistrationCouncilController.get_all_registration_council, name='registration_council_list_create'),  # get all
    path('registration/council/<int:registration_council_id>/', RegistrationCouncilController.get_registration_council_by_id, name='registration_council_retrieve'),  # get specific
    path('registration/council/update/<int:registration_council_id>/', RegistrationCouncilController.update_registration_council, name='update_registration_council'),  # update
    path('registration/council/delete/<int:registration_council_id>/', RegistrationCouncilController.delete_registration_council, name='delete_registration_council'),  # delete
]

