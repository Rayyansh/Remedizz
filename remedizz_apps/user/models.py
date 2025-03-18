from django.contrib.auth.models import AbstractUser
from django.db import models
import random
from datetime import timedelta
from django.utils.timezone import now

class User(AbstractUser):
    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('digital_clinic', 'Digital Clinic'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=20, unique=True)
    profile_picture = models.ImageField(upload_to="users/profile_pictures/", null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    max_otp_try = models.CharField(max_length=2, default=3)
    otp_max_out = models.DateTimeField(blank=True, null=True)
    token = models.CharField(max_length=100, blank=True, null=True)


    class Meta:
        db_table = 'user'

    def __str__(self):
        return f"{self.username} ({self.role})"

    def generate_otp(self):
        """Generate and store a 6-digit OTP with expiry time."""
        self.otp = str(random.randint(100000, 999999))
        self.otp_expiry = now() + timedelta(minutes=5)  # OTP valid for 5 mins
        self.save()

    def is_otp_valid(self, otp):
        """Validate the OTP"""
        if self.otp == otp and self.otp_expiry and now() < self.otp_expiry:
            return True
        return False