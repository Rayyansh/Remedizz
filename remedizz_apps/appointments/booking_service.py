from remedizz_apps.appointments.models import Appointment
from remedizz_apps.appointments.utils import check_slot_availability
from rest_framework.exceptions import ValidationError
from django.utils import timezone


class BookingService:
    @staticmethod
    def create_appointment(patient, validated_data):
        """
        Create an appointment using validated data from the serializer.
        The schedule is already resolved in the serializer.
        """
        return Appointment.objects.create(
            patient=patient,
            doctor=validated_data['doctor'],
            schedule=validated_data['schedule'],
            appointment_date=validated_data['appointment_date'],
            appointment_time=validated_data['appointment_time'],
            symptoms=validated_data.get('symptoms'),
            status=validated_data.get('status', 'Pending'),
        )

    @staticmethod
    def update_appointment(appointment_id, validated_data):
        """
        Update an existing appointment. Assumes validation is already handled.
        """
        appointment = Appointment.objects.get(id=appointment_id)

        for field, value in validated_data.items():
            setattr(appointment, field, value)

        appointment.save()
        return appointment