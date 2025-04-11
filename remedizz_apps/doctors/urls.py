from django.urls import path
from remedizz_apps.doctors.controller import DoctorController

urlpatterns = [

    # Doctor profile crud

    # path('create/', DoctorController.create_doctor, name='create_doctor'),
    path('', DoctorController.get_doctor, name='get_all_doctors'),
    path('<int:doctor_id>/', DoctorController.get_doctor, name='get_doctor'),
    path('update/<int:doctor_id>/', DoctorController.update_doctor, name='update_doctor'),
    path('delete/<int:doctor_id>/', DoctorController.delete_doctor, name='delete_doctor'),

    # Doctor search with doctor name or with speciality

    path('search/', DoctorController.search_doctors, name='search_doctors'), 
]

