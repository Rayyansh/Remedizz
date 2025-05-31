from rest_framework import serializers
from remedizz_apps.patients.models import Records



class PatientRecordRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Records
        fields = '__all__'

    def create(self, validated_data):
        return Records.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def validate(self, data):
        # Additional custom validation if needed
        return data
