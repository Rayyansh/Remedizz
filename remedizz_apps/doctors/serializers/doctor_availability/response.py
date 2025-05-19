from rest_framework import serializers
from remedizz_apps.doctors.models.doctor_availability import DoctorSchedule
from remedizz_apps.doctors.models.doctor import Doctor

class DoctorResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = ['doctor_id', 'name']

class DoctorScheduleResponseSerializer(serializers.ModelSerializer):
    doctor = DoctorResponseSerializer()

    class Meta:
        model = DoctorSchedule
        fields = ['id', 'doctor', 'appointment_type', 'weekday', 'start_time', 'end_time', 'slot_duration', 'buffer_time']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Using the custom get_weekday_display method to get the full weekday name
        representation['weekday_name'] = instance.get_weekday_display()
        return representation