from django.urls import path
from remedizz_apps.doctors.controller import DoctorController, RegistrationCouncilController, DoctorScheduleController, DoctorRecordsController

urlpatterns = [

    # Doctor profile crud

    path('', DoctorController.get_doctor, name='get_all_doctors'),
    path('<int:doctor_id>/', DoctorController.get_doctor, name='get_doctor'),
    path('update/<int:doctor_id>/', DoctorController.update_doctor, name='update_doctor'),
    path('delete/<int:doctor_id>/', DoctorController.delete_doctor, name='delete_doctor'),

    # Doctor search with doctor name or with speciality

    path('search/', DoctorController.search_doctors, name='search_doctors'), 

    # Doctor Schedule URLS
    path('schedule/', DoctorScheduleController.get_doctor_schedule, name='get_doctor_schedule'),
    path('schedule/<int:weekday>/', DoctorScheduleController.get_doctor_schedule, name='get_doctor_schedule_by_weekday'),
    path('schedule/create/', DoctorScheduleController.create_doctor_schedule, name='create_doctor_schedule'),
    path('schedule/update/<int:schedule_id>/', DoctorScheduleController.update_doctor_schedule, name='update_doctor_schedule'),
    path('schedule/delete/<int:schedule_id>/', DoctorScheduleController.delete_doctor_schedule, name='delete_doctor_schedule'),
    
    # Registration Council urls

    path('registration/council/create/', RegistrationCouncilController.create_registration_council, name='create_registration_council'),  # create
    path('registration/council/', RegistrationCouncilController.get_registration_council, name='registration_council_list_create'),  # get all
    path('registration/council/<int:registration_council_id>/', RegistrationCouncilController.get_registration_council, name='registration_council_retrieve'),  # get specific
    path('registration/council/update/<int:registration_council_id>/', RegistrationCouncilController.update_registration_council, name='update_registration_council'),  # update
    path('registration/council/delete/<int:registration_council_id>/', RegistrationCouncilController.delete_registration_council, name='delete_registration_council'),  # delete

    # ClinicMedicalRecordsController
    path('medical-records/', DoctorRecordsController.get_medical_record, name='get_medical_records'),
    path('medical-records/create/', DoctorRecordsController.create_medical_record, name='create_medical_record'),
    path('medical-records/update/<int:clinic_id>/', DoctorRecordsController.update_medical_record, name='update_medical_record'),
    path('medical-records/delete/<int:clinic_id>/', DoctorRecordsController.delete_medical_record, name='delete_medical_record'),
]

