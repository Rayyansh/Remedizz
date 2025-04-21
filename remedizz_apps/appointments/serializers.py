from rest_framework import serializers
from .models import Appointment
from remedizz_apps.doctors.models import DoctorSchedule , Doctor
from remedizz_apps.doctors.serializers import DoctorScheduleSerializer ,DoctorResponseSerializer
from remedizz_apps.patients.models import Patient




# Serializer for Booking Request (used when creating a booking)
class BookingRequestSerializer(serializers.ModelSerializer):
    #patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())
    # schedule = serializers.PrimaryKeyRelatedField(queryset=DoctorSchedule.objects.all(), required=False)
    status = serializers.ChoiceField(choices=Appointment.STATUS_CHOICES, required=False)

    class Meta:
        model = Appointment
        fields = [ 'doctor',  'symptoms','status',]

    def validate(self, data):
    
        doctor = data.get('doctor')
        schedule = data.get('schedule')
       

   
        if not schedule:
            pass
            # raise serializers.ValidationError("Schedule is required for booking.")
        
        return data
    

    def create(self, validated_data):
        # Default to "Pending" if not provided
        validated_data['status'] = validated_data.get('status', 'Pending')
        return super().create(validated_data)

    

class BookingResponseSerializer(serializers.ModelSerializer):
    # patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    doctor =  DoctorResponseSerializer() 
    patient_id = serializers.IntegerField(source='patient.id') 
    # schedule = DoctorScheduleSerializer() 
   
   

    class Meta:
        model = Appointment
        fields = ['id', 'patient_id', 'doctor',  'symptoms', 'status', 'booked_at']


class BookingListSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    doctor =  DoctorResponseSerializer()  

    class Meta:
        model = Appointment
        fields = ['id',  'booked_at', 'patient', 'doctor']


class BookingUpdateSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Appointment.STATUS_CHOICES)

    class Meta:
        model = Appointment
        fields = ['status']

    def validate_status(self, status):
      
        appointment = self.instance
        if  appointment and  appointment.status == status:
            raise serializers.ValidationError("Status is already set to this value.")
        return status
    





