from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
import random
from datetime import timedelta
from django.utils.timezone import now

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError



class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('digital_clinic', 'Digital Clinic'),
    )
    
    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be exactly 10 digits."
    )

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        ("username"),
        max_length=20,
        help_text=(
            "Required. 20 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
    )
    email = models.EmailField(("email address"), blank=True, max_length=25)
    is_staff = models.BooleanField(
        ("staff status"),
        default=False,
        help_text=("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        ("active"),
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email"]


    date_joined = models.DateTimeField(("date joined"), default=now)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=10,
        unique=True,
        null=False,
        blank=False,
        help_text="Required: 10-digit phone number"
    )
    profile_picture = models.ImageField(upload_to="users/profile_pictures/", null=True, blank=True, max_length=50)
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
        return self.otp

    def is_otp_valid(self, otp):
        """Validate the OTP"""
        if self.otp == otp and self.otp_expiry and now() < self.otp_expiry:
            return True
        return False
    
    def save(self, *args, **kwargs):
        # Run phone_number validators only
        for validator in self._meta.get_field('phone_number').validators:
            validator(self.phone_number)
        
        super().save(*args, **kwargs)
    