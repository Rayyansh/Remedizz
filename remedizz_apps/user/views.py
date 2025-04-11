from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from remedizz_apps.user.models import User
from remedizz_apps.user.serializers import UserAuthSerializer, OTPVerifySerializer
from remedizz_apps.user.serializers import UserAuthResponseSerializer
from remedizz_apps.user.utils import send_otp_sms
from remedizz_apps.user.utils import generate_jwt_token
from remedizz_apps.user.permissions import IsDoctor, IsPatient, IsDigitalClinic, IsAuthenticatedUser
from remedizz_apps.patients.models import Patient
from remedizz_apps.doctors.models import Doctor
from remedizz_apps.clinics.models import DigitalClinic
from django.db import transaction

class UserAuthView(APIView):
    permission_classes = [AllowAny]

    def auth_process(self, params):
        serializer = UserAuthSerializer(data=params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = params.get('username')
        phone_number = params.get('phone_number')
        role = params.get('role')

        try:
            with transaction.atomic():
                user, created = User.objects.get_or_create(username=username, phone_number=phone_number, role=role)

                if created:
                    if role == "Patient":
                        Patient.objects.create(patient_id=user,name=username)

                    elif role == "Doctor":
                        # Providing default values for required fields
                        Doctor.objects.create(
                            doctor_id=user,
                            name=username
                        )

                    elif role == "DigitalClinic":
                        DigitalClinic.objects.create(
                            digital_clinic_id=user,
                            name=username
                        )

                    else:
                        return Response({"error": "Invalid role provided."}, status=status.HTTP_400_BAD_REQUEST)

                # Generate OTP
                otp = default_token_generator.make_token(user)[:6]
                user.otp = otp
                user.otp_expiry = timezone.now() + timezone.timedelta(minutes=5)
                user.save()

                # Send OTP
                send_otp_sms(phone_number, otp)

                return Response({"message": "OTP sent successfully.", "OTP":{otp}}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def verify_otp(self, params):
        serializer = OTPVerifySerializer(data=params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        otp = params.get('otp')
        
        try:
            user = User.objects.get(otp=otp, otp_expiry__gte=timezone.now())
        except User.DoesNotExist:
            return Response({"error": "Invalid OTP or OTP expired."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.otp = None
        user.otp_expiry = None
        user.save()
        
        token = generate_jwt_token(user)
        
        response_data = UserAuthResponseSerializer(user).data
        response_data["token"] = token
        
        return Response(response_data, status=status.HTTP_200_OK)
