from rest_framework import serializers
from remedizz_apps.doctors.models.doctor_availability import DoctorSchedule
from remedizz_apps.doctors.models.doctor import Doctor

class DoctorScheduleRequestSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(), required=False)

    class Meta:
        model = DoctorSchedule
        fields = ['doctor','appointment_type', 'weekday', 'start_time', 'end_time', 'slot_duration', 'buffer_time']

    def validate(self, data):
        # No need to check doctor here, it's read-only and set by view.
        if data.get('start_time') and data.get('end_time') and data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("Start time must be before end time.")

        # Check for duplicate schedule
        doctor = self.instance.doctor if self.instance else None  # get doctor from instance on update
        weekday = data.get('weekday', self.instance.weekday if self.instance else None)
        start_time = data.get('start_time', self.instance.start_time if self.instance else None)
        end_time = data.get('end_time', self.instance.end_time if self.instance else None)

        if DoctorSchedule.objects.filter(
            doctor=doctor,
            weekday=weekday,
            start_time=start_time,
            end_time=end_time
        ).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("A schedule already exists with the same details.")

        return data
