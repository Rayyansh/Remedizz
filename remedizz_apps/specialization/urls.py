from django.urls import path
from remedizz_apps.specialization.controller import SpecializationrController

urlpatterns = [
    path('specializations/create/', SpecializationrController.create_specialization, name='create_specialization'),  # create
    path('specializations/', SpecializationrController.get_all_specialization, name='specialization-list-create'),  # get all
    path('specializations/<int:specialization_id>/', SpecializationrController.get_specialization_by_id, name='specialization-retrieve'),  # get specific
    path('specializations/update/<int:specialization_id>/', SpecializationrController.update_specialization, name='update_specialization'),  # update
    path('specializations/delete/<int:specialization_id>/', SpecializationrController.delete_specialization, name='delete_specialization'),  # delete
]
