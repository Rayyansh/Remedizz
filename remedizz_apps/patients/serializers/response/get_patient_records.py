from rest_framework import serializers
from remedizz_apps.patients.models import Records

class PatientRecordResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Records
        fields = '__all__'
