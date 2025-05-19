from rest_framework import serializers
from .models import Appointment
from remedizz_apps.doctors.models.doctor import Doctor
from remedizz_apps.doctors.models.doctor_availability import DoctorSchedule
from remedizz_apps.doctors.serializers.doctor_availability.request import DoctorScheduleRequestSerializer
from remedizz_apps.doctors.serializers.doctor_profile.response import DoctorResponseSerializer
from remedizz_apps.patients.models import Patient
import datetime


class BookingRequestSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())
    appointment_date = serializers.DateField()
    appointment_time = serializers.TimeField()

    class Meta:
        model = Appointment
        fields = ['id','doctor', 'appointment_date', 'appointment_time', 'symptoms', 'status']

    def validate(self, data):
        doctor = data.get('doctor')
        appointment_date = data.get('appointment_date')
        appointment_time = data.get('appointment_time')

        # Get all schedules for the doctor on the same weekday
        schedules = DoctorSchedule.objects.filter(doctor=doctor, weekday=appointment_date.weekday())

        if not schedules.exists():
            raise serializers.ValidationError("No schedules found for the doctor on this day.")

        # Find a schedule that covers the requested time
        matched_schedule = None
        for schedule in schedules:
            if schedule.start_time <= appointment_time < schedule.end_time:
                matched_schedule = schedule
                break

        if not matched_schedule:
            raise serializers.ValidationError("No matching schedule found for the selected time.")

        # Check for duplicate booking
        if Appointment.objects.filter(
            doctor=doctor,
            schedule=matched_schedule,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        ).exists():
            raise serializers.ValidationError("This time slot is already booked for the selected date.")

        # Inject the resolved schedule into validated data
        data['schedule'] = matched_schedule
        data['status'] = data.get('status', 'Pending')

        return data

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        appointment_date = validated_data.get('appointment_date', instance.appointment_date)
        appointment_time = validated_data.get('appointment_time', instance.appointment_time)

        if appointment_date < datetime.now().date():
            raise serializers.ValidationError("Cannot update past appointments.")
        if appointment_date == datetime.now().date() and appointment_time < datetime.now().time():
            raise serializers.ValidationError("Cannot update booking for a time that has passed.")

        # Check for time slot conflict if updated
        doctor = validated_data.get('doctor', instance.doctor)
        schedule = validated_data.get('schedule', instance.schedule)

        if Appointment.objects.filter(
            doctor=doctor,
            schedule=schedule,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        ).exclude(id=instance.id).exists():
            raise serializers.ValidationError("This time slot is already booked for the selected date.")

        instance.appointment_date = appointment_date
        instance.appointment_time = appointment_time
        instance.symptoms = validated_data.get('symptoms', instance.symptoms)
        instance.status = validated_data.get('status', instance.status)
        instance.schedule = validated_data.get('schedule', instance.schedule)
        instance.save()
        return instance
    

class BookingResponseSerializer(serializers.ModelSerializer):
    doctor_id = serializers.IntegerField(source='doctor.id')
    patient_id = serializers.IntegerField(source='patient.id')
    schedule_id = serializers.IntegerField(source='doctor.id')
    appointment_date = serializers.DateField(format="%Y-%m-%d")
    appointment_time = serializers.TimeField()

    class Meta:
        model = Appointment
        fields = ['id', 'patient_id', 'doctor_id', 'schedule_id', 'appointment_date', 'appointment_time', 'symptoms', 'status', 'booked_at']