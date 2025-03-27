from django.urls import path
from remedizz_apps.user.controller import AuthController

urlpatterns = [
    path('', AuthController.auth_process, name='auth_process'),
    path('verify-otp/', AuthController.verify_otp, name='verify_otp'),
    # path('doctor/', AuthController.doctor_view, name='doctor_view'),
    # path('patient/', AuthController.patient_view, name='patient_view'),
    # path('digital-clinic/', AuthController.digital_clinic_view, name='digital_clinic_view'),
]
