from django.urls import path
from remedizz_apps.clinics.controller import *

urlpatterns = [
    path('', ClinicController.get_clinic, name='get_all_clinicss'),
    path('<int:digital_clinic_id>/', ClinicController.get_clinic, name='get_clinic'),
    path('update/<int:digital_clinic_id>/', ClinicController.update_clinic, name='update_clinic'),
    path('delete/<int:digital_clinic_id>/', ClinicController.delete_clinic, name='delete_clinic'),

    # ClinicPaymentInfoController
    path('payment-info/', ClinicPaymentInfoController.get_payment_info, name='get_payment_info'),
    path('payment-info/create/', ClinicPaymentInfoController.create_payment_info, name='create_payment_info'),
    path('payment-info/update/<int:clinic_id>/', ClinicPaymentInfoController.update_payment_info, name='update_payment_info'),
    path('payment-info/delete/<int:clinic_id>/', ClinicPaymentInfoController.delete_payment_info, name='delete_payment_info'),

    # ClinicMedicalRecordsController
    path('medical-records/<int:clinic_id>/', ClinicMedicalRecordsController.get_medical_record, name='get_medical_records'),
    path('medical-records/create/', ClinicMedicalRecordsController.create_medical_record, name='create_medical_record'),
    path('medical-records/update/', ClinicMedicalRecordsController.update_medical_record, name='update_medical_record'),
    path('medical-records/delete/<int:clinic_id>/', ClinicMedicalRecordsController.delete_medical_record, name='delete_medical_record'),
]

