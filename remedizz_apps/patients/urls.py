from django.urls import path
from remedizz_apps.patients.controllers import PatientController, ChildPatientController

urlpatterns = [
    path('', PatientController.get_patient, name='get_all_patients'),
    path('<int:patient_id>/', PatientController.get_patient, name='get_patient'),
    path('update/<int:patient_id>/', PatientController.update_patient, name='update_patient'),
    path('delete/<int:patient_id>/', PatientController.delete_patient, name='delete_patient'),

    # Patient medical record routes
    path('records/', PatientController.get_patient_records, name='get_patient_records'),
    path('records/create/', PatientController.create_patient_record, name='create_patient_record'),
    path('records/update/<int:record_id>/', PatientController.update_patient_records, name='update_patient_record'),
    path('records/delete/<int:record_id>/', PatientController.delete_patient_records, name='delete_patient_record'),

    path('members/', ChildPatientController.create_child),
    path('members/all/', ChildPatientController.get_children),
    path('members/<int:members_id>/', ChildPatientController.get_children),
    path('members/update/<int:members_id>/', ChildPatientController.update_child),
    path('members/delete/<int:members_id>/', ChildPatientController.delete_child),
]


