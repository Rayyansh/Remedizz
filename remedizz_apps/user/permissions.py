from rest_framework.permissions import BasePermission


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.role == 'doctor'


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user and getattr(request.user, "role", None) == "Patient"


class IsDigitalClinic(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.role == 'digital_clinic'


class IsAuthenticatedUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
