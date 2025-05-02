from rest_framework import serializers
from remedizz_apps.doctors.models.doctor_availability import DoctorSchedule
from remedizz_apps.doctors.models.doctor import Doctor

class DoctorScheduleRequestSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(), required=False)

    class Meta:
        model = DoctorSchedule
        fields = ['doctor', 'appointment_type', 'weekday', 'start_time', 'end_time', 'slot_duration', 'buffer_time']

    def validate(self, data):
        # Custom validation logic if needed (e.g., ensuring start time < end time)
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("Start time must be before end time.")
        
        # Check if a schedule already exists with the same doctor, weekday, start_time, and end_time
        doctor_schedule_exists = DoctorSchedule.objects.filter(
            doctor=data.get('doctor'),
            weekday=data.get('weekday'),
            start_time=data.get('start_time'),
            end_time=data.get('end_time')
        ).exists()

        if doctor_schedule_exists:
            raise serializers.ValidationError("A schedule already exists with the same details.")
        
        return data
