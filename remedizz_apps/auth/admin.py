from django.contrib import admin
from remedizz_apps.auth.models import User, OTP


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "user_role", "contact_number")


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ("user", "otp_code", "created_at")
