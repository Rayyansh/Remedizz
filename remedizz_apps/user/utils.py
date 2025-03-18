import jwt
import datetime
from django.conf import settings

def send_otp_sms(phone_number, otp):
    """Send OTP via SMS using Twilio."""
    pass

def generate_jwt_token(user):
    """Generate JWT token for authenticated user."""
    payload = {
        'user_id': user.id,
        'username': user.username,
        'role': user.role,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1),
        'iat': datetime.datetime.now(datetime.timezone.utc)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token
