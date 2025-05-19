from rest_framework import serializers
from remedizz_apps.doctors.models.doctor_availability import DoctorSchedule
from remedizz_apps.doctors.models.doctor import Doctor

class DoctorScheduleRequestSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(), required=False)

    class Meta:
        model = DoctorSchedule
        fields = ['appointment_type', 'weekday', 'start_time', 'end_time', 'slot_duration', 'buffer_time']

    def validate(self, data):
        user = data.get('doctor')
        print(user.id, user.pk)
        if user:
            doctor = Doctor.objects.filter(id=user.id).first()
            if not doctor:
                raise serializers.ValidationError("Doctor profile not found for this user.")
            data['doctor'] = doctor  # Replace user with doctor instance

        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("Start time must be before end time.")

        doctor_schedule_exists = DoctorSchedule.objects.filter(
            doctor=data.get('doctor'),
            weekday=data.get('weekday'),
            start_time=data.get('start_time'),
            end_time=data.get('end_time')
        ).exists()

        if doctor_schedule_exists:
            raise serializers.ValidationError("A schedule already exists with the same details.")

        return data
