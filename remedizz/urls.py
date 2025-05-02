from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('remedizz_apps.user.urls')),
    path('patients/', include('remedizz_apps.patients.urls')),
    path('doctors/', include('remedizz_apps.doctors.urls')),
    path('clinics/', include('remedizz_apps.clinics.urls')),
    path('appointments/', include('remedizz_apps.appointments.urls')),
    path('city/', include('remedizz_apps.city.urls')),
    path('gender/', include('remedizz_apps.gender.urls')),
    path('specialization/', include('remedizz_apps.specialization.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

