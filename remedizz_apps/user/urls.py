from django.urls import path
from remedizz_apps.user.controller import AuthController

urlpatterns = [
    path('', AuthController.auth_process, name='auth_process'),
    path('verify-otp/', AuthController.verify_otp, name='verify_otp'),
]
