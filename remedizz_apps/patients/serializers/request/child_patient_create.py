from rest_framework import serializers
from remedizz_apps.patients.models import Patient



class ChildPatientRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    date_of_birth = serializers.DateField()
    address = serializers.CharField(required=False, allow_blank=True)
    record = serializers.FileField(required=False, allow_null=True)
    prescription = serializers.FileField(required=False, allow_null=True)
    reports = serializers.FileField(required=False, allow_null=True)

    def validate(self, data):
        return data