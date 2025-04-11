from django.urls import path
from remedizz_apps.patients.controllers import PatientController, ChildPatientController

urlpatterns = [
    path('', PatientController.get_patient, name='get_all_patients'),
    path('<int:patient_id>/', PatientController.get_patient, name='get_patient'),
    path('update/<int:patient_id>/', PatientController.update_patient, name='update_patient'),
    path('delete/<int:patient_id>/', PatientController.delete_patient, name='delete_patient'),

    path('child/', ChildPatientController.create_child),
    path('child/all/', ChildPatientController.get_children),
    path('child/<int:child_id>/', ChildPatientController.get_children),
    path('child/update/<int:child_id>/', ChildPatientController.update_child),
    path('child/delete/<int:child_id>/', ChildPatientController.delete_child),
]


