from django.urls import path
from remedizz_apps.clinics.controller import *

urlpatterns = [
    path('', ClinicController.get_clinic, name='get_all_clinicss'),
    path('<int:digital_clinic_id>/', ClinicController.get_clinic, name='get_clinic'),
    path('update/<int:digital_clinic_id>/', ClinicController.update_clinic, name='update_clinic'),
    path('delete/<int:digital_clinic_id>/', ClinicController.delete_clinic, name='delete_clinic'),
]

