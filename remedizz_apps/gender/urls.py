from django.urls import path
from remedizz_apps.gender.controller import GenderController

urlpatterns = [
    path('genders/create/', GenderController.create_gender, name='create_gender'),  # create
    path('genders/', GenderController.get_all_genders, name='gender-list-create'),  # get all
    path('genders/<int:gender_id>/', GenderController.get_gender_by_id, name='gender-retrieve'),  # get specific
    path('genders/update/<int:gender_id>/', GenderController.update_gender, name='update_gender'),  # update
    path('genders/delete/<int:gender_id>/', GenderController.delete_gender, name='delete_gender'),  # delete
]
