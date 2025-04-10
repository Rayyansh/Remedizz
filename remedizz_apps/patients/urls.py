from django.urls import path
from remedizz_apps.patients.controllers import PatientController

urlpatterns = [
    path('', PatientController.get_patient, name='get_all_patients'),
    path('<int:patient_id>/', PatientController.get_patient, name='get_patient'),
    path('update/<int:patient_id>/', PatientController.update_patient, name='update_patient'),
    path('delete/<int:patient_id>/', PatientController.delete_patient, name='delete_patient'),
]


