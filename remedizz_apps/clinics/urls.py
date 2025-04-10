from django.urls import path
from remedizz_apps.clinics.controller import ClinicController

urlpatterns = [
    path('', ClinicController.get_clinic, name='get_all_clinics'),  # GET all
    path('<int:clinic_id>/', ClinicController.get_clinic, name='get_clinic'),  # GET single
    path('create/', ClinicController.create_clinic, name='create_clinic'),
    path('update/<int:clinic_id>/', ClinicController.update_clinic, name='update_clinic'),
    path('delete/<int:clinic_id>/', ClinicController.delete_clinic, name='delete_clinic'),
]

