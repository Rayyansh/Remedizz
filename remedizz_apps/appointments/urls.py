from django.urls import path
from .controller import BookingController

urlpatterns = [
    path('appointment/', BookingController.get_all_appointment, name='booking-list'),
    path('appointment/create/', BookingController.create_appointment, name='booking-create'),
    path('appointment/<int:appointment_id>/', BookingController.get_appointment, name='booking-detail'),
    path('appointment/status/<int:appointment_id>/', BookingController.get_appointment_status, name='booking-status'),




    # path('bookings/search/', BookingController.search_bookings, name='booking-search'),
]




