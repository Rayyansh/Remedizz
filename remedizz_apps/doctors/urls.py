from django.urls import path
from remedizz_apps.doctors.controller import DoctorController

urlpatterns = [
    # path('create/', DoctorController.create_doctor, name='create_doctor'),
    path('', DoctorController.get_doctor, name='get_all_doctors'),
    path('<int:doctor_id>/', DoctorController.get_doctor, name='get_doctor'),
    path('update/<int:doctor_id>/', DoctorController.update_doctor, name='update_doctor'),
    path('delete/<int:doctor_id>/', DoctorController.delete_doctor, name='delete_doctor'),
]

