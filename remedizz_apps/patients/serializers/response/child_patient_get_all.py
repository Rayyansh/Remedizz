from rest_framework import serializers
from remedizz_apps.patients.models import ChildPatient


class ChildPatientResponseSerializer(serializers.ModelSerializer):
    parent_id = serializers.IntegerField(source="parent.id", read_only=True)
    parent_name = serializers.CharField(source="parent.name", read_only=True)
    gender = serializers.SlugRelatedField(read_only=True, slug_field='gender_name')
    city = serializers.SlugRelatedField(read_only=True, slug_field='city_name')
    

    class Meta:
        model = ChildPatient
        fields = [
            'id', 'name', 'gender', 'city', 'date_of_birth', 'address',
            'record', 'prescription', 'reports',
            'created_at', 'updated_at',
            'parent_id', 'parent_name'
        ]