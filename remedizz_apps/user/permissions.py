from rest_framework.permissions import BasePermission
from remedizz_apps.clinics.models import *


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user and getattr(request.user, "role", None) == "Doctor"


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user and getattr(request.user, "role", None) == "Patient"


class IsDigitalClinic(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.role == 'DigitalClinic'


class IsAuthenticatedUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
