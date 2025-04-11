from rest_framework import serializers
from remedizz_apps.patients.models import Patient


class PatientResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = ["patient_id", "name", "date_of_birth", "address", "record", "prescription", "reports", "created_at",
                  "updated_at"]