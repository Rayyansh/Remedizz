from rest_framework.views import APIView
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

class UserAuthView(APIView):

    def auth_process(self, params):
        serializer = UserAuthSerializer(data=params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = params.get('username')
        phone_number = params.get('phone_number')
        role = params.get('role')
        
        user, created = User.objects.get_or_create(username=username, phone_number=phone_number, role=role)
        
        otp = default_token_generator.make_token(user)[:6]
        user.otp = otp
        user.otp_expiry = timezone.now() + timezone.timedelta(minutes=5)
        user.save()
        
        send_otp_sms(phone_number, otp)
        
        return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)

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

class DoctorOnlyView(APIView):
    permission_classes = [IsDoctor]
    
    def get(self, request):
        return Response({"message": "Welcome, Doctor!"}, status=status.HTTP_200_OK)

class PatientOnlyView(APIView):
    permission_classes = [IsPatient]
    
    def get(self, request):
        return Response({"message": "Welcome, Patient!"}, status=status.HTTP_200_OK)

class DigitalClinicOnlyView(APIView):
    permission_classes = [IsDigitalClinic]
    
    def get(self, request):
        return Response({"message": "Welcome, Digital Clinic!"}, status=status.HTTP_200_OK)
