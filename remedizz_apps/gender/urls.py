from django.urls import path
from remedizz_apps.gender.controller import GenderController

urlpatterns = [
    path('create/', GenderController.create_gender, name='create_gender'),  # create
    path('', GenderController.get_all_genders, name='gender-list-create'),  # get all
    path('<int:gender_id>/', GenderController.get_gender_by_id, name='gender-retrieve'),  # get specific
    path('update/<int:gender_id>/', GenderController.update_gender, name='update_gender'),  # update
    path('delete/<int:gender_id>/', GenderController.delete_gender, name='delete_gender'),  # delete
]
