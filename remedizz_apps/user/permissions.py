from rest_framework.permissions import BasePermission

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'doctor'

class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'patient'

class IsDigitalClinic(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'digital_clinic'

class IsAuthenticatedUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
